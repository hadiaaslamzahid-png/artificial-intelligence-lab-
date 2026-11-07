import re

samples = [
    "AI, search!",
    "I can't log in.",
    "help@example.com",
    "CS4944 version 2.1",
    "",
    "یہ ایک مثال ہے"
]

print("TASK 1: TOKENIZATION COMPARISON")
for original in samples:
    whitespace_tokens = original.split()
    word_tokens = re.findall(r"\b\w+\b", original, flags=re.UNICODE)

    print("\nOriginal:", repr(original))
    print("Whitespace tokens:", whitespace_tokens)
    print("Whitespace count:", len(whitespace_tokens))
    print("Word-like tokens:", word_tokens)
    print("Word-like count:", len(word_tokens))

print("\nNotes:")
print("1. Whitespace splitting keeps punctuation attached to words.")
print("2. The regular expression separates parts of contractions and email addresses.")
print("3. This simple expression is not a complete Urdu or multilingual tokenizer.")

try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2", device="cpu"
    )
    print("\nOptional model subword comparison:")
    for sample in samples[:2]:
        print(repr(sample), "=>", model.tokenizer.tokenize(sample))
except ImportError:
    print("\nModel tokenizer comparison skipped.")
    print("Install sentence-transformers to run this optional part.")
