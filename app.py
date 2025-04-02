import streamlit as st
import tensorflow as tf
import numpy as np
import os
import sqlite3
from dataclasses import dataclass
import pickle
import joblib
import matplotlib.pyplot as plt

feature_scaler = joblib.load('ml_models/mlp_model_v11_feature_scaler.pkl')
target_scaler = joblib.load('ml_models/mlp_model_v11_target_scaler.pkl')


@dataclass
class Motor:
    name: str
    kv: float
    weight: float
    diameter: float
    height: float


@dataclass
class Propeller:
    name: str
    diameter: float
    pitch: float
    number_of_blades: int


    # Connect to the database
conn = sqlite3.connect("data/tyto_database.db")
cursor = conn.cursor()

# Fetch distinct Motor data
cursor.execute(
    "SELECT \"Name\", kv, \"Weight(g)\", \"Diameter(mm)\", \"Height(mm)\" FROM motors_table")

# Create Motor objects
motors = [
    Motor(name=row[0], kv=row[1], weight=row[2], diameter=row[3], height=row[4])
    for row in cursor.fetchall()  # Fetch all rows here
]

# Fetch distinct Propeller data
cursor.execute(
    "SELECT \"Name\", \"Diameter(in)\", \"Pitch(in)\", \"Number_of_Blades\" FROM propellers_table")

# Create Propeller objects
propellers = [
    Propeller(name=row[0], diameter=row[1], pitch=row[2], number_of_blades=row[3])
    for row in cursor.fetchall()  # Fetch all rows here
]

motor_choices = [motor.name for motor in motors]
propeller_choices = [propeller.name for propeller in propellers]

conn.close()  # Close the connection


# Streamlit UI
st.title("MLP Thrust Prediction")
st.write("Enter a motor and propeller to predict thrust:")

# Create a dictionary where the key is the motor name and the value is the Motor object
motor_dict = {motor.name: motor for motor in motors}

# Get a list of motor names for the selectbox
motor_choices = list(motor_dict.keys())

# Streamlit selectbox to select the motor by name
selected_motor_name = st.selectbox("Motor Name:", motor_choices)

# Access the full motor object based on the selected name
selected_motor = motor_dict[selected_motor_name]

# Create a dictionary where the key is the motor name and the value is the Motor object
propeller_dict = {propeller.name: propeller for propeller in propellers}

# Get a list of motor names for the selectbox
propeller_choices = list(propeller_dict.keys())

# Streamlit selectbox to select the motor by name
selected_propeller_name = st.selectbox("Propeller Name:", propeller_choices)

# Access the full motor object based on the selected name
selected_propeller = propeller_dict[selected_propeller_name]


use_range = st.checkbox("Run 10 throttle settings")

if use_range:
    throttle_values = np.linspace(0.1, 1, 10)  # 10 throttle values from 0 to 1
else:
    throttle = st.number_input("Throttle (0-1)", min_value=0.0, max_value=1.0, step=0.01)
    throttle_values = [throttle]  # Convert single value to list for consistency

# Display selected throttle values
st.write("Selected Throttle Values:", throttle_values)

voltage = st.number_input("Voltage (V)")


def create_features(throttle, voltage, motor: Motor, propeller: Propeller):
    features = np.array([throttle, voltage, motor.kv, motor.weight, motor.diameter, motor.height,
                        propeller.diameter, propeller.pitch, propeller.number_of_blades])
    print(f"raw features: {features}")

    features = features.reshape(1, -1)
    features = feature_scaler.transform(features)
    print(f"scaled features: {features}")

    return features


model = tf.keras.models.load_model("ml_models/mlp_model_v10.keras")

if st.button("Predict Thrust"):
    predicted_thrusts = []
    for throttle in throttle_values:
        features = create_features(throttle, voltage, selected_motor, selected_propeller)
        prediction = model.predict(features)
        prediction = target_scaler.inverse_transform(prediction)

        predicted_thrusts.append(prediction[0][0])

    # Initialize actual thrust values
    actual_throttle_values = []
    actual_thrust_values = []

    # Connect to SQLite database and fetch real data
    conn = sqlite3.connect("data/tyto_database.db")
    cursor = conn.cursor()

    query = """
        SELECT Throttle, \"Thrust(gf)\"
        FROM merged_table 
        WHERE motor_name = ? AND propeller_name = ? 
        ORDER BY throttle ASC
    """
    cursor.execute(query, (selected_motor_name, selected_propeller_name))
    results = cursor.fetchall()

    # Close the connection
    conn.close()

    # Process actual data if available
    if results:
        actual_throttle_values, actual_thrust_values = zip(*results)  # Unpack throttle and thrust values

    # Create the plot
    fig, ax = plt.subplots()

    # Plot predicted thrust curve
    ax.plot(throttle_values, predicted_thrusts,
            label=f"Predicted: {selected_motor_name} & {selected_propeller_name}", linestyle="dashed")

    # Plot actual thrust data if available
    if results:
        ax.scatter(actual_throttle_values, actual_thrust_values, color="red", label="Actual Data", zorder=3)
        print(actual_throttle_values)
        print(actual_thrust_values)

    # Formatting
    ax.set_title("Thrust Curve Comparison")
    ax.set_xlabel("Throttle Setting [0-1]")
    ax.set_ylabel("Thrust [gf]")
    ax.legend()

    # Display in Streamlit
    st.pyplot(fig)


def stop_app():
    os._exit(0)  # Forcefully exit the application


st.button("Close App", on_click=stop_app)


def on_closed():
    os._exit(0)  # Forcefully exit the app when the window is closed
