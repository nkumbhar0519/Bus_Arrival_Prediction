import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle

# Load dataset
data = pd.read_csv("bus_data.csv")

# Convert day_type to numeric
data['day_type'] = data['day_type'].map({'weekday': 0, 'weekend': 1})

# Convert traffic column if needed
data['traffic'] = data['traffic'].map({'low':0,'medium':3,'heavy':6})

# Features (inputs)
X = data[['route_id', 'stop_id', 'hour', 'day_type','traffic']]

# Target
y = data['arrival_delay']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)

# Save model
with open("bus_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model trained and saved")