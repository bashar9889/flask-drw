import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time


# Function to get coordinates
def get_coordinates(address, geolocator):
    try:
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
        return (None, None)
    except (GeocoderTimedOut, GeocoderServiceError):
        return (None, None)


# Load the Excel file
file_path = 'Book2.xlsx'  # Replace with the path to your Excel file
addresses_df = pd.read_excel(file_path)

# Initialize the geocoder
geolocator = Nominatim(user_agent="coordinate_finder")

# Create new columns for latitude and longitude
addresses_df['Latitude'] = None
addresses_df['Longitude'] = None

# Iterate over the addresses and fetch their coordinates
for index, row in addresses_df.iterrows():
    # Combine the area and address for geocoding
    full_address = f"{row['region']} {row['address']}"
    coordinates = get_coordinates(full_address, geolocator)

    addresses_df.at[index, 'Latitude'] = coordinates[0]
    addresses_df.at[index, 'Longitude'] = coordinates[1]

    # Sleep to throttle requests
    time.sleep(1)

# Save the updated dataframe back to an Excel file
output_file_path = 'updated_addresses_with_coordinates8.xlsx'
addresses_df.to_excel(output_file_path, index=False)







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
file_path = 'Book2.xlsx'  # Replace with the path to your Excel file
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
output_file_path = 'updated_coordinates_with_area.xlsx'
coordinates_df.to_excel(output_file_path, index=False)