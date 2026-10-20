# Week 3 — Advanced Data Analysis and Visualization in Logistics

**Project:** Logistics Performance & Delivery Analytics using Python  
**Hypothetical organization:** FastTrack Logistics Pvt. Ltd.  
**Dataset:** 300 simulated shipment records. This is synthetic data for educational use, not real company data.

## Project contents
- `Week3_Advanced_Logistics_Analysis_Report.docx` — formatted report with EDA, seven embedded charts, interpretations, and recommendations.
- `data/hypothetical_logistics_dataset.csv` — raw simulated dataset.
- `src/analyze_logistics.py` — data cleaning, descriptive statistics, correlation analysis, and chart generation.
- `dashboard.py` — interactive Streamlit dashboard with filters, KPI cards, Plotly charts, summary table, and CSV download.
- `outputs/` — cleaned data, charts, and CSV summary tables.
- `requirements.txt` — dependencies.

## Setup (Windows / VS Code)
1. Extract the ZIP and open the extracted folder in VS Code.
2. Open Terminal in the project folder.
3. Create and activate a virtual environment (optional but recommended):
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
4. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```

## Run the analysis
From the project root:
```powershell
python src/analyze_logistics.py
```
Charts are saved to `outputs/charts/` and summary tables to `outputs/tables/`.

## Run the interactive dashboard
From the project root:
```powershell
streamlit run dashboard.py
```
Streamlit will show a local address in the terminal; open it in your browser. Use the sidebar filters to select region, transport mode, and shipment type. The dashboard can export the filtered records as a CSV.

## Main analysis topics
- Missing values and duplicate shipment IDs
- Mean, median, spread, and distributions
- Delivery time, shipment volume, distance, weight, and cost
- Correlation matrix
- Cost comparison by transport mode
- Delivery-time comparison by region
- On-time delivery rate by mode
- Daily transportation cost trend (7-day rolling average)

## Important notes
- All records are simulated.
- Cost is represented in Indian rupees (INR).
- `on_time` is true when actual delivery days are less than or equal to promised delivery days.
- Correlation indicates association, not causation.
