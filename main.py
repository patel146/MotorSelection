import requests
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import csv
from classes import DrivetrainData,Battery,DroneConfiguration
from typing import List
import mplcursors
import math

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

# download_data()

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
            existing_drivetrain = next((d for d in drivetrains if d.motor == motor and d.propeller == propeller and d.cell_count == cell_count), None)

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
    
# for index,drivetrain in enumerate(drivetrains):
#     print(index,drivetrain)
    
def create_drone_configurations():
    drone_configurations: List[DroneConfiguration] = []
    print(f'{len(drivetrains)} drivetrains, {len(batteries)} batteries')
    for drivetrain in drivetrains:
        for battery in batteries:
            if battery.cell_count == drivetrain.cell_count:
                for number_of_batteries in range(1,6):
                    drone_configurations.append(DroneConfiguration(drivetrain,battery,number_of_batteries))
    return drone_configurations

drone_configurations = create_drone_configurations()

print(f'{len(drone_configurations)} total configurations')

def create_drone_configurations_lookup_table(drone_configurations: List[DroneConfiguration], filename="data/drone_configurations_lookup.csv"):
    """
    Create a CSV file containing a lookup table of drone configurations.

    Parameters:
    - drone_configurations: List of drone configuration objects.
    - filename: Name of the CSV file to be created (default: "drone_configurations_lookup.csv").

    Each drone configuration object is expected to have the following attributes:
    - id: Unique identifier for the configuration.
    - motor: Motor used in the configuration.
    - propeller: Propeller used in the configuration.
    - battery: Battery used in the configuration.
    - number_of_batteries: Number of batteries in the configuration.
    """
    # Define the CSV header
    header = ["id", "motor", "propeller", "battery", "number_of_batteries","cost","useful_thrust","avail_weight","endurance","throttle"]
    
    # Open the file in write mode
    with open(filename, mode="w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        
        # Write the header
        writer.writeheader()
        
        # Write each drone configuration as a row
        for config in drone_configurations:
            writer.writerow({
                "id": config.id,
                "motor": config.drivetrain.motor,
                "propeller": config.drivetrain.propeller,
                "battery": config.battery,
                "number_of_batteries": config.number_of_batteries,
                "cost": config.cost(),
                "useful_thrust":config.total_useful_hover_thrust(1.8),
                "avail_weight": config.total_available_weight_capacity(),
                "endurance": config.naive_endurance(1.8),
                "throttle": config.ideal_throttle_setting(1.8)
            })

    print(f"Lookup table created: {filename}")
    
create_drone_configurations_lookup_table(drone_configurations)

def create_drone_configurations_decision_table(drone_configurations: List[DroneConfiguration],  thrust_to_weight_ratio, filename="data/drone_configurations_decision.csv"):
    """
    Create a CSV file containing a decision table of drone configurations and key stats.

    """
    # Define the CSV header
    header = ["id", "motor", "propeller", "battery", "number_of_batteries","useful thrust","endurance","score"]
    
    # Open the file in write mode
    with open(filename, mode="w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        
        # Write the header
        writer.writeheader()
        
        # Write each drone configuration as a row
        for config in drone_configurations:
            writer.writerow({
                "id": config.id,
                "motor": config.drivetrain.motor,
                "propeller": config.drivetrain.propeller,
                "battery": config.battery.name,
                "number_of_batteries": config.number_of_batteries,
                "useful thrust": config.total_useful_hover_thrust(thrust_to_weight_ratio),
                "endurance": config.naive_endurance(thrust_to_weight_ratio),
                "score": config.total_useful_hover_thrust(thrust_to_weight_ratio)/config.weight() + config.naive_endurance(thrust_to_weight_ratio)/60,
                "throttle": config.ideal_throttle_setting(1.8)
            })

    print(f"decision table created: {filename}")
    
# create_drone_configurations_decision_table(drone_configurations,1.7)

# thrust_to_weight_ratio = 2
# fig, ax = plt.subplots()
# plt.xlabel('Endurance [min.]', fontsize=12)
# plt.ylabel('Useful Thrust (g)', fontsize=12)
# ax.set_ylim([0,16000])
# ax.set_xlim([0,60])
# plt.title('Performance Data: Endurance vs. Useful Thrust', fontsize=14)

# for drone_configuration in drone_configurations:
#     sc = plt.scatter(drone_configuration.naive_endurance(thrust_to_weight_ratio), drone_configuration.total_useful_hover_thrust(
#         thrust_to_weight_ratio), marker='o', linestyle='-', color='b', label=f'{drone_configuration.id}')
#     sc = plt.scatter(drone_configuration.naive_endurance(thrust_to_weight_ratio=1.9), drone_configuration.total_useful_hover_thrust(
#         thrust_to_weight_ratio=1.9), marker='o', linestyle='-', color='r', label=f'{drone_configuration.id}')
#     sc = plt.scatter(drone_configuration.naive_endurance(thrust_to_weight_ratio=1.8), drone_configuration.total_useful_hover_thrust(
#         thrust_to_weight_ratio=1.8), marker='o', linestyle='-', color='g', label=f'{drone_configuration.id}')
#     sc = plt.scatter(drone_configuration.naive_endurance(thrust_to_weight_ratio=1.7), drone_configuration.total_useful_hover_thrust(
#         thrust_to_weight_ratio=1.7), marker='o', linestyle='-', color='k', label=f'{drone_configuration.id}')
#     # mplcursors.cursor(sc, hover=True)
#     plt.grid(True, linestyle='--', alpha=0.6)
#     # Show the plot
#     plt.tight_layout()
# plt.show()

def carpet_plot(budget):
    # Define the range of thrust_to_weight_ratio
    thrust_to_weight_ratios = np.linspace(1.2, 2.2, 10)  # Adjust the range and number of points as needed
    fig, ax = plt.subplots()
    ax.set_ylim([0,20000])
    ax.set_xlim([0,60])

    # Create a grid for endurance and hover thrust for all drone configurations
    for drone_configuration in drone_configurations:
        if drone_configuration.cost() < budget:
            if drone_configuration.total_useful_hover_thrust(1.8) > drone_configuration.total_available_weight_capacity() and drone_configuration.total_available_weight_capacity() > 6000:
                # Calculate values
                endurance = []
                hover_thrust = []
                for ratio in thrust_to_weight_ratios:
                    endurance.append(drone_configuration.naive_endurance(thrust_to_weight_ratio=ratio))
                    hover_thrust.append(drone_configuration.total_useful_hover_thrust(thrust_to_weight_ratio=ratio))
                
                # Create a carpet plot (or line plot) with thrust_to_weight_ratio as the third variable
                plt.plot(endurance, hover_thrust, label=f'{drone_configuration.id}')
                plt.scatter(endurance, hover_thrust, c=thrust_to_weight_ratios, cmap='viridis', s=10)  # Color by thrust_to_weight_ratio

    # Add labels and legend
    plt.colorbar(label="Thrust-to-Weight Ratio")
    plt.xlabel("Naive Endurance [min.]")
    plt.ylabel("Total Useful Hover Thrust [g]")
    # plt.legend(title="Drone Configurations")
    plt.title("Carpet Plot of Endurance vs. Hover Thrust")
    mplcursors.cursor(fig, hover=True)
    plt.show()
    
def carpet_plot_available_weight():
    # Define the range of thrust_to_weight_ratio
    thrust_to_weight_ratios = np.linspace(1.2, 2.2, 10)  # Adjust the range and number of points as needed
    fig, ax = plt.subplots()
    ax.set_ylim([0,20000])
    ax.set_xlim([0,60])

    # Create a grid for endurance and hover thrust for all drone configurations
    for drone_configuration in drone_configurations:
        # Calculate values
        endurance = []
        available_weight = []
        for ratio in thrust_to_weight_ratios:
            endurance.append(drone_configuration.naive_endurance(thrust_to_weight_ratio=ratio))
            available_weight.append(drone_configuration.total_available_weight_capacity())
        
        # Create a carpet plot (or line plot) with thrust_to_weight_ratio as the third variable
        plt.plot(endurance, available_weight, label=f'{drone_configuration.id}')
        plt.scatter(endurance, available_weight, c=thrust_to_weight_ratios, cmap='viridis', s=10)  # Color by thrust_to_weight_ratio

    # Add labels and legend
    plt.colorbar(label="Thrust-to-Weight Ratio")
    plt.xlabel("Naive Endurance [min.]")
    plt.ylabel("Total Available Weight [g]")
    # plt.legend(title="Drone Configurations")
    plt.title("Carpet Plot of Endurance vs. Available Weight")
    mplcursors.cursor(fig, hover=True)
    plt.show()
    
def carpet_plot_cruise(budget,vel):
    # Define the range of thrust_to_weight_ratio
    thrust_to_weight_ratios = np.linspace(1.2, 2.2, 10)  # Adjust the range and number of points as needed
    fig, ax = plt.subplots()
    ax.set_ylim([0,20000])
    ax.set_xlim([0,60])

    # Create a grid for endurance and hover thrust for all drone configurations
    for drone_configuration in drone_configurations:
        if drone_configuration.cost() < budget:
            if drone_configuration.total_useful_hover_thrust(1.8) > drone_configuration.total_available_weight_capacity() and drone_configuration.total_available_weight_capacity() > 6000:
                # Calculate values
                endurance = []
                available_payload_at_cruise = []
                for ratio in thrust_to_weight_ratios:
                    endurance.append(drone_configuration.naive_endurance(thrust_to_weight_ratio=ratio))
                    available_payload_at_cruise.append(drone_configuration.available_payload_at_cruise(thrust_to_weight_ratio=ratio, cruise_velocity=vel))
                
                # Create a carpet plot (or line plot) with thrust_to_weight_ratio as the third variable
                plt.plot(endurance, available_payload_at_cruise, label=f'{drone_configuration.id}')
                plt.scatter(endurance, available_payload_at_cruise, c=thrust_to_weight_ratios, cmap='viridis', s=10)  # Color by thrust_to_weight_ratio

    # Add labels and legend
    plt.colorbar(label="Thrust-to-Weight Ratio")
    plt.xlabel("Naive Endurance [min.]")
    plt.ylabel("Available Payload at Cruise [g]")
    # plt.legend(title="Drone Configurations")
    plt.title("Carpet Plot of Endurance vs. Available payload at cruise")
    mplcursors.cursor(fig, hover=True)
    plt.grid()
    plt.show()
    
# carpet_plot(6000)
# carpet_plot_cruise(6000,15)
candidate = next((obj for obj in drone_configurations if obj.id == 'd33f3ccc'), None)
# d = candidate.drag_force(10)
# w = candidate.weight()
# tw = 1.2
# vel = 20
# cr = candidate.available_payload_at_cruise(tw,vel)
# hvr = candidate.total_useful_hover_thrust(tw)
# print(cr)
# print(hvr)
# print(hvr-cr)
# print(math.degrees(math.atan(d/w)))

# candidate.carpet_plot_velocity()
# carpet_plot(6000)

def get_battery_config_performance(target):
    ''' Returns the overall weight and cost of a battery configuration, given a target capacity
    '''
    battery_config = candidate.get_battery_configuration(batteries,target)

    total_weight = sum(battery.weight for battery in battery_config)
    total_cost = sum(battery.cost for battery in battery_config)

    return total_weight, total_cost

def plot_battery_configs():
    targets = np.linspace(800,1200,10)
    weights = []
    costs = []
    available_payloads = []
    endurances = []

    with open('data/battery_configs.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Weight (g)', 'Cost ($CAD)', 'Available Payload (g)', 'Endurance (min)', 'Battery Config'])

        for target in targets:
            weight, cost = get_battery_config_performance(target)
            weights.append(weight)
            costs.append(cost)
            battery_config = candidate.get_battery_configuration(batteries,target)
            available_payload, endurance = candidate.drone_summary_given_battery_config(battery_config,1.8,15)
            available_payloads.append(available_payload)
            endurances.append(endurance)

            battery_config_str = ', '.join([battery.name for battery in battery_config])
            
            writer.writerow([weight, cost, available_payload, endurance, battery_config_str])


    plt.scatter(weights, costs)
    plt.xlabel('Total Weight (g)')
    plt.ylabel('Total Cost ($CAD)')

    for i, (weight, cost) in enumerate(zip(weights, costs)):
        plt.annotate(f'Payload: {available_payloads[i]}g\nEndurance: {endurances[i]}min', (weight, cost),
                        textcoords="offset points", xytext=(0, 10), ha='center')
    plt.show()



print(candidate.ideal_total_power_setting(2))

