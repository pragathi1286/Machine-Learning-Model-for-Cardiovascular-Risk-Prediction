import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import resample
import joblib
import os

# Load dataset
df = pd.read_csv("framingham.csv")
df = df.dropna().reset_index(drop=True)
df["education"] = df["education"].astype(str)

# Features and target
X = df.drop("TenYearCHD", axis=1)
y = df["TenYearCHD"]

# Balance dataset
X["TenYearCHD"] = y
majority = X[X.TenYearCHD == 0]
minority = X[X.TenYearCHD == 1]
minority_upsampled = resample(minority, replace=True, n_samples=len(majority), random_state=42)
df_balanced = pd.concat([majority, minority_upsampled])
y = df_balanced["TenYearCHD"]
X = df_balanced.drop("TenYearCHD", axis=1)

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocessor
numeric = ["age", "cigsPerDay", "totChol", "sysBP", "diaBP", "BMI", "heartRate", "glucose"]
categorical = ["education", "male", "currentSmoker", "BPMeds", "prevalentStroke", "prevalentHyp", "diabetes"]

numeric_transformer = Pipeline(steps=[("scaler", StandardScaler())])
categorical_transformer = Pipeline(steps=[("encoder", OneHotEncoder(handle_unknown="ignore"))])
preprocessor = ColumnTransformer(
    transformers=[("num", numeric_transformer, numeric),
                  ("cat", categorical_transformer, categorical)]
)

# Model
rf = RandomForestClassifier(
    n_estimators=400,
    max_depth=10,
    random_state=42,
    class_weight="balanced"
)

# Pipeline
pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", rf)])
pipeline.fit(X_train, y_train)

# Evaluate
acc = pipeline.score(X_test, y_test)
print(f"✅ Model Trained Successfully. Accuracy: {acc:.2f}")

# Save model and preprocessor
os.makedirs("model", exist_ok=True)
joblib.dump(rf, "model/best_model.pkl")
joblib.dump(preprocessor, "model/preprocessor.pkl")
print("📦 Model and Preprocessor saved in /model/")
