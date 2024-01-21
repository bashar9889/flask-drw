from flask import Flask, request, jsonify
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import joblib  # for loading the model
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from math import radians, cos, sin, asin, sqrt
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Function to calculate the distance between two points using the Haversine formula
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # Haversine formula
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371  # Radius of Earth in kilometers
    return c * r

# Function to get coordinates
def get_coordinates(address, geolocator):
    try:
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
        return (None, None)
    except (GeocoderTimedOut, GeocoderServiceError):
        return (None, None)

# Initialize the geolocator
geolocator = Nominatim(user_agent="coordinate_finder")

# Load your trained models and scaler
dt_classifier = joblib.load('dt_model.pkl')
mlp_classifier = joblib.load('mlp_model.pkl')
scaler = joblib.load('scaler.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    price = float(data['price'])
    location = data['location']

    # Convert location to coordinates
    coordinates = get_coordinates(location, geolocator)
    time.sleep(1)  # To prevent hitting request limit

    if coordinates[0] is not None and coordinates[1] is not None:
        # Create a DataFrame for the input features
        input_df = pd.DataFrame([[price, coordinates[0], coordinates[1]]],
                                columns=['price', 'Latitude', 'Longitude'])  # Ensure these column names match those used in training

        # Preprocess the input
        input_features = scaler.transform(input_df)

        result = "Unavailable"
        # Preprocess the input
        #input_features = scaler.transform([[price, float(coordinates[0]), float(coordinates[1])]])
        

        # Make predictions using both models
        dt_prediction = dt_classifier.predict(input_features)
        mlp_prediction = mlp_classifier.predict(input_features)

        # Assuming binary classification with labels [0, 1] for ['Bad', 'Good']
        result = "Good" if dt_prediction[0] == 1 else "Bad"
    response = jsonify({"prediction": result})
    print("Sending response:", response.get_data(as_text=True))  # Log the response
    return response
        

if __name__ == '__main__':
    app.run(debug=True)
