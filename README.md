**📚 RAG PDF Chatbot**

一个基于大语言模型（LLM）的本地知识库问答系统，支持 PDF 上传、多轮对话、语义检索与 RAG（Retrieval-Augmented Generation）问答。

**🚀 项目效果**

用户可以：

1、上传 PDF 文档
2、对论文 / 文档进行问答
3、进行多轮对话
4、基于文档内容生成回答
5、使用向量数据库进行语义检索
6、使用 Rerank 提升检索精度

**🧠 项目架构**

用户问题
   ↓
Query Rewrite（问题改写）
   ↓
Embedding 向量化
   ↓
Chroma 向量数据库检索
   ↓
Rerank 重排序
   ↓
拼接上下文 Prompt
   ↓
LLM 生成最终答案

**🛠️ 技术栈**
LLM
* GLM-4.5-Flash
* 智谱 AI API

RAG Framework
* LangChain

Vector Database
* Chroma
* FAISS（实验版本）

Embedding Model
* BAAI/bge-m3
* BAAI/bge-small-zh-v1.5

Rerank
* BAAI/bge-reranker-base

Frontend
* Streamlit

Document Loader
* PyPDFLoader

**✨ 核心功能**

✅ PDF 上传
支持上传论文、技术文档等 PDF 文件。

✅ 文本切分（Chunking）
使用 RecursiveCharacterTextSplitter 进行文本分块，并通过 overlap 保持上下文连续性。

✅ 向量检索
通过 Embedding 将文本转换为向量，并使用 Chroma 进行语义检索。

✅ Rerank 重排序
使用 Cross Encoder 对召回结果进行重排序，提高检索精度。

✅ 多轮对话记忆
支持基于历史对话进行上下文问答。

✅ Query Rewrite
通过 LLM 自动改写用户问题，提高检索召回率。

**📂 项目结构**

rag-chatbot/
│
├── app.py                 # Streamlit 主程序
├── requirements.txt       # 项目依赖
├── README.md              # 项目说明
├── chroma_db/             # 向量数据库（本地持久化）
└── sample.pdf             # 测试文件（可选）

**⚡ 本地运行**

1️⃣ 克隆项目
git clone https://github.com/29449/rag-chatbot.git
cd rag-chatbot

2️⃣ 创建虚拟环境
python3 -m venv rag
source rag/bin/activate

3️⃣ 安装依赖
pip install -r requirements.txt

4️⃣ 配置 API KEY
推荐使用环境变量：
export ZHIPU_API_KEY="你的API_KEY"

5️⃣ 启动项目
streamlit run app.py

**🎯 项目亮点**

* 从零实现完整 RAG Pipeline
* 支持本地知识库问答
* 实现 Query Rewrite + Rerank
* 支持 Chroma 持久化存储
* 支持多轮对话记忆
* 支持论文问答场景
* 完成 Web 化部署

**📈 后续优化方向**

* Hybrid Search（BM25 + Vector Search）
* Agent 工作流
* 多文件知识库
* OCR 文档解析
* Milvus / Elasticsearch 替换向量数据库
* Docker 部署
* 云端部署

**💬 项目背景**

该项目用于学习与实践 LLM 应用开发、RAG 架构以及 AI 工程化能力。

通过本项目，完成了：
* LangChain 使用
* 向量数据库构建
* Embedding 与语义检索
* Rerank 排序
* Prompt Engineering
* Streamlit Web 开发
* Git/GitHub 工程管理

**👨‍💻 Author**

浙江工业大学 ｜ AI方向研究生

如果这个项目对你有帮助，欢迎 Star ⭐
