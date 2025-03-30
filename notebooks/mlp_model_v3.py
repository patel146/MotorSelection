# -*- coding: utf-8 -*-
"""ENGM670_Tyto

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1B9GoMZPrcH3VQKFS-CvEnNrEKxdOzYt4
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score

df = pd.read_csv("merged_table.csv")
df
df.isna().sum()

# sns.pairplot(df.sample(25),hue="Throttle")
# plt.show()

motor_names = df['Motor_Name']
propeller_names = df["Propeller_Name"]

motor_encoder = LabelEncoder()
propeller_encoder = LabelEncoder()
df['Motor_Name'] = motor_encoder.fit_transform(motor_names)
df['Propeller_Name'] = propeller_encoder.fit_transform(propeller_names)

df = df.dropna()

features = df[['Throttle', 'Rotation_speed(RPM)', 'Voltage (V)', 'Motor_Name', 'Motor_kv(RPM/V)', 'Motor_Weight(g)', 'Motor_Diameter(mm)', 'Motor_Height(mm)', 'Internal_Resistance(Ohms)', 'Propeller_Name', 'Propeller_Diameter(in)', 'Pitch(in)', 'Number_of_Blades']]
targets = df['Thrust(gf)']


scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

X_train, X_test, y_train, y_test = train_test_split(features_scaled, targets, test_size=0.2, random_state=214)

features.isna().sum()

model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(128,activation='relu'),
    tf.keras.layers.Dense(64,activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(
    optimizer='adam',
    loss='mean_squared_error',
    metrics=['mae'],
)

model.summary()

history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=100,
    batch_size=32,
    verbose=1
)

test_loss, test_mae = model.evaluate(X_test, y_test)
print(f"Test Loss: {test_loss}")
print(f"Test MAE: {test_mae}")

plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()

"""# Consider Early Stopping"""

# Predict on new data (e.g., a new motor-propeller combination)
predictions = model.predict(X_test)

# Example: Print the first 5 predicted thrust values
print(predictions[:5])

model.save('mlp_model_v3.keras')