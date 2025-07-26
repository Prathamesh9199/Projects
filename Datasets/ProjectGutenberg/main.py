from datasets import load_dataset
import os
from tqdm import tqdm

# Create a folder to save individual books
os.makedirs("data", exist_ok=True)

# Load Project Gutenberg dataset with English books in streaming mode
ds = load_dataset("manu/project_gutenberg", split="en", streaming=True)

# Save first 10 books to individual .txt files
for i, book in tqdm(enumerate(ds), total=10):
    if i >= 10:
        break
    title = book.get("title", f"book_{i}")
    filename = f"data/book_{i+1:02d}_{title.replace(' ', '_').replace('/', '')[:50]}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(book["text"])
