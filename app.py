import streamlit as st
import tensorflow as tf
import numpy as np
import os

# Load the model
MODEL_PATH = "ml_models/mlp_model_v2.keras"
if os.path.exists(MODEL_PATH):
    model = tf.keras.models.load_model(MODEL_PATH)
else:
    st.error("Model file not found! Ensure that 'model.keras' exists in 'ml_models' folder.")
    st.stop()

# Define a simple feature encoder (this needs to match how the model was trained)


def encode_features(motor, propeller):
    motor_mapping = {"motor1": 0, "motor2": 1, "motor3": 2}  # Example mapping
    propeller_mapping = {"prop1": 0, "prop2": 1, "prop3": 2}  # Example mapping

    if motor not in motor_mapping or propeller not in propeller_mapping:
        return None

    return np.array([[motor_mapping[motor], propeller_mapping[propeller]]], dtype=np.float32)


# Streamlit UI
st.title("MLP Thrust Prediction")
st.write("Enter a motor and propeller to predict thrust:")

motor = st.text_input("Motor Name:")
propeller = st.text_input("Propeller Name:")

if st.button("Predict Thrust"):
    features = encode_features(motor, propeller)
    if features is None:
        st.error("Invalid motor or propeller name! Use predefined values.")
    else:
        thrust_prediction = model.predict(features)[0][0]  # Assuming single output neuron
        st.success(f"Predicted Thrust: {thrust_prediction:.2f} N")


def stop_app():
    os._exit(0)  # Forcefully exit the application


st.button("Close App", on_click=stop_app)


def on_closed():
    os._exit(0)  # Forcefully exit the app when the window is closed
