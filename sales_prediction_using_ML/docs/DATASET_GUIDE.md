# Dataset Guide

## Bundled dataset (runs immediately)
- File: `data/sample_sales_17000.csv`
- Records: exactly 17,000
- Structure: 17 product IDs × 1,000 daily dates
- Columns: `date`, `product_id`, `sales`
- Date span: 2023-01-01 through 2025-09-26
- Type: synthetic generated data, not observed transactions
- Purpose: reproducible demonstration and application testing

## Recommended real dataset: Kaggle Store Item Demand Forecasting Challenge
Direct dataset page: https://www.kaggle.com/competitions/demand-forecasting-kernels-only/data
Competition overview: https://www.kaggle.com/competitions/demand-forecasting-kernels-only

### What is in it?
The training file contains daily unit sales for 10 stores and 50 items, with columns:
- `date`: date of sale
- `store`: store identifier
- `item`: item identifier
- `sales`: units sold that day

The original training file has about 913,000 rows, so do NOT use the full file for this project if your maximum is 17,000.

### Download instructions (browser)
1. Create a free Kaggle account or sign in.
2. Open https://www.kaggle.com/competitions/demand-forecasting-kernels-only/data .
3. Read and accept the competition rules if Kaggle asks.
4. Find `train.csv` and click Download. Kaggle may download a ZIP archive.
5. Extract the ZIP and locate `train.csv`.
6. Copy the path to `train.csv`.
7. Open a terminal in this project folder and activate your `.venv`.
8. Run (replace the example path with your actual path):
```bat
python src/prepare_kaggle_subset.py "C:\Users\YourName\Downloads\train.csv"
```
9. The script selects eight complete store-item combinations. The output is normally 15,304 records (8 × 1,913 dates) and never exceeds 17,000.
10. The generated file is `data/real_sales_subset.csv`.
11. Start the dashboard and upload `data/real_sales_subset.csv` from the sidebar.

### Dataset license / use
Kaggle competition data is governed by the competition rules. Read those terms on Kaggle before reusing or redistributing it. Do not put the downloaded raw dataset into a public GitHub repository unless its terms permit it.

## Required CSV format for any other dataset
```csv
date,product_id,sales
2024-01-01,SKU_001,10
2024-01-02,SKU_001,12
2024-01-01,SKU_002,7
```
Each row represents one product's sales on one date. If a source has multiple stores, make `product_id` unique by combining store and item identifiers (e.g. `STORE_2_ITEM_17`). The application groups duplicate date/product rows by summing sales.

## Other public source
UCI Online Retail II: https://archive.ics.uci.edu/dataset/502/online+retail+ii . It has over one million invoice-line records and requires aggregation by invoice date and stock code before sampling a maximum of 17,000 daily product records. Review its CC BY 4.0 terms and source documentation.
