#These comments are for me to understand the context of the file, whilst learning to write my first FastApi.
# This is the main file of the FastAPI application. It loads a pre-trained XGBoost model and defines endpoints for predicting customer churn based on input data.
import pandas as pd
import joblib
from fastapi import FastAPI
from pydantic import BaseModel
# Load the pre-trained XGBoost model
model = joblib.load('models/best_model_xgboost.pkl')

# Initialize FastAPI app
app = FastAPI(title="Churn Prediction API")

# Define the input data model wich is based on the features used in the model aka X_train columns
class CustomerData(BaseModel):
    Tenure: float
    CityTier: int
    WarehouseToHome: float
    HourSpendOnApp: float
    NumberOfDeviceRegistered: int
    SatisfactionScore: int
    NumberOfAddress: int
    Complain: int
    OrderAmountHikeFromlastYear: float
    CouponUsed: int
    OrderCount: int
    DaySinceLastOrder: float
    CashbackAmount: float

    PreferredLoginDevice_Mobile_Phone: int
    PreferredLoginDevice_Phone: int
    PreferredPaymentMode_COD: int
    PreferredPaymentMode_Cash_on_Delivery: int
    PreferredPaymentMode_Credit_Card: int
    PreferredPaymentMode_Debit_Card: int
    PreferredPaymentMode_E_wallet: int
    PreferredPaymentMode_UPI: int
    Gender_Male: int
    PreferedOrderCat_Grocery: int
    PreferedOrderCat_Laptop_and_Accessory: int
    PreferedOrderCat_Mobile: int
    PreferedOrderCat_Mobile_Phone: int
    PreferedOrderCat_Others: int
    MaritalStatus_Married: int
    MaritalStatus_Single: int
@app.get("/")
def home(): # Health check endpoint
    return {"message": "Churn API is running!"}

# Define the prediction endpoint
@app.post("/predict")
def predict_churn(data: CustomerData):
    # 1. Convert the input data to a DataFrame
    input_df = pd.DataFrame([data.model_dump()])
    
    # 2. Creating the existing engineered features
    input_df['DissatisfactionIndex'] = input_df['Complain'] / (input_df['OrderCount'] + 1) * (5 - input_df['SatisfactionScore'])
    
    input_df['DeviceToTenureRatio'] = input_df['NumberOfDeviceRegistered'] / (input_df['Tenure'] +1)
    
    input_df['InactivityRatio'] = input_df['DaySinceLastOrder'] / (input_df['Tenure'] + 1)
    
    input_df['RecencyWeight'] = input_df['OrderCount'] / (input_df['DaySinceLastOrder'] + 1)
    
    input_df['SpendVelocity'] = input_df['OrderAmountHikeFromlastYear'] / (input_df['DaySinceLastOrder'] + 1)

    
    # 3. Make predictions
    prediction = model.predict(input_df)           # 0 or 1
    probability = model.predict_proba(input_df)    # Probability %
    
    # 4. Return the prediction and probability
    return {
        "churn_prediction": int(prediction[0]),
        "churn_probability": float(probability[0][1]),
        "risk_level": "High" if probability[0][1] > 0.5 else "Low"
    }