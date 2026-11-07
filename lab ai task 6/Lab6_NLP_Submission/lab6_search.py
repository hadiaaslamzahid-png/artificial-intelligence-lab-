import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class Retriever:
    def __init__(self, records, backend="tfidf"):
        if not records or any(not r["text"].strip() for r in records):
            raise ValueError("Please provide non-empty text records.")
        if backend not in ("tfidf", "embedding"):
            raise ValueError("Backend must be tfidf or embedding.")

        self.records = records
        self.backend = backend

        if backend == "tfidf":
            self.vectorizer = TfidfVectorizer()
            self.matrix = self.vectorizer.fit_transform(
                [r["text"] for r in records]
            )
        else:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError as exc:
                raise RuntimeError(
                    "For embeddings, install sentence-transformers first."
                ) from exc

            self.model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2", device="cpu"
            )
            self._check_length([r["text"] for r in records])
            self.matrix = self.model.encode(
                [r["text"] for r in records],
                normalize_embeddings=True
            )

    def _check_length(self, texts):
        for item in texts:
            token_ids = self.model.tokenizer(
                item, truncation=False
            )["input_ids"]
            if len(token_ids) > self.model.max_seq_length:
                raise ValueError(
                    "Text is longer than the model input limit. Split it first."
                )

    def search(self, query, k=3, filters=None):
        if not query.strip() or k <= 0:
            return []

        if self.backend == "tfidf":
            query_vector = self.vectorizer.transform([query])
            if query_vector.nnz == 0:
                return []
            scores = (query_vector @ self.matrix.T).toarray()[0]
        else:
            self._check_length([query])
            query_vector = self.model.encode(
                [query], normalize_embeddings=True
            )[0]
            scores = self.matrix @ query_vector

        allowed = [
            i for i, record in enumerate(self.records)
            if all(record.get(key) == value
                   for key, value in (filters or {}).items())
        ]
        ranked = sorted(allowed, key=lambda i: (-float(scores[i]), i))
        return [
            (self.records[i], float(scores[i]))
            for i in ranked[:k]
        ]


def show_hits(hits):
    if not hits:
        print("No matching records.")
    for record, score in hits:
        print(f'{record["id"]} | score={score:.3f}')
        print(record["text"])
