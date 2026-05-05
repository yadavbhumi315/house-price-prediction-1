import pandas as pd
from xgboost import XGBRegressor
import pickle
import os

# Ensure model folder exists
os.makedirs("model", exist_ok=True)

# Load dataset
df = pd.read_csv("data/train.csv")

# Select features
X = df[['OverallQual', 'GrLivArea', 'GarageCars']]
y = df['SalePrice']

# Train model
model = XGBRegressor()
model.fit(X, y)

# Save model
with open("model/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved successfully!")