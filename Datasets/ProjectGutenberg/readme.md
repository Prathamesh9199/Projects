* Script to download and preprocess the Project Gutenberg dataset for English books.

What is this script doing?
1. Downloads N books from Project Gutenberg in streaming mode.
2. Saves each book as a .txt file in a folder named "books".
3. Combines all texts into a single cleaned file, separated by spacing between books.
4. Cleans the text to remove emails and keep only allowed punctuation and alphanumeric characters.

How can I use this script?
1. python -m venv .venv
2. source .venv/bin/activate
3. pip install datasets
4. python main.py
5. python data_prep.py
