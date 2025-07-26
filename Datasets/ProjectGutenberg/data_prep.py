import os
import re

def clean_text(text):
    # Remove emails
    text = re.sub(r'\S+@\S+', '', text)
    # Keep only allowed punctuation and alphanumeric characters
    text = re.sub(r"[^a-zA-Z0-9\s\.\,\;\:\'\“\”\"\?\!]", '', text)
    # Normalize multiple spaces/newlines
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Combine all texts into a single cleaned file
combined_text = ""

folder_path = "data\\processed_books"

for filename in sorted(os.listdir(folder_path)):
    if filename.endswith(".txt"):
        with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
            raw_text = f.read()
            cleaned = clean_text(raw_text)
            combined_text += cleaned + "\n\n"  # Add spacing between books

# Save final cleaned text to one file
with open("data\\cleaned_combined_books.txt", "w", encoding="utf-8") as f:
    f.write(combined_text)
