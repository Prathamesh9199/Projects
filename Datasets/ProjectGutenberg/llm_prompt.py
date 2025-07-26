prompt = """
You are a highly skilled text-cleaning and rewriting assistant. You are given a block of raw English text that contains:

1. URLs (e.g., "http://example.com", "www.gutenberg.org")
2. Table of contents or index-like sections (often beginning with "CONTENTS", "CHAPTER I.", etc., and followed by chapter names or page numbers)
3. Chapter headings (e.g., "CHAPTER I. THE LIFE OF ADDISON", "CHAPTER VIII.")
4. Names of real people or fictional characters (any named individuals, including author/editor/compiler names)

Your tasks are:

### Step 1: Clean the text
- Remove **all URLs**
- Remove any section that resembles an **index** or **table of contents**  
  (e.g., lines with "CHAPTER" followed by Roman numerals and titles/page numbers)
- Remove all **chapter headings**
- Remove all **person names**, including authors, characters, editors, and historical figures. This includes single or multi-word names like:
  - “John Milton”, “SHELLEY J. A. Symonds”, “C. Morison”
  - Names inside list formats or sentences
  - Full names and initials
  - The list provided is not exhaustive but a sample, use named entity recognition to identify names and remove them
- DO NOT REMOVE common noun references like “the king,” “the author,” or “a poet” — only remove identifiable personal names.

### Step 2: Rephrase & Refactor
- After removals, rephrase the remaining content naturally so that the **meaning is preserved**.
- Rewrite the text so it **reads smoothly and coherently**, even where names, URLs, or structural sections were deleted.
- Fix or rephrase **broken or incomplete sentences** caused by the deletions.
- Make sure the resulting paragraphs are fluid, understandable, and logically connected.

### **Output Format**
- **Return the final cleaned and rewritten version of the input text.**
- **Do not mention that anything was removed.**
- **Do not include explanations or commentary — only return the final cleaned and rephrased content.**

Now, here is the input text:
---
{chunk}
---

Please return the cleaned and rewritten version."""