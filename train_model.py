import pandas as pd
from xgboost import XGBRegressor
import pickle
import os

# ---------------- CREATE MODEL FOLDER ----------------
os.makedirs("model", exist_ok=True)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/train.csv")

# ---------------- SELECT FEATURES ----------------
X = df[['OverallQual', 'GrLivArea', 'GarageCars']]
y = df['SalePrice']

# ---------------- TRAIN MODEL ----------------
model = XGBRegressor()
model.fit(X, y)

# ---------------- SAVE MODEL ----------------
model_path = os.path.join("model", "model.pkl")

with open(model_path, "wb") as f:
    pickle.dump(model, f)

# ---------------- SUCCESS MESSAGE ----------------
print("✅ Model trained and saved successfully!")