import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('historical_exchange_rates.csv')

# Check the first few rows of the dataset
print(data.head())

# Preprocess the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data['exchange_rate'].values.reshape(-1, 1))

# Create training and test datasets
train_size = int(len(scaled_data) * 0.8)
train_data = scaled_data[:train_size]
test_data = scaled_data[train_size:]

# Function to create sequences for LSTM
def create_sequences(data, seq_length):
    xs, ys = [], []
    for i in range(len(data) - seq_length):
        x = data[i:i + seq_length]
        y = data[i + seq_length]
        xs.append(x)
        ys.append(y)
    print(f"Created {len(xs)} sequences of length {seq_length}")
    return np.array(xs), np.array(ys)

seq_length = 5  # Reduced sequence length
x_train, y_train = create_sequences(train_data, seq_length)
x_test, y_test = create_sequences(test_data, seq_length)

# Print shapes for debugging
print(f"x_train shape: {x_train.shape}")
print(f"y_train shape: {y_train.shape}")
print(f"x_test shape: {x_test.shape}")
print(f"y_test shape: {y_test.shape}")

# Reshape input data to be 3-dimensional
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# Build the LSTM model
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(seq_length, 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(units=1))

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, epochs=25, batch_size=32)


model.save('currency_predictor.h5')


predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

train_data_plot = scaler.inverse_transform(train_data)
test_data_plot = scaler.inverse_transform(test_data)


train_index = data.index[:train_size]
test_index = data.index[train_size + seq_length:train_size + seq_length + len(predictions)]


plt.figure(figsize=(14, 5))
plt.plot(train_index, train_data_plot[:len(train_index)], label='Training Data')
plt.plot(data.index[train_size:train_size + len(test_data)], test_data_plot[:len(test_data)], label='Test Data')
plt.plot(test_index, predictions, label='Predicted Data')
plt.legend()
plt.show()
