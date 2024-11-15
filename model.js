const fs = require('fs');
const csv = require('csv-parser');
const MLR = require('ml-regression').MultivariateLinearRegression;  // Multiple Linear Regression
const scaler = require('minmaxscaler');  // For scaling similar to MinMaxScaler in Python

let data = [];
let features = [];
let target = [];

// Read the CSV file and process the data
fs.createReadStream('load.csv')
  .pipe(csv())
  .on('data', (row) => {
    // Extract features and target columns
    // console.log(row['humidity_2M'])
    features.push([
      parseFloat(row['temp_2M']),
      parseFloat(row['humidity_2M']),
      parseFloat(row['precipitation_2M']),
      parseFloat(row['wind_speed_2M']),
      parseFloat(row['holiday'])
    ]);
    target.push(parseFloat(row['net_demand']));
  })
  .on('end', () => {
    console.log('CSV file successfully processed');

    // Scaling the features (similar to MinMaxScaler in Python)
    // console.log(features)
    let scaledFeatures = features
  // console.log(scaledFeatures)
    // Split the data into training and testing sets (75% training, 25% testing)
    let splitIndex = Math.floor(scaledFeatures.length * 0.75);
    let X_train = scaledFeatures.slice(0, splitIndex);
    let X_test = scaledFeatures.slice(splitIndex);
    let y_train = target.slice(0, splitIndex);
    let y_test = target.slice(splitIndex);

    // Train the Linear Regression model
    console.log(X_train)
    console.log(y_train)
    const regression = new MLR(X_train, y_train);

    // Test the model and calculate RMSE (Root Mean Squared Error)
    const y_pred = X_test.map(x => regression.predict(x));
    const rmse = Math.sqrt(y_test.reduce((sum, y, idx) => sum + Math.pow(y - y_pred[idx], 2), 0) / y_test.length);
    
    console.log(`RMSE: ${rmse}`);

    // Save the model and scaler
    fs.writeFileSync('linear_regression_model.json', JSON.stringify(regression));
    fs.writeFileSync('scaler.json', JSON.stringify(scaler));
    console.log("Model and scaler saved successfully!");
  });
