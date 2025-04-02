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

# load the data and remove rows with NaN
df = pd.read_csv("merged_table.csv")
df
df.dropna(inplace=True)
df.isna().sum() # verifies dataframe has clean data
df.shape

motor_names = df['Motor_Name']
propeller_names = df["Propeller_Name"]

# Choosing features
# Motor specific: kv, weight, diameter, height
# Propeller specific: diameter, pitch, number of blades
# System specific: voltage, throttle setting
features = df[['Throttle', 'Voltage (V)', 'Motor_kv(RPM/V)', 'Motor_Weight(g)', 'Motor_Diameter(mm)', 'Motor_Height(mm)', 'Propeller_Diameter(in)', 'Pitch(in)', 'Number_of_Blades']]
targets = df['Thrust(gf)']

# Try Log
# features_log = np.log1p(features)
# targets_log = np.log1p(targets)

feature_scaler = StandardScaler()
target_scaler = StandardScaler()
features_scaled = feature_scaler.fit_transform(features)
targets_scaled = target_scaler.fit_transform(targets.values.reshape(-1, 1))



# X_train, X_test, y_train, y_test = train_test_split(features_log, targets_log, test_size=0.2, random_state=214)

X_train, X_test, y_train, y_test = train_test_split(features_scaled, targets_scaled, test_size=0.2, random_state=214)

def check_data_cleanliness(df, name):
    print(f"🔍 Checking {name}...")
    if np.isnan(df).sum().sum() > 0:
        print(f"❌ {name} contains NaN values!")
    else:
        print(f"✅ No NaN values in {name}.")

    if np.isinf(df).sum().sum() > 0:
        print(f"❌ {name} contains infinite values!")
    else:
        print(f"✅ No infinite values in {name}.")

    print(f"📊 {name} shape: {df.shape}\n")

# Check training and test data
check_data_cleanliness(X_train, "X_train")
check_data_cleanliness(X_test, "X_test")
check_data_cleanliness(y_train, "y_train")
check_data_cleanliness(y_test, "y_test")

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
target_scaler.inverse_transform(predictions)

model.save('mlp_model_v11.keras')

# prompt: evaluate mlp_model_v1 to mlp_model_v10 and present the results in a bar graph

import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import os

model_results = []

for i in [7,8,11]:
    model_path = f'mlp_model_v{i}.keras'
    if os.path.exists(model_path):
      try:
        model = tf.keras.models.load_model(model_path)
        print(model.summary())
        # Assuming X_test and y_test are defined as in your original code
        test_loss, test_mae = model.evaluate(X_test, y_test, verbose=0)
        model_results.append({'Model': f'mlp_model_v{i}', 'MAE': test_mae})
      except Exception as e:
        print(f"Error loading model {model_path}: {e}")
    else:
        print(f"Model file not found: {model_path}")

results_df = pd.DataFrame(model_results)

plt.figure(figsize=(10, 6))
plt.bar(results_df['Model'], results_df['MAE'])
plt.xlabel('Model Version')
plt.ylabel('Mean Absolute Error (MAE)')
plt.yscale('log')
plt.title('Performance of MLP Models')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

import joblib

joblib.dump(feature_scaler, "mlp_model_v11_feature_scaler.pkl")
joblib.dump(target_scaler, "mlp_model_v11_target_scaler.pkl")

actual_motor_name = "T-Motor U5 KV400"
actual_propeller_name = "T-Motor P15x5"
actual_throttle_values = [0.0, 0.0, 0.14, 0.1666666666666666, 0.2222222222222222, 0.2777777777777778, 0.3333333333333333, 0.35, 0.3888888888888889, 0.4444444444444444, 0.5, 0.5, 0.5555555555555556, 0.6111111111111112, 0.6666666666666666, 0.7222222222222222, 0.7777777777777778, 0.8, 0.8333333333333334, 0.8888888888888888, 0.9444444444444444, 1.0, 1.0]
actual_thrust_values = [1.4240825462667999, 0.6514313352341, 20.115591312837697, 21.9666102420602, 66.5461687995696, 120.6869394737754, 198.8750441950105, 370.5641632142067, 302.7335311408687, 421.5960387892298, 769.364806658645, 595.2549069691078, 766.163501572168, 927.9562264570776, 1120.457268361469, 1319.9702701031445, 1563.7447171027825, 2091.8387560088313, 1786.382329565856, 2031.0753637517398, 2250.2668496468214, 2369.4668440009586, 2485.1930373686223]
plt.scatter(actual_throttle_values, actual_thrust_values, color="red", label="Actual Data", zorder=3)