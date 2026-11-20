from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

FEATURES = ["product_code", "day_of_week", "day_of_month", "month", "day_of_year", "is_weekend", "lag_1", "lag_2", "lag_7", "lag_14", "rolling_mean_7", "rolling_mean_14"]

def validate_sales(df: pd.DataFrame) -> pd.DataFrame:
    required = {"date", "product_id", "sales"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError("CSV must contain columns: date, product_id, sales. Missing: " + ", ".join(sorted(missing)))
    out = df[["date", "product_id", "sales"]].copy()
    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    out["sales"] = pd.to_numeric(out["sales"], errors="coerce")
    out["product_id"] = out["product_id"].astype(str)
    out = out.dropna(subset=["date", "sales", "product_id"])
    out = out[out["sales"] >= 0]
    out = out.groupby(["date", "product_id"], as_index=False)["sales"].sum()
    out = out.sort_values(["product_id", "date"]).reset_index(drop=True)
    if len(out) < 100:
        raise ValueError("Please provide at least 100 valid daily product records.")
    return out

def make_features(df: pd.DataFrame) -> pd.DataFrame:
    pieces=[]
    products=sorted(df.product_id.unique())
    product_codes={p:i for i,p in enumerate(products)}
    for p,g in df.groupby("product_id", sort=False):
        g=g.sort_values("date").copy()
        g["product_code"]=product_codes[p]
        g["day_of_week"]=g.date.dt.dayofweek
        g["day_of_month"]=g.date.dt.day
        g["month"]=g.date.dt.month
        g["day_of_year"]=g.date.dt.dayofyear
        g["is_weekend"]=(g.date.dt.dayofweek>=5).astype(int)
        for lag in [1,2,7,14]: g[f"lag_{lag}"]=g.sales.shift(lag)
        g["rolling_mean_7"]=g.sales.shift(1).rolling(7).mean()
        g["rolling_mean_14"]=g.sales.shift(1).rolling(14).mean()
        pieces.append(g)
    return pd.concat(pieces).dropna(subset=FEATURES+["sales"]).sort_values("date").reset_index(drop=True)

def fit_and_evaluate(raw: pd.DataFrame, n_estimators: int=180):
    data=validate_sales(raw)
    featured=make_features(data)
    # Hold out the latest 7 calendar days for every product: time-aware validation.
    cutoff=data.date.max()-pd.Timedelta(days=6)
    train=featured[featured.date < cutoff]
    test=featured[featured.date >= cutoff]
    if len(train)<50 or len(test)<5:
        raise ValueError("Not enough history for a 7-day chronological test. Add more historical dates.")
    model=RandomForestRegressor(n_estimators=n_estimators, min_samples_leaf=2, max_features=0.9, random_state=42, n_jobs=-1)
    model.fit(train[FEATURES], train.sales)
    pred=np.maximum(0, model.predict(test[FEATURES]))
    metrics={"MAE":float(mean_absolute_error(test.sales,pred)),"RMSE":float(np.sqrt(mean_squared_error(test.sales,pred))),"R2":float(r2_score(test.sales,pred)) if test.sales.nunique()>1 else float('nan'),"test_rows":int(len(test)),"train_rows":int(len(train))}
    comparison=test[["date","product_id","sales"]].copy().rename(columns={"sales":"actual_sales"})
    comparison["predicted_sales"]=pred
    # Permutation importance is a model-agnostic global explanation, calculated on holdout data.
    sample=test if len(test)<=2500 else test.sample(2500, random_state=42)
    perm=permutation_importance(model,sample[FEATURES],sample.sales,n_repeats=5,random_state=42,n_jobs=-1,scoring="neg_mean_absolute_error")
    importance=pd.DataFrame({"feature":FEATURES,"importance":perm.importances_mean}).sort_values("importance",ascending=False)
    return model, metrics, comparison, importance, data

def forecast_next_days(model, history: pd.DataFrame, horizon: int=7) -> pd.DataFrame:
    data=validate_sales(history)
    products=sorted(data.product_id.unique())
    product_codes={p:i for i,p in enumerate(products)}
    results=[]
    for p in products:
        g=data[data.product_id==p].sort_values("date")
        dates=list(g.date)
        vals=list(g.sales.astype(float))
        if len(vals)<15: continue
        for _ in range(horizon):
            next_date=dates[-1]+pd.Timedelta(days=1)
            arr=np.asarray(vals,dtype=float)
            row={"product_code":product_codes[p],"day_of_week":next_date.dayofweek,"day_of_month":next_date.day,"month":next_date.month,"day_of_year":next_date.dayofyear,"is_weekend":int(next_date.dayofweek>=5),"lag_1":arr[-1],"lag_2":arr[-2],"lag_7":arr[-7],"lag_14":arr[-14],"rolling_mean_7":float(arr[-7:].mean()),"rolling_mean_14":float(arr[-14:].mean())}
            y=max(0.0,float(model.predict(pd.DataFrame([row])[FEATURES])[0]))
            dates.append(next_date); vals.append(y)
            results.append({"date":next_date,"product_id":p,"predicted_sales":round(y,2)})
    return pd.DataFrame(results)

def explain_one_prediction(model, history: pd.DataFrame, product_id: str, horizon: int=1):
    """Return transparent local feature perturbations around the latest forecast row.
    This is a model-agnostic local sensitivity explanation, not a causal explanation.
    """
    data=validate_sales(history)
    products=sorted(data.product_id.unique()); codes={p:i for i,p in enumerate(products)}
    g=data[data.product_id==str(product_id)].sort_values("date")
    if len(g)<15: return pd.DataFrame(columns=["feature","impact"])
    dates=list(g.date); vals=list(g.sales.astype(float)); row=None
    for _ in range(horizon):
        nd=dates[-1]+pd.Timedelta(days=1); a=np.asarray(vals)
        row={"product_code":codes[str(product_id)],"day_of_week":nd.dayofweek,"day_of_month":nd.day,"month":nd.month,"day_of_year":nd.dayofyear,"is_weekend":int(nd.dayofweek>=5),"lag_1":a[-1],"lag_2":a[-2],"lag_7":a[-7],"lag_14":a[-14],"rolling_mean_7":float(a[-7:].mean()),"rolling_mean_14":float(a[-14:].mean())}
        y=max(0.0,float(model.predict(pd.DataFrame([row])[FEATURES])[0])); dates.append(nd); vals.append(y)
    base=float(model.predict(pd.DataFrame([row])[FEATURES])[0])
    impacts=[]
    for f in FEATURES:
        changed=dict(row)
        if f in ["lag_1","lag_2","lag_7","lag_14","rolling_mean_7","rolling_mean_14"]:
            changed[f]=float(changed[f])*1.10
        elif f=="is_weekend": changed[f]=1-int(changed[f])
        else: continue
        delta=float(model.predict(pd.DataFrame([changed])[FEATURES])[0])-base
        impacts.append({"feature":f,"impact":delta})
    return pd.DataFrame(impacts).sort_values("impact",key=lambda s:s.abs(),ascending=False)
