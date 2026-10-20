import pandas as pd
import numpy as np


def get_scores(df):
    return df["Score"].to_numpy(dtype=float)


def average_score(scores):
    return np.mean(scores)


def highest_score(scores):
    return np.max(scores)


def lowest_score(scores):
    return np.min(scores)


def total_score(scores):
    return np.sum(scores)


def pass_rate(scores):
    passing_scores = scores >= 50
    return average_score(passing_scores) * 100


def cleanup(path):
    try:
        df = pd.read_csv(path)
    except Exception as e:
        print("Error during file importing: ", str(e))
        return

    df = df.copy()

    df["Name"] = df["Name"].str.strip()

    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    df["Score"] = pd.to_numeric(df["Score"], errors="coerce")

    df = df.dropna(subset=["Name", "Age", "Score"])

    df = df[df["Age"].between(5, 100) & df["Score"].between(0, 100)]

    df = df.drop_duplicates()

    df["Age"] = df["Age"].astype(int)

    return df.reset_index(drop=True)


if __name__ == "__main__":
    df = cleanup("./data/students.csv")

    if df is None or df.empty:
        print("No valid records to process.")
    else:
        scores = get_scores(df)

        print("===== STUDENT SCORE REPORT =====")
        print(df, "\n")
        print("Number of valid students:", len(scores))
        print("Average score:", average_score(scores))
        print("Highest score:", highest_score(scores))
        print("Lowest score:", lowest_score(scores))
        print("Total score:", total_score(scores))
        print(f"Pass rate: {pass_rate(scores):.1f}%")
