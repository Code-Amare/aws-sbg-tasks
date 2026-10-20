# Week 01: Student Score Data Processing

## Overview

This project loads a raw student dataset from a CSV file, cleans it with
Pandas, and calculates basic statistics on the scores with NumPy.

The CSV intentionally contains bad data (missing values, text instead of
numbers, impossible ages and scores, extra spaces, duplicates) so the
cleaning step can be demonstrated.

## Project Structure

```
week-01/
├── README.md
├── student_scores.py
├── student_scores.ipynb
└── data/
    └── students.csv
```

## How It Works

1. **Load**: read `students.csv` with Pandas.
2. **Clean**:
   - strip extra spaces from names
   - convert `Age` and `Score` to numbers (`errors="coerce"` turns invalid values into `NaN`)
   - drop rows with missing values
   - keep only ages 5-100 and scores 0-100
   - remove exact duplicate rows
3. **Process with NumPy**: convert scores to an array and calculate the
   average, highest, lowest, total, and pass rate (pass mark: 50).
4. **Report**: print a summary of the results.

## How to Run

Install the requirements:

```bash
pip install pandas numpy
```

Run the script from inside the `week-01/` folder:

```bash
python student_scores.py
```

The notebook (`student_scores.ipynb`) contains the same code with outputs
and short explanations. Upload `students.csv` to Colab before running it.

## Sample Output

```
===== STUDENT SCORE REPORT =====
Number of valid students: 8
Average score: 61.5
Highest score: 100.0
Lowest score: 0.0
Total score: 492.0
Pass rate: 62.5%
```

Out of 17 raw rows, 8 valid records remain after cleaning.

## Tools Used

- Python 3
- Pandas (loading and cleaning)
- NumPy (statistics)
- Google Colab (notebook)
