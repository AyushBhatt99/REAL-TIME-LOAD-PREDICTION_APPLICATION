import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
# from sklearn.metrics import mean_squared_error
from sklearn.metrics import root_mean_squared_error
import joblib

# Load your dataset
df = pd.read_csv('load.csv')

# Data preprocessing: Scale relevant columns (assuming certain columns based on previous conversation)
scaler = MinMaxScaler()

# Assuming your features are in these columns (replace with actual column names)
features = ['temp_2M', 'humidity_2M', 'precipitation_2M', 'wind_speed_2M', 'holiday']
target = 'net_demand'

# Scale features
df[features] = scaler.fit_transform(df[features])

# Drop any missing values (if needed)
df = df.dropna()

# Define X (features) and y (target)
X = df[features].values
y = df[target].values

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Train the Linear Regression model
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Test the model (optional)
y_pred = regressor.predict(X_test)
rmse = root_mean_squared_error(y_test, y_pred)
print(f'RMSE: {rmse}')

# Save the trained model to a file
joblib.dump(regressor, 'linear_regression_model.pkl')

# Save the scaler to use during prediction
joblib.dump(scaler, 'scaler.pkl')

print("Model and scaler saved successfully!")
