# Automobile Performance Analyzer 🚗

An AI-powered system that intelligently analyzes automobile performance reports, technical manuals, and diagnostic data — enabling users to query, compare, and extract insights through natural language conversation.

## Features

- **Natural Language Querying:** Ask technical questions about vehicle specs and get direct answers.
- **Source Citations:** Every answer cites the source document ensuring accuracy and no hallucinations.
- **Diagnostic Interpreter:** Look up OBD fault codes to understand root problems and fixes.
- **RAG Architecture:** Uses Retrieval-Augmented Generation to leverage your own domain documents, avoiding fine-tuning costs.
- **Streamlit Interface:** A simple, elegant UI for chatting and uploading documents.

## Project Architecture

1. **Document Processor**: Extracts and cleans text from PDF/TXT/CSV files, chunking them into smaller token lists for embedding.
2. **Vector Database**: Embeds chunks using `HuggingFaceEmbeddings` and stores them persistently in ChromaDB.
3. **RAG Pipeline**: Combines ChatGoogleGenerativeAI (Gemini), MMR retrieval, and conversational memory context.

## Requirements & Setup

Ensure you have Python 3.10+ installed.

1. Install dependencies:
   ```bash
   pip install -r requirement.txt
   ```
2. Configure Gemini API Key:
   Create a `.env` file in the root directory:
   ```env
   MISTRAL_API_KEY="your-api-key-here"
   ```

## Running the Application

To run the Streamlit frontend locally:
```bash
 python -m streamlit run app.py
```
This deploys the chat UI where you can upload more reports, process them into the VectorDB, and query the Automobile AI.

## Sample Queries

Try asking the assistant:
- "What is the maximum power and torque of the Tata Nexon EV?"
- "Compare fuel efficiency between Maruti Swift petrol and diesel variants"
- "What does OBD fault code P0301 mean?"
