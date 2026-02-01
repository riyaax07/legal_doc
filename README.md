# 🧠 LegalAI – EU AI Act Document Assistant

LegalAI is an AI-powered document question-answering system that allows users to **ask natural language questions about the EU Artificial Intelligence Act** and receive **accurate, document-grounded answers** through a chat interface.

This project uses **Retrieval-Augmented Generation (RAG)** to ensure responses are based strictly on the original legal text, reducing hallucinations and improving trustworthiness.

---

## 🚀 Problem Statement

Legal documents like the **EU AI Act** are:
- Extremely long and complex  
- Difficult to navigate and understand  
- Inefficient to search manually  

Students, developers, startups, and researchers often struggle to extract **specific, relevant information** from such documents quickly and accurately.

---

## 💡 Solution

LegalAI solves this by:
- Converting the EU AI Act PDF into searchable text  
- Embedding the text into a vector database  
- Retrieving only the most relevant sections for each question  
- Generating concise answers strictly from retrieved content  

This ensures **accuracy, transparency, and reliability**.

---

## 🧠 Core Concept: Retrieval-Augmented Generation (RAG)

This project follows a **RAG architecture**, which combines:

1. **Document Retrieval** – Finds relevant sections from the law  
2. **Language Generation** – Uses an LLM to generate answers from retrieved content  

Unlike traditional chatbots, LegalAI does **not guess or hallucinate**.

---

## 🏗️ Architecture Overview

1. **PDF Processing**
   - Downloads and parses the EU AI Act PDF  
   - Converts it into raw text using PyMuPDF  

2. **Text Chunking**
   - Splits text into manageable sections  

3. **Embedding & Storage**
   - Converts chunks into vector embeddings  
   - Stores them in **ChromaDB**  

4. **Query Flow**
   - User asks a question  
   - Relevant chunks are retrieved via similarity search  
   - LLM generates a grounded response  

5. **Chat Interface**
   - Built using **Streamlit**  
   - Maintains chat history per session  

---

## 🛠️ Tech Stack

- **Python**
- **LangChain**
- **ChromaDB** (Vector Database)
- **OpenAI Embeddings & Chat Models**
- **Streamlit**
- **PyMuPDF**

---

## 📁 Project Structure

legal_doc/
│
├── app.py # Streamlit application
├── agent.py # RAG + chat logic
├── embed.py # PDF parsing & vector embedding
├── utils.py # Constants and helpers
├── chroma_db/ # Persistent vector database
├── requirements.txt
└── README.md


---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/riyaax07/legal_doc
cd legal_doc
2️⃣ Create Virtual Environment
python -m venv venv
Activate it:

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Set OpenAI API Key
# macOS / Linux
export OPENAI_API_KEY="your_api_key_here"

# Windows
setx OPENAI_API_KEY "your_api_key_here"
5️⃣ Run the App
streamlit run app.py
💬 Example Questions You Can Ask
What is the purpose of the EU AI Act?

What are high-risk AI systems?

What obligations apply to AI system providers?

Are biometric systems regulated?

What penalties exist for non-compliance?

🎯 Use Cases
📚 Students studying AI regulation

🚀 Startups checking AI compliance

🧑‍💻 Developers building regulated AI systems

🏛️ Policy and legal researchers

🧪 Key Learnings
Building RAG-based systems end-to-end

Working with vector databases and embeddings

Managing real-world dependency conflicts

Handling LLM limitations and API constraints

Designing explainable and trustworthy AI systems

🔮 Future Improvements
Document citation highlighting

Support for multiple legal documents

Local/offline embedding models

Role-based explanations (student / lawyer / startup)

Improved UI with section references

📜 Disclaimer
This tool is for educational and informational purposes only and does not constitute legal advice.

⭐ Support
If you found this project helpful, consider giving it a ⭐ on GitHub — it really helps!
