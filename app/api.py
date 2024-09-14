from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import os
# Load the saved model
app = FastAPI()

model = joblib.load('model.joblib')


# Allow requests from the frontend (Next.js) to access the FastAPI backend
origins = [
    "http://localhost:3000",  # Replace with your Next.js app's URL
    "http://127.0.0.1:3000",
    "https://teslapredictionapi.vercel.app"
]
# teslapredictionapi

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from your frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Initialize FastAPI app

# Define a Pydantic model for input validation
class CarInput(BaseModel):
    year: int
    model: str
    color: str
    miles: int
    trim: str
    interior: str
    wheels: str
    features: str
    country: str
    location: str
    state: str

# Load dataset (use your actual path)
dataset_path = os.path.join(os.path.dirname(__file__), 'tesla_used_car_sold-2022-08.csv')

@app.get("/form-options/")
def get_form_options():
    try:
        # Load dataset
        df = pd.read_csv(dataset_path)

        # Fill NaN values with a default or placeholder value
        df.fillna('Unknown', inplace=True)

        # Get unique values for each field and return them
        return {
            "years": df['year'].dropna().unique().tolist(),
            "models": df['model'].dropna().unique().tolist(),
            "colors": df['color'].dropna().unique().tolist(),
            "interiors": df['interior'].dropna().unique().tolist(),
            "trims": df['trim'].dropna().unique().tolist(),
            "wheels": df['wheels'].dropna().unique().tolist(),
            "features": df['features'].dropna().unique().tolist(),
            "countries": df['country'].dropna().unique().tolist(),
            "locations": df['location'].dropna().unique().tolist(),
            "states": df['state'].dropna().unique().tolist(),
        }
    except Exception as e:
        # Log the error and raise an HTTP error for better debugging
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@app.post("/predict/")
def predict_price(input_data: CarInput):
    # Convert input data to a DataFrame
    input_dict = input_data.dict()
    df = pd.DataFrame([input_dict])
    
    # Predict the price
    try:
        prediction = model.predict(df)
        return {"predicted_price": f"${prediction[0]:,.2f}"}
    except Exception as e:
        return {"error": str(e)}

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Tesla Price Prediction API!"}



