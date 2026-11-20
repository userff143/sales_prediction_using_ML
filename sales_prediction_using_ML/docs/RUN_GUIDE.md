# Detailed Run Instructions (Windows 10/11)

## A. Install Python
1. Open https://www.python.org/downloads/ .
2. Download Python 3.11.x for Windows.
3. Run the installer.
4. IMPORTANT: tick **Add python.exe to PATH** at the bottom of the first installer screen.
5. Click Install Now and wait for completion.
6. Open Command Prompt and check: `py --version`. It should display Python 3.11.x.

## B. Extract and open the project
1. Download `sales_prediction_using_ML.zip`.
2. Right-click it → **Extract All**.
3. Open the extracted folder named `sales_prediction_using_ML`.
4. Confirm you can see `app.py`, `requirements.txt`, `data`, `src`, and `docs`.
5. In VS Code, choose File → Open Folder and select this folder. Or use PyCharm → Open.

## C. Open a terminal in the correct folder
- VS Code: Terminal → New Terminal.
- PyCharm: View → Tool Windows → Terminal.
- The terminal path must end with `sales_prediction_using_ML`.
- Check by running `dir`. You should see `app.py`.

## D. Create an isolated Python environment
Run:
```bat
py -3.11 -m venv .venv
```
This creates a `.venv` folder so the project's packages do not interfere with other Python projects.

Activate it:
```bat
.venv\Scripts\activate
```
If activation is successful, `(.venv)` appears at the start of the terminal line.

If PowerShell blocks activation, either use Command Prompt terminal or run this once in PowerShell for the current user:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
Then close and reopen the terminal and activate again.

## E. Install packages
Run these commands one by one:
```bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```
Wait until installation completes. Do not close the terminal during installation.

## F. Start the dashboard
Run:
```bat
streamlit run app.py
```
Streamlit prints a local URL, usually `http://localhost:8501`. Ctrl+click the URL or copy it into Chrome/Edge.
Keep the terminal open while using the dashboard. To stop the app, click the terminal and press Ctrl+C.

## G. Use the dashboard
1. The sample dataset loads automatically from `data/sample_sales_17000.csv`.
2. Sidebar slider chooses a 3–7 day forecast horizon.
3. Select a product from the dropdown to see its recent sales and forecast.
4. Review the historical daily total-sales chart.
5. Review MAE, RMSE and R². These metrics are calculated on the latest seven days held out chronologically.
6. Review actual-vs-predicted scatter and residual histogram.
7. Review global permutation feature importance.
8. Review local sensitivity for the selected product.
9. Use download buttons to export forecasts and test predictions.

## H. Upload a different CSV
1. Prepare a CSV with exactly these columns: `date`, `product_id`, `sales`.
2. Example:
```csv
date,product_id,sales
2024-01-01,ITEM_A,18
2024-01-02,ITEM_A,21
2024-01-01,ITEM_B,7
2024-01-02,ITEM_B,9
```
3. Dates must be valid. Sales must be numeric and non-negative.
4. Each product should have at least 15 daily observations. For better results, use several months or years of continuous daily history.
5. In the sidebar, click Browse files and select the CSV.
6. The dashboard validates and analyses the file in memory. It does not write it into a database.
7. If the file has several rows for the same date and product, the app sums them into daily sales.

## I. Get a real public dataset with no more than 17,000 records
Read `DATASET_GUIDE.md`. Download the Kaggle Store Item Demand Forecasting `train.csv`, then use the included subset script. The script selects eight complete store-item series (normally about 15,304 records) and writes `data/real_sales_subset.csv`. Upload that CSV in the dashboard.

## J. Free deployment using Streamlit Community Cloud
1. Create/sign in to GitHub.
2. Create a new public repository named `sales_prediction_using_ML` (or another available name).
3. Upload the project files. Do not upload `.venv` or personal files.
4. Visit https://share.streamlit.io/ and sign in with GitHub.
5. Click **Create app**.
6. Select your repository, branch (usually `main`) and main file path `app.py`.
7. Click **Deploy** and wait for build completion.
8. Share the generated Streamlit URL.

The bundled dataset is part of the repository, so the deployed app does not require a database. Free hosting quotas and policies can change; consult https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app before deployment.

## K. Common errors
- `streamlit is not recognized`: activate `.venv`, then run `pip install -r requirements.txt`.
- `No module named sklearn`: run `pip install -r requirements.txt` in the activated environment.
- `FileNotFoundError`: make sure you run `streamlit run app.py` from the project root and that the `data` folder exists.
- `CSV must contain columns...`: rename your CSV headers to `date`, `product_id`, `sales` exactly.
- Forecast missing for a product: that product needs at least 15 valid daily observations.
- Dashboard slow on first load: the Random Forest model trains when the app starts; allow it a little time.
- Port already in use: run `streamlit run app.py --server.port 8502` and open `http://localhost:8502`.

## L. Academic integrity and reporting
The bundled data is synthetic. Use the Kaggle-derived subset for your final experimental results if you need real retail sales data. Report the exact data source, selected number of rows, date range, train/test dates, model parameters and evaluation metrics. Never present synthetic-data metrics as real-world accuracy.
