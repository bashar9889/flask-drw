import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time


# Function to get area name from coordinates
def get_area_name(latitude, longitude, geolocator):
    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        if location:
            return location.raw['address'].get('suburb', None)
        return None
    except (GeocoderTimedOut, GeocoderServiceError):
        return None


# Load the Excel file
file_path = 'Book3.xlsx'  # Replace with the path to your Excel file
coordinates_df = pd.read_excel(file_path)

# Initialize the geocoder
geolocator = Nominatim(user_agent="area_finder")

# Create a new column for area name
coordinates_df['Area'] = None

# Iterate over the coordinates and fetch their area names
for index, row in coordinates_df.iterrows():
    latitude = row['Latitude']
    longitude = row['Longitude']
    area_name = get_area_name(latitude, longitude, geolocator)

    coordinates_df.at[index, 'Area'] = area_name

    # Sleep to throttle requests
    time.sleep(1)

# Save the updated dataframe back to an Excel file
output_file_path = 'updated_coordinates_with_area1.xlsx'
coordinates_df.to_excel(output_file_path, index=False)


