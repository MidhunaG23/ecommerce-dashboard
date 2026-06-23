# E-Commerce Analytics Dashboard

A production-style Streamlit dashboard that works with any sales-style
CSV or Excel file, not just one fixed dataset. It automatically detects
which columns represent dates, sales, profit, category, product, customer,
and region, then adapts every KPI, chart, and filter to whatever is
actually present in the uploaded file.

## Features

- Upload any CSV/Excel file with sales-style data
- Automatic, name-based + dtype-fallback column detection
- Manual column-mapping override when auto-detection is wrong
- Built-in sample dataset for instant exploration (no upload needed)
- KPI cards: Sales, Profit, Orders, Margin (adaptive to available columns)
- Multi-page dashboard: Overview, Product Analysis, Customer Analysis,
  Reports, About
- Dynamic filters: category, region, date range, product, global search
- Interactive Plotly charts: bar, pie, line, horizontal top-N
- Graceful error handling: empty files, bad formats, missing columns,
  zero-row results after filtering. The app never crashes, it explains.
- CSV export of filtered data
- Data quality summary (missing values, row/column counts)

## Folder Structure

ecommerce_dashboard/
- app.py - Main entry point
- requirements.txt
- README.md
- utils/
  - data_loader.py - Safe file loading and validation
  - column_detector.py - Auto-detects column roles
  - sample_data.py - Generates demo dataset
  - helpers.py - Shared small utilities
- components/
  - filters.py - Sidebar filters and column mapping UI
  - kpi.py - KPI metric cards
  - charts.py - Plotly chart builders
- pages_content/
  - dashboard.py - Overview page
  - product_analysis.py
  - customer_analysis.py
  - reports.py
  - about.py

## Setup

Install dependencies and run:

    pip install -r requirements.txt
    streamlit run app.py

## How It Works

1. Upload or toggle sample data - the app needs a dataframe to start.
2. Column detection (utils/column_detector.py) scans column names against
   keyword lists (e.g. "sales", "revenue", "amount" maps to the sales
   role) and falls back to picking the largest numeric column or a
   sensible categorical column if name-matching fails.
3. Manual override - if detection is wrong, the user can remap any role
   via the "Column Mapping (Advanced)" sidebar expander.
4. Minimum viability check - the app needs at least one numeric metric
   (Sales or Profit) and one dimension (Category or Product) to build a
   dashboard. If that's not met, it shows a friendly warning instead of
   crashing.
5. Filters and pages then operate only on roles that were actually
   detected. A dataset without a Region column simply won't show a
   Region filter or chart, instead of throwing an error.

## Supported File Types

- .csv
- .xlsx / .xls

## Notes on Extending

- Add a new chart: drop a new function into components/charts.py and
  call it from the relevant page in pages_content/.
- Add a new page: create a module in pages_content/ with a render()
  function, then register it in the sidebar radio and routing block in
  app.py.
- Add a new detectable column role: add a keyword list entry to
  KEYWORDS in utils/column_detector.py and a corresponding label in
  render_column_mapping_editor in components/filters.py.
