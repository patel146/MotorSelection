import requests
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import csv
from classes import DrivetrainData

data_file_path = 'data/data.csv'

def download_drivetrain_data():
    '''
    Get data from google sheets and download locally. This sheet will be used as the source data to run analysis on.
    '''
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS9HEXwMzeAm0KR3eouwCsm3mdRzWk94vf_Xsd7b9NRZJ-J1GnKf6qXVQ7tigkFsu9GTMHCROFbmeN_/pub?gid=0&single=true&output=csv"
    response = requests.get(csv_url)
    # Save the CSV locally
    with open(data_file_path, "wb") as file:
        file.write(response.content)

    print("CSV file downloaded successfully!")

def read_drivetrain_data():
    '''
    Read a CSV file into a dictionary.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        list[dict]: A list of dictionaries where each row in the CSV file 
                    corresponds to a dictionary with column headers as keys.
    '''
    drivetrain_data = []

    # Open the CSV file
    with open(data_file_path, mode='r', newline='') as csvfile:
        # Use csv.DictReader to map rows to dictionaries
        reader = csv.DictReader(csvfile)
        
        # Add each row dictionary to the list
        for row in reader:
            drivetrain_data.append(row)

    return drivetrain_data

drivetrain_data = read_drivetrain_data()

def create_drivetrain_objects(drivetrain_data):
    drivetrains = []
    for entry in drivetrain_data:
        # Extract values from the CSV row (entry is a dictionary)
        motor = entry['MOTOR']
        propeller = entry['PROPELLER']
        motor_weight = entry['MOTOR WEIGHT (g)']
        propeller_weight_per_blade = entry['PROPELLER WEIGHT PER BLADE (g)']
        propeller_configuration = entry['PROPELLER CONFIGURATION']
        motor_cost = entry['MOTOR COST ($CAD)']
        propeller_cost = entry['PROPELLER COST ($CAD)']
        battery_voltage = entry['BATTERY VOLTAGE (V)']
        throttle = entry['THROTTLE (%)']
        power = entry['POWER (W)']
        thrust = entry['THRUST (g)']
        
        # Check if a DrivetrainData object with the same motor and propeller already exists
        existing_drivetrain = next((d for d in drivetrains if d.motor == motor and d.propeller == propeller), None)

        if existing_drivetrain:
            # If the object already exists, add the performance data
            existing_drivetrain.add_performance_data(throttle, power, thrust)
        else:
            # If it doesn't exist, create a new DrivetrainData object
            drivetrain = DrivetrainData(motor, propeller, motor_weight, propeller_weight_per_blade, 
                                        propeller_configuration, motor_cost, propeller_cost, battery_voltage)
            drivetrain.add_performance_data(throttle, power, thrust)

            # Add the new DrivetrainData object to the list
            drivetrains.append(drivetrain)
    return drivetrains

drivetrains = create_drivetrain_objects(drivetrain_data)
    
drivetrains[0].plot_performance_data()
