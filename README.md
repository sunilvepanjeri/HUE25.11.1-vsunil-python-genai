# 🧠 Multi-Agent Code Analyzer & Documentation Generator

This project provides an end-to-end workflow for **user authentication**, **file upload**, **code analysis**, **automatic documentation generation**, and **querying a LangGraph-powered multi-agent system**.  
The system uses **FastAPI**, **Streamlit**, **Chromadb**, **OpenAI models**, and **LangGraph** to deliver an intelligent and interactive developer assistant.

---

## 🚀 Features

### 🔐 **User Authentication**
- Secure **Signup** and **Login** endpoints  
- Implemented using **FastAPI** and **Pydantic** for validation  
- Once authenticated, the user can upload files  

### 📁 **ZIP File Upload**
- Users upload a `.zip` file containing source code  
- The system extracts and processes the files automatically  

### 🤖 **LangGraph Multi-Agent System**
- Designed to:
  - Analyze source code  
  - Generate detailed documentation  
  - Index the documentation in a vector store  
  - Allow natural language queries about the uploaded project  

### 💬 **Chat Interface**
- Query system documentation using natural language  
- Powered by **OpenAI LLMs** and LangGraph agents  
- Vector search using **Chromadb**  

### 🖥️ **Frontend & Backend**
- **Streamlit** frontend (`ui.py`)  
- **FastAPI** backend (`main.py`)  
- Three major endpoints:
  1. `/signup`  
  2. `/login`  
  3. `/query` — for asking questions to the code-analysis bot  

---

## 🏗️ Tech Stack

| Component | Technology |
|----------|------------|
| Backend Framework | **FastAPI** |
| Frontend UI | **Streamlit** |
| LLM Provider | **OpenAI** |
| Multi-Agent Framework | **LangGraph** |
| Vector Store | **Chromadb** |
| Data Validation | **Pydantic** |
| Authentication | Custom login/signup system |
| File Handling | ZIP upload & extraction |

---

