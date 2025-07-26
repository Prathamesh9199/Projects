import re
import ollama
from pathlib import Path
from llm_prompt import prompt
from concurrent.futures import ThreadPoolExecutor, as_completed

def call_mistral(chunk, i):
    print(f"[Thread {i}] Calling mistral for chunk...")
    final_prompt = prompt.format(chunk=chunk)
    response = ollama.chat(model='mistral:7b', messages=[
        {"role": "user", "content": final_prompt}
    ])
    return response['message']['content'].replace('\\n', '')

def data_cleaning(text, output_path, chunk_size=1000, max_chunks=10):
    print("🚀 Starting parallel data cleaning using Mistral 7B (Ollama + GPU)...")
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)][:max_chunks]

    processed_chunks = [''] * len(chunks)
    with ThreadPoolExecutor(max_workers=4) as executor:  # adjust to match your GPU/thread capacity
        futures = {
            executor.submit(call_mistral, chunk, i): i for i, chunk in enumerate(chunks)
        }
        for future in as_completed(futures):
            i = futures[future]
            try:
                result = future.result()
                processed_chunks[i] = result
            except Exception as e:
                print(f"[Thread {i}] ❌ Error: {e}")

    final_output = "\n\n".join(processed_chunks)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_output)

    print("✅ Done. Cleaned and rephrased output saved.")

def main():
    input_path = Path("data/cleaned_combined_books.txt")
    output_path = Path("data/final_cleaned_output.txt")
    text = input_path.read_text(encoding='utf-8')
    data_cleaning(text, output_path)

if __name__ == "__main__":
    main()