# Supermarket Sales Analysis with AI

A complete beginner-friendly Data Analytics project aligned to the AICTE | IBM SkillsBuild Data Analytics with AI internship theme. The supplied internship resource names the Masterclass 4 workbook **“Supermarket Sales Analysis DA project”**. This implementation turns that topic into a runnable Streamlit dashboard with data cleaning, exploratory analytics, anomaly detection, customer segmentation, and business insights.

## Project objective

Analyze supermarket transaction data to understand sales trends, branch performance, product performance, customer behavior, payment preferences, and unusual transactions, then convert those findings into business-oriented insights.

## Features

- Data validation and cleaning
- Duplicate removal and missing-value treatment
- Sales KPIs
- Daily sales trend
- Branch and product-line analysis
- Customer analytics
- Payment-method analysis
- Isolation Forest anomaly detection
- K-Means customer segmentation scaffold
- AI-style business insights generated from model/analytics outputs
- CSV download of the cleaned, filtered data
- Responsive Streamlit dashboard

## Folder structure

```text
supermarket_sales_ai_project/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── generate_data.py
│   └── supermarket_sales.csv
├── src/
│   ├── preprocessing.py
│   └── ai_models.py
└── docs/
    ├── project_report.md
    ├── presentation.md
    └── viva_questions.md
```

## How to run

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Open the local Streamlit URL shown in the terminal.

## Dataset note

The provided internship PDF lists the workbook/resource name but does **not** include the workbook's data columns or its actual CSV contents. Therefore this package includes a locally generated demonstration dataset with the same supermarket-sales problem framing. For final submission, replace `data/supermarket_sales.csv` with the official internship dataset if your mentor provided it, while keeping the same or mapped column names.

## Recommended final submission artifacts

1. GitHub repository containing this project.
2. Screenshots of the dashboard.
3. `docs/project_report.md` converted to PDF/Word if your institute requires it.
4. `docs/presentation.md` converted into a PPT.
5. IBM SkillsBuild certificate as the internship's stated Deliverable 1.

The internship guide states that IBM SkillsBuild self-paced learning is Deliverable 1 and that students were instructed to upload the e-certificate. fileciteturn0file0L18-L25
