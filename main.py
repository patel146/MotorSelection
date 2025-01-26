import requests
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import csv
from classes import DrivetrainData,Battery,DroneConfiguration
from typing import List
import mplcursors

data_file_path = 'data/data.csv'
battery_data_file_path = 'data/battery_data.csv'

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

def download_battery_data():
    '''
    Get data from google sheets and download locally. This sheet will be used as the source data to run analysis on.
    '''
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS9HEXwMzeAm0KR3eouwCsm3mdRzWk94vf_Xsd7b9NRZJ-J1GnKf6qXVQ7tigkFsu9GTMHCROFbmeN_/pub?gid=825319924&single=true&output=csv"
    response = requests.get(csv_url)
    # Save the CSV locally
    with open(battery_data_file_path, "wb") as file:
        file.write(response.content)

    print("CSV file downloaded successfully!")

def download_data():
    download_drivetrain_data()
    download_battery_data()

download_data()

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
def read_battery_data():
    '''
    Read a CSV file into a dictionary.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        list[dict]: A list of dictionaries where each row in the CSV file 
                    corresponds to a dictionary with column headers as keys.
    '''
    battery_data = []

    # Open the CSV file
    with open(battery_data_file_path, mode='r', newline='') as csvfile:
        # Use csv.DictReader to map rows to dictionaries
        reader = csv.DictReader(csvfile)
        
        # Add each row dictionary to the list
        for row in reader:
            battery_data.append(row)

    return battery_data

drivetrain_data = read_drivetrain_data()
battery_data = read_battery_data()

def create_drivetrain_objects(drivetrain_data):
    drivetrains = []
    
    for entry in drivetrain_data:
        try:
            # Extract values from the CSV row (entry is a dictionary)
            motor = entry['MOTOR']
            propeller = entry['PROPELLER']
            motor_weight = float(entry['MOTOR WEIGHT (g)'])
            propeller_weight_per_blade = float(entry['PROPELLER WEIGHT PER BLADE (g)'])
            propeller_configuration = int(entry['PROPELLER CONFIGURATION'])
            motor_cost = float(entry['MOTOR COST ($CAD)'])
            propeller_cost = float(entry['PROPELLER COST ($CAD)'])
            battery_voltage = float(entry['BATTERY VOLTAGE (V)'])
            cell_count = int(entry['CELL COUNT'])
            throttle = float(entry['THROTTLE (%)'])
            power = float(entry['POWER (W)'])
            thrust = float(entry['THRUST (g)'])
            
            # Check if a DrivetrainData object with the same motor, propeller already exists
            existing_drivetrain = next((d for d in drivetrains if d.motor == motor and d.propeller == propeller), None)

            if existing_drivetrain:
                # If the object already exists, add the performance data
                existing_drivetrain.add_performance_data(throttle, power, thrust)
            else:
                # If it doesn't exist, create a new DrivetrainData object
                drivetrain = DrivetrainData(motor, propeller, motor_weight, propeller_weight_per_blade, 
                                            propeller_configuration, motor_cost, propeller_cost, battery_voltage, cell_count)
                drivetrain.add_performance_data(throttle, power, thrust)
                drivetrains.append(drivetrain)
                
        except KeyError as e:
            print(f"Error: Missing key {e} in entry {entry}")
        except ValueError as e:
            print(f"Error: Invalid value for {e} in entry {entry}")
    
    return drivetrains


def create_battery_objects(battery_data):
    batteries = []
    for entry in battery_data:
        name = entry['NAME']
        weight = float(entry['WEIGHT (g)'])
        cost = float(entry['COST ($CAD)'])
        voltage = float(entry['VOLTAGE (V)'])
        cell_count = int(entry['CELL COUNT'])
        capacity_milliamp_hours = float(entry['CAPACITY (mAh)'])
        
        batteries.append(Battery(name, weight, cost, voltage, cell_count, capacity_milliamp_hours))
    return batteries

drivetrains = create_drivetrain_objects(drivetrain_data)
batteries = create_battery_objects(battery_data)
    
for index,drivetrain in enumerate(drivetrains):
    print(index,drivetrain)
    
def create_drone_configurations():
    drone_configurations: List[DroneConfiguration] = []
    print(f'{len(drivetrains)} drivetrains, {len(batteries)} batteries')
    for drivetrain in drivetrains:
        for battery in batteries:
            if battery.cell_count == drivetrain.cell_count:
                for number_of_batteries in range(1,4):
                    drone_configurations.append(DroneConfiguration(drivetrain,battery,number_of_batteries))
    return drone_configurations
drone_configurations = create_drone_configurations()

thrust_to_weight_ratio = 2
fig, ax = plt.subplots()
plt.xlabel('Endurance [min.]', fontsize=12)
plt.ylabel('Useful Thrust (g)', fontsize=12)
plt.title('Performance Data: Endurance vs. Useful Thrust', fontsize=14)

for drone_configuration in drone_configurations:
    sc = plt.scatter(drone_configuration.naive_endurance(thrust_to_weight_ratio), drone_configuration.total_useful_hover_thrust(
        thrust_to_weight_ratio), marker='o', linestyle='-', color='b', label=f'{drone_configuration.id}')
    mplcursors.cursor(sc, hover=True)
    plt.grid(True, linestyle='--', alpha=0.6)
    # Show the plot
    plt.tight_layout()
plt.show()
