# %% Imports
import re
import numpy as np
import pandas as pd
import chromadb


# %% 1. Load the raw dataset
def load_data(path="faqs.csv"):
    """Load the raw FAQ CSV with Pandas."""
    return pd.read_csv(path)


# %% 2. Cleaning functions
def clean_text(text):
    """Lowercase, trim, remove symbols (lecture slide 12)."""
    t = str(text).lower().strip()
    t = re.sub(r"[^a-z0-9@.\s]", "", t)
    return re.sub(r"\s+", " ", t)


def handle_missing(df):
    """Drop rows with a blank question or answer."""
    df = df.copy()
    df = df.replace(r"^\s*$", np.nan, regex=True)
    return df.dropna(subset=["question", "answer"])


def remove_duplicates(df):
    """Keep each question once (case/space-insensitive)."""
    key = df["question"].map(clean_text)
    return df.loc[~key.duplicated()]


def fix_types(df):
    """Make sure both columns are strings."""
    df = df.copy()
    df["question"] = df["question"].astype(str)
    df["answer"] = df["answer"].astype(str)
    return df


def remove_outliers(df, z_max=3):
    """Drop answers whose word count is a z-score outlier (NumPy)."""
    df = df.copy()
    df["n_words"] = df["answer"].str.split().str.len()
    counts = df["n_words"].to_numpy()
    z = (counts - np.mean(counts)) / (np.std(counts) or 1)
    return df.loc[np.abs(z) <= z_max]


def clean_data(df):
    df = handle_missing(df)
    df = remove_duplicates(df)
    df = fix_types(df)
    df = remove_outliers(df)
    df["text"] = (df["question"] + " " + df["answer"]).map(clean_text)
    return df.reset_index(drop=True)


# %% 3. NumPy statistics
def length_stats(df):
    n = df["answer"].str.split().str.len().to_numpy()
    return {
        "mean": float(np.mean(n)),
        "median": float(np.median(n)),
        "std": float(np.std(n)),
        "p95": float(np.percentile(n, 95)),
    }


# %% 4. Chunking (lecture slide 13)
def chunk(words, size=200, overlap=40):
    step = size - overlap
    return [words[i : i + size] for i in range(0, len(words), step)]


def build_chunks(df):
    chunks, ids, metas = [], [], []
    for i, row in df.iterrows():
        for j, piece in enumerate(chunk(row["text"].split())):
            chunks.append(" ".join(piece))
            ids.append(f"faq{i}_c{j}")
            metas.append({"question": row["question"], "answer": row["answer"]})
    return chunks, ids, metas


# %% 5. Embed + store in Chroma (default model: 384-dim MiniLM)
def build_collection(chunks, ids, metas):
    db = chromadb.Client()
    col = db.create_collection("faqs")
    col.add(documents=chunks, ids=ids, metadatas=metas)
    return col


# %% 6. Query -> top 3
def search(col, query, k=3):
    hits = col.query(query_texts=[query], n_results=k)
    print(f"\nQuery: {query}")
    for rank, (meta, dist) in enumerate(
        zip(hits["metadatas"][0], hits["distances"][0]), 1
    ):
        print(f"  {rank}. {meta['question']}  (distance {dist:.3f})")
        print(f"     -> {meta['answer']}")


def main():
    raw = load_data()
    print("Raw shape:", raw.shape)
    df = clean_data(raw)
    print("Clean shape:", df.shape)
    print("Answer length stats:", length_stats(df))
    col = build_collection(*build_chunks(df))
    for q in [
        "I can't sign in",
        "I want my money back",
        "when does my plan renew",
        "how do I talk to a human",
    ]:
        search(col, q)


if __name__ == "__main__":
    main()
