import pandas as pd
from math import radians, cos, sin, asin, sqrt
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time


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

# Read the dataset
file_path = 'data2.xlsx'  # Replace with your file path
crime_df = pd.read_excel(file_path)

# Assume user's location and price are given
user_latitude = 45.5017  # For example
user_longitude = -73.5673  # For example
user_price = 450000  # For example, the price the user is considering paying

# Function to get coordinates
def get_coordinates(address, geolocator):
    try:
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
        return (None, None)
    except (GeocoderTimedOut, GeocoderServiceError):
        return (None, None)

geolocator = Nominatim(user_agent="coordinate_finder")

full_address = "Anjou 8145 Rue Bombardier"

coordinates = get_coordinates(full_address, geolocator)
time.sleep(1)


# Count the number of crimes within a 2 km radius of the user's location
crime_count = crime_df.apply(lambda row: haversine(coordinates[1], coordinates[0], row['longitude'], row['latitude']), axis=1)
crimes_within_2km = crime_count[crime_count <= 2].count()




# Split the user input address into words
address_parts = full_address.split()

# Check if the first part is 'Saint' and extract the first two words if so
if address_parts[0].lower() == 'saint' and len(address_parts) > 1 or address_parts[0].lower() == 'le' and len(address_parts) > 1:
    potential_area_name = " ".join(address_parts[:2])
else:
    potential_area_name = address_parts[0]





# List of areas from the dataset
    areas = [ "Rosemont-La Petite-Patrie",
"Ahuntsic-Cartierville",
"Anjou",
"Le Sud-Ouest",
"Griffintown",
"L'Ile Des Soeurs",
"Bizard-Sainte-Geneviève",
"Lachine",
"LaSalle",
"Le Plateau-Mont-Royal",
"Le Sud-Ouest",
"Mercier–Hochelaga-Maisonneuve",
"Mont-Royal",
"Montréal-Nord",
"Outremont",
"Pierrefonds-Roxboro",
"Rivière-des-Prairies–Pointe-aux-Trembles",
"Saint-Laurent",
"Saint-Léonard",
"Verdun",
"Ville-Marie",
"Villeray–Saint-Michel–Parc-Extension"
]




# Find the closest match to the user's input in the area list
# Here we use direct string comparison for a better match
closest_match = None
for area in areas:
    # Normalize both strings to lower case for comparison
    if potential_area_name.lower() in area.lower():
        closest_match = area
        break

print("Closest match:", closest_match)


# Assuming closest_match is not None, find the average area price
if closest_match:
    # Filter the dataframe for the matched area and calculate the average price
    avg_price_in_area = crime_df.loc[crime_df['Area'] == closest_match, 'avg price in area'].mean() if not crime_df.loc[crime_df['Area'] == closest_match, 'avg price in area'].empty else None
    print(f"The average price in the area for {closest_match} is: {avg_price_in_area}")
else:
    print("No matching area found in the dataset.")



# Get the average price for the user's area
#avg_price_in_area = avg_price_in_area

# Compare the user's price to the average price in the area
investment_decision = 'Good' if user_price < avg_price_in_area and crimes_within_2km < 10 else 'Bad'

# Output the results
print(f"Number of crimes within a 2 km radius: {crimes_within_2km}")
print(f"Average price in the area: {avg_price_in_area}")
print(f"Investment Decision: {investment_decision}")









# Load the purchases data
purchases_data_path = 'purchases.xlsx'  # Replace with your file path
purchases_df = pd.read_excel(purchases_data_path)

# Iterate over the rows in the purchases dataframe
for index, purchase in purchases_df.iterrows():
    # Get coordinates for the purchase address
    full_address = f"{purchase['region']} {purchase['address']}"
    coordinates = f"{purchase['Latitude']} {purchase['Longitude']}"
    get_coordinates(full_address, geolocator)
    time.sleep(1)  # To prevent hitting request limit

    if coordinates[0] is not None and coordinates[1] is not None:
        # Count the number of crimes within a 2 km radius
        crime_count = crime_df.apply(lambda row: haversine(float(coordinates[1]), float(coordinates[0]), row['longitude'], row['latitude']), axis=1)
        crimes_within_2km = crime_count[crime_count <= 2].count()

        # Determine investment quality
        avg_price_in_area = purchase['avg price in area']
        user_price = purchase['price']
        investment_decision = 'Good' if user_price < avg_price_in_area and crimes_within_2km < 10 else 'Bad'
        
        # Assign the result to the 'result' column
        purchases_df.at[index, 'result'] = investment_decision
    else:
        print(f"Coordinates for the address '{full_address}' could not be retrieved.")
        purchases_df.at[index, 'result'] = 'Unknown'

# Save the updated dataframe to a new Excel file without modifying the original
output_file_path = 'labeled_purchases.xlsx'
purchases_df.to_excel(output_file_path, index=False)