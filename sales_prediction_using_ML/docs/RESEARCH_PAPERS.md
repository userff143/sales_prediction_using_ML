# Research Papers for Sales Prediction Using Machine Learning

Listed in descending publication year. These papers are relevant background; they do not imply that this project reproduces their methods or reported results.

## 2025

### 1. Sales Forecasting and Demand Prediction Through Time Series Analysis and Machine Learning (2025)
- Authors: Nagalakshmi M.V.N. et al.
- Published: 6 October 2025
- DOI: https://doi.org/10.12732/ijam.v38i6s.656
- Link: https://ijamjournal.org/ijam/publication/index.php/ijam/article/view/656
- Relevance: Discusses time-series forecasting and compares classical forecasting with machine-learning/deep-learning approaches, using rolling-origin evaluation. Useful for explaining why temporal validation matters.

### 2. Forecasting Retail Sales using Machine Learning Models (2025)
- Authors: Oluwasola Oluwaseun Mustapha and Terry Sithole
- Published: 19 April 2025
- DOI: https://doi.org/10.47672/ajsas.2679
- Link: https://ajpojournals.org/journals/AJSAS/article/view/2679
- Relevance: Recent retail sales forecasting research that can support the problem statement and literature review. Check the full paper for its exact data, models and evaluation details.

### 3. Sales Forecasting for Retail Stores Using Hybrid Neural Networks and Sales-Affecting Variables (2025)
- Published: 11 September 2025
- DOI: https://doi.org/10.7717/peerj-cs.3058
- Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC12453866/
- Relevance: Studies retail forecasting with CNN-LSTM and external factors such as holidays, weather and salary days. Useful comparison for future enhancement; this project deliberately uses a smaller, simpler tabular ML model.

## 2024

### 4. Hybrid Convolutional Long Short-Term Memory Models for Sales Forecasting in Retail (2024)
- First published: 13 February 2024
- DOI: https://doi.org/10.1002/for.3073
- Link: https://onlinelibrary.wiley.com/doi/10.1002/for.3073
- Relevance: Proposes CNN-LSTM hybrid architectures for retail sales forecasting. Useful for discussing deep-learning alternatives to Random Forest.

### 5. A Demand Forecasting System of Product Categories Defined by Their Time Series Using a Hybrid Approach of Ensemble Learning with Feature Engineering (2024)
- Authors: Santiago Mejía and Jose Aguilar
- Published: 2 September 2024
- DOI: https://doi.org/10.1007/s00607-024-01320-y
- Link: https://link.springer.com/article/10.1007/s00607-024-01320-y
- Relevance: Uses time-series feature engineering, product grouping and ensemble learning. Closely related to lag/rolling features used in this project.

### 6. Which Product Description Phrases Affect Sales Forecasting? An Explainable AI Framework by Integrating WaveNet Neural Network Models with Multiple Regression (2024 issue; DOI registered 2023)
- Journal: Decision Support Systems, Volume 176, January 2024
- DOI: https://doi.org/10.1016/j.dss.2023.114065
- Link: https://www.sciencedirect.com/science/article/pii/S0167923623001409
- Relevance: Combines sales forecasting and SHAP explanations. Useful as XAI literature, although it explains text/product-description features rather than the lag-based features in this project.

## 2023

### 7. Applying Machine Learning in Retail Demand Prediction—A Comparison of Tree-Based Ensembles and Long Short-Term Memory-Based Deep Learning (2023)
- Authors: Mehran Nasseri, Taha Falatouri, Patrick Brandtner and Farzaneh Darbanian
- Published: 9 October 2023
- DOI: https://doi.org/10.3390/app131911112
- Link: https://www.mdpi.com/2076-3417/13/19/11112
- Relevance: Compares tree-based ensemble models including Random Forest with LSTM for retail demand prediction. Supports the choice of a tree ensemble as a practical baseline.

### 8. Interpreting Direct Sales’ Demand Forecasts Using SHAP Values (2023)
- Authors: Mariana Arboleda-Florez and Carlos Castro-Zuluaga
- DOI: https://doi.org/10.1590/0103-6513.20220035
- Link: https://www.scienceopen.com/document?vid=ed093bd3-a6be-4f8d-82c6-675a174192fc
- Relevance: Applies SHAP to interpret demand forecasts and explains why interpretability matters when introducing ML into forecasting workflows.

## 2022

### 9. A Comparative Study of Demand Forecasting Models for a Multi-Channel Retail Company: A Novel Hybrid Machine Learning Approach (2022)
- Authors: Arnab Mitra, Arnav Jain, Avinash Kishore and Pravin Kumar
- Published: 27 September 2022
- DOI: https://doi.org/10.1007/s43069-022-00166-4
- Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC9514716/
- Relevance: Compares Random Forest, XGBoost, Gradient Boosting, AdaBoost and neural networks for retail demand forecasting. Useful for the model-selection discussion.

### 10. Retail Sales Forecast Based on Machine Learning Methods (2022 conference; indexed 2023)
- Published at 2022 6th Annual International Conference on Data Science and Business Analytics
- DOI: https://doi.org/10.1109/ICDSBA57203.2022.00030
- Link: https://ieeexplore.ieee.org/document/10129443/
- Relevance: Uses Walmart weekly sales and Random Forest regression. Relevant to tree-based sales forecasting.

## How to use these papers in your report
1. Use 2025–2022 papers in the literature survey, newest first.
2. For each paper, record the exact dataset, forecasting horizon, algorithms, metrics and limitations from its full text.
3. Do not copy reported accuracy values as your own results.
4. Cite each paper in your institution's required format (IEEE/APA/Harvard).
5. The project implementation uses Random Forest, chronological holdout, MAE/RMSE/R², permutation importance and local sensitivity. It does not currently implement LSTM, CNN, SHAP or the papers' hybrid methods.
