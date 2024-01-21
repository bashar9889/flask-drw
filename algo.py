import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
from flask import Flask, request, jsonify
import joblib



# Load the data
data_path = 'labeled_purchases.xlsx'
df = pd.read_excel(data_path)

# Preprocess the data
# Assuming your features are in columns like 'Price', 'Latitude', 'Longitude', etc.
# And your target variable is in the column 'result'
features = df[['price', 'Latitude', 'Longitude']]  # Update with actual feature columns
target = df['result']

# Handle missing values if any
features.fillna(method='ffill', inplace=True)

# Encode the categorical target variable
le = LabelEncoder()
target_encoded = le.fit_transform(target)

# Normalize the feature data
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(features_scaled, target_encoded, test_size=0.3, random_state=42)

# Build and train the decision tree model
dt_classifier = DecisionTreeClassifier()
dt_classifier.fit(X_train, y_train)

# Build and train the MLP model
mlp_classifier = MLPClassifier(max_iter=1000)
mlp_classifier.fit(X_train, y_train)

# Evaluate the models
dt_predictions = dt_classifier.predict(X_test)
mlp_predictions = mlp_classifier.predict(X_test)

print("Decision Tree Classifier Report:")
print(classification_report(y_test, dt_predictions))

print("MLP Classifier Report:")
print(classification_report(y_test, mlp_predictions))



# Save the trained models and scaler
joblib.dump(dt_classifier, 'dt_model.pkl')
joblib.dump(mlp_classifier, 'mlp_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

# If you also need to save the label encoder
#joblib.dump(label_encoder, 'label_encoder.pkl')


