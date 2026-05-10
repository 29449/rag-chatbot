import os
import streamlit as st
import tempfile
from zhipuai import ZhipuAI

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from FlagEmbedding import FlagReranker

# ===== 初始化 =====
client = ZhipuAI(api_key="ZHIPU_API_KEY")
reranker = FlagReranker('BAAI/bge-reranker-base', use_fp16=True)

# 向量数据库构造
@st.cache_resource
def load_db(file):
    loader = PyPDFLoader(file)
    documents = loader.load()
    documents = documents[:5]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3"
    )

    # 本地内存向量数据库
    # db = FAISS.from_documents(chunks, embeddings)
    # 向量数据库升级为Chroma
    if os.path.exists("./chroma_db"):
        db = Chroma(
            persist_directory="./chroma_db",
            embedding_function=embeddings
        )
    else:
        db = Chroma.from_documents(
            chunks,
            embeddings,
            persist_directory="./chroma_db"
        )

    return db

# 向量重排序
def rerank(query, docs):
    pairs = [[query, doc.page_content] for doc in docs]

    scores = reranker.compute_score(pairs)

    # 按分数排序
    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)

    return [doc for doc, score in ranked]

# LLM改写问题
def rewrite_query(query):
    response = client.chat.completions.create(
        model="glm-4.5-flash",
        messages=[
            {"role": "system", "content": "把用户问题改写成更完整的检索问题"},
            {"role": "user", "content": query}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content

# 将提示词输入至LLM
def ask_llm(prompt):
    response = client.chat.completions.create(
        model="glm-4.5-flash",
        messages=[
            {"role": "system", "content": "请基于资料回答问题，不要胡编"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

# ===== 页面 =====
st.title("📚 我的RAG问答系统")

uploaded_file = st.file_uploader("上传你的PDF文件", type="pdf")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        db = load_db(temp_file.name)
else:
    st.warning("请先上传你的PDF文件")

question = st.text_input("请输入你的问题：")

if question:
    # 加“对话记忆”
    if "history" not in st.session_state:
        st.session_state.history = []
    history_text = ""
    for q, a in st.session_state.history:
        history_text += f"用户：{q}\nAI：{a}\n"

    # 获取数据库
    # question = rewrite_query(question)
    docs = db.similarity_search(question, k=5)
    docs = rerank(question, docs)[:2]
    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
        以下是历史对话：
        {history_text}

        请根据以下资料回答问题：
        资料：
        {context}

        当前问题：
        {question}
        """

    answer = ask_llm(prompt)

    st.session_state.history.append((question, answer))

    st.write("## 💬 对话记录")

    for q, a in st.session_state.history:
        st.write("🙋‍♂️", q)
        st.write("🤖", a)
