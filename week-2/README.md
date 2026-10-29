# Week 2 – Mini Semantic Search

Semantic search over a 28-question FAQ: Pandas (load + clean) → chunk → embed → Chroma → top 3 matches.

## Setup (virtual environment)

```bash
python -m venv venv
venv\Scripts\activate        # Windows  (Mac/Linux: source venv/bin/activate)
pip install -r ../requirements.txt
```

`venv/` is ignored via `.gitignore`.

## Run

```bash
cd week-02
python mini_semantic_search.py
```

Or open `mini_semantic_search.ipynb` in Google Colab: <PASTE COLAB LINK>

## Example queries

- `I can't sign in` → Why can't I log in?
- `I want my money back` → How can I get a refund?
- `when does my plan renew` → When will my subscription renew?
- `how do I talk to a human` → How do I contact customer support?
