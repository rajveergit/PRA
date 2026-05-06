import json
import os
import sys

# Ensure we can import from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag_pipeline import RAGPipeline

def evaluate_rag_system(rag_chain_query_func, test_queries_path: str, output_path: str):
    with open(test_queries_path, 'r') as f:
        queries = json.load(f)

    results = []
    print(f"Starting evaluation of {len(queries)} queries...")
    for q in queries:
        print(f"Evaluating: {q['id']} - {q['query']}")
        try:
            response = rag_chain_query_func(q["query"])
            answer = response.get("answer", "")
        except Exception as e:
            answer = f"Error: {e}"
            
        results.append({
            "id": q["id"],
            "query": q["query"],
            "expected": q["ground_truth"],
            "category": q.get("category", ""),
            "generated_answer": answer,
        })
        
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)
        
    print(f"Evaluation finished. Results saved to {output_path}")
    return results

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_queries_file = os.path.join(current_dir, "test_queries.json")
    output_file = os.path.join(current_dir, "evaluation_results.json")
    
    db_path = os.path.join(os.path.dirname(current_dir), "chroma_db")
    
    try:
        pipeline = RAGPipeline(persist_dir=db_path)
        evaluate_rag_system(pipeline.query, test_queries_file, output_file)
    except Exception as e:
        print(f"Evaluation setup failed: {e}. (Ensure environment, keys, and database are setup)")
