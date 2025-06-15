<div align="center">

# 🤖 Grievance RAG Chatbot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat&logo=mongodb&logoColor=white)](https://www.mongodb.com/)

✨ A powerful RAG (Retrieval-Augmented Generation) chatbot built with FastAPI that delivers intelligent responses by combining document retrieval with advanced language models.

</div>

## ✨ Features

- 🚀 **FastAPI Backend**: Blazing fast API built with FastAPI
- 🗄️ **MongoDB Integration**: Robust data storage and retrieval
- 🔒 **Authentication**: Secure user authentication system
- ⚙️ **Environment Configuration**: Easy setup with `.env` files
- 📝 **Logging**: Comprehensive logging with Loguru
- 🤖 **AI-Powered**: Leverages MistralAI for intelligent responses
- 🔄 **Real-time Updates**: Hot-reload for development

## 📋 Prerequisites

- 🐍 Python 3.8+
- 🍃 MongoDB (local or cloud instance)
- 🏗️ Python virtual environment (recommended)

## 🚀 Installation

1. 🎯 Clone the repository:
   ```bash
   git clone <repository-url>
   cd rag_chatbot
   ```

2. 🛠️ Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # or
   source .venv/bin/activate  # On macOS/Linux
   ```

3. 📦 Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. 🔧 Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update the variables in `.env` with your configuration

## ⚙️ Configuration

Rename `.env.example` to `.env` and configure the following environment variables:

```
# Database
MONGO_CONN_STR=your_mongo_connection_string_here

# Authentication
LLM_API_KEY=your_mistral_ai_api_key_here
LLM_MODEL=your_mistral_ai_model_here
```

## 🚦 Running the Application

Start the development server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at 🔗 `http://127.0.0.1:8000`

## 🌐 Live Demo

The application is deployed and available at: [https://grievance-rag-chatbot.onrender.com/](https://grievance-rag-chatbot.onrender.com/)
> Note: It may take up to 1 minute to bring the service up as Render.com sets the state to sleep due to 15 minutes of inactivity.

## 📚 API Documentation

Once the server is running, you can access the interactive API documentation at:

- 📘 **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- 📚 **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

> 💡 Try out the API endpoints directly from the Swagger UI!

## 📁 Project Structure

```

grievance_rag_chatbot/
├── app/                    # Application source code
│   ├── __init__.py
│   ├── main.py             # FastAPI application
│   ├── models/             # Pydantic models
│   ├── routes/             # API routes
│   ├── services/           # Business logic
│   └── utils/              # Utility functions
├── static/                 # Static files
├── .env                    # Environment variables
├── .env.example            # Example environment variables
├── .gitignore
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

## 📄 License

📄 This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- 🚀 [FastAPI](https://fastapi.tiangolo.com/) for the awesome web framework
- 🍃 [MongoDB](https://www.mongodb.com/) for the database
- 🤖 [MistralAI](https://mistral.ai/) for the powerful language model
- 🙏 All the amazing open-source projects that made this possible
