import os
import re
import sys
import pandas as pd
import json
from langchain_text_splitters.character import RecursiveCharacterTextSplitter

def _print(msg: str):
    safe = msg.encode('ascii', errors='ignore').decode('ascii')
    print(safe)

def extract_metadata(filename: str) -> dict:
    metadata = {"source": filename}
    lower_name = filename.lower()
    
    if "tata" in lower_name: metadata["vehicle_brand"] = "Tata"
    elif "maruti" in lower_name: metadata["vehicle_brand"] = "Maruti"
    
    if "nexon" in lower_name: metadata["vehicle_model"] = "Nexon"
    elif "swift" in lower_name: metadata["vehicle_model"] = "Swift"
    elif "creta" in lower_name: metadata["vehicle_model"] = "Creta"
    
    if "2023" in lower_name: metadata["year"] = "2023"
    
    if "performance" in lower_name: metadata["document_type"] = "performance_report"
    elif "manual" in lower_name: metadata["document_type"] = "owner_manual"
    elif "safety" in lower_name or "ncap" in lower_name: metadata["document_type"] = "safety_report"
    elif "emission" in lower_name or "bs6" in lower_name: metadata["document_type"] = "emission_data"
    elif "obd" in lower_name: metadata["document_type"] = "diagnostic_data"
    elif "dyno" in lower_name: metadata["document_type"] = "dyno_test"
    else: metadata["document_type"] = "unknown"
        
    return metadata

def clean_text(text: str) -> str:
    """Remove noise from extracted automobile documents."""
    text = re.sub(r'Page \d+ of \d+', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'\|{2,}', ' ', text)
    text = ' '.join(text.split())
    return text.strip()

def chunk_documents(text: str, metadata: dict) -> list:
    """Chunk text into overlapping segments for optimal retrieval."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=64,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.create_documents([text], metadatas=[metadata])
    return chunks

def process_files(raw_dir: str, processed_dir: str, status_callback=None):
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)
        
    all_chunks = []
    
    for filename in os.listdir(raw_dir):
        file_path = os.path.join(raw_dir, filename)
        metadata = extract_metadata(filename)
        
        if filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            cleaned_text = clean_text(content)
            chunks = chunk_documents(cleaned_text, metadata)
            all_chunks.extend(chunks)
            msg = f"📄 {filename}: {len(chunks)} chunks generated"
            _print(msg)
            if status_callback: status_callback(msg)
            
        elif filename.endswith('.csv'):
            df = pd.read_csv(file_path)
            from langchain_core.documents import Document
            row_docs = []
            for _, row in df.iterrows():
                row_text = " | ".join(f"{col}: {val}" for col, val in row.items() if pd.notnull(val))
                row_docs.append(Document(page_content=row_text, metadata=dict(metadata)))
            all_chunks.extend(row_docs)
            msg = f"📊 {filename}: {len(row_docs)} chunks generated (1 per row)"
            _print(msg)
            if status_callback: status_callback(msg)
            
    dict_chunks = [{"page_content": c.page_content, "metadata": c.metadata} for c in all_chunks]
    
    output_path = os.path.join(processed_dir, 'processed_chunks.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dict_chunks, f, indent=4)
        
    msg = f"Total: {len(dict_chunks)} chunks saved to processed_chunks.json"
    _print(msg)
    if status_callback: status_callback(msg)


if __name__ == "__main__":
    raw_dir = os.path.join(os.path.dirname(__file__), "data", "raw")
    processed_dir = os.path.join(os.path.dirname(__file__), "data", "processed")
    process_files(raw_dir, processed_dir)
