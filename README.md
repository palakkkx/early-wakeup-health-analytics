# 🌅 Early Wake-Up & Health Analytics

Interactive Streamlit dashboard for exploratory analysis of the **Early Wake-Up, Exercise & Health Outcomes** dataset.

## Dataset

The notebook analysis used a dataset with:

- **10,000 records**
- **64 columns**
- Sleep and wake-up variables
- Exercise and lifestyle variables
- Wellness and health-score variables
- `Early_Waker` classification

The original analysis included Pandas-based inspection and cleaning, missing-value checks, grouping/aggregation, and visualizations such as pie charts, histograms, scatter plots, bar charts and box plots.

## Dashboard features

- Interactive filtering by gender, occupation and early-waker status
- KPI cards for records, health score, sleep duration and BMI
- Gender distribution
- Average health score by occupation
- BMI distribution
- Sleep duration vs energy level
- Sugary-drink frequency
- Exercise-type distribution
- Average daily steps by gender
- BMI correlation table
- Filtered-data explorer and CSV export

## Tech stack

- Python
- Pandas
- NumPy
- Plotly
- Streamlit

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Place the dataset at:

```text
data/early_wakeup_health_dataset.csv
```

## Deployment

This project can be deployed through Streamlit Community Cloud from the GitHub repository.

## Resume description

**Early Wake-Up & Health Analytics Dashboard** | Python, Pandas, Plotly, Streamlit

- Analyzed **10,000 health and lifestyle records across 64 features** covering sleep, exercise, nutrition and wellness indicators.
- Performed data cleaning, missing-value analysis, grouping/aggregation and exploratory data analysis using Pandas and NumPy.
- Built an interactive Streamlit dashboard with filters, KPI metrics, Plotly visualizations and downloadable filtered data.

> Note: The dataset is used for exploratory analysis. Dashboard relationships should not be interpreted as medical or causal conclusions.
