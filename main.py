import csv
import re



def to_valid_variable_name(s):
    """
    Converts a string into a valid Python variable name.

    Args:
        s (str): The input string.

    Returns:
        str: A valid Python variable name.
    """
    s = re.sub(r'[^0-9a-zA-Z_]', '_', s)  # Replace invalid characters with underscores
    s = re.sub(r'^[^a-zA-Z_]+', '', s)    # Remove leading characters that aren't letters or underscores
    return s

def parse_component_data_from_tsv(file_path):
    """
    Parses motor data from a TSV file and creates a Motor object for each row.

    Args:
        file_path (str): Path to the TSV file.

    Returns:
        list: A list of Component objects.
    """
    components = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            link = row['LINK']
            name = row['NAME']
            weight = float(row['WEIGHT [g]'])
            cost = float(row['COST [CAD]'].replace('$', ''))
            print(f"{to_valid_variable_name(name)} = Component('{link}', '{name}', {weight}, {cost})")
    return components

def parse_component_data_from_tsv2(file_path):
    """
    Parses motor data from a TSV file and creates a Motor object for each row.

    Args:
        file_path (str): Path to the TSV file.

    Returns:
        list: A list of Component objects.
    """
    components = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            motor = row['MOTOR']
            number_of_cells = row['NO of CELLS']
            prop = (row['PROP'])
            drive_train_id = int(row['DRIVETRAIN ID'])
            amperage = row['AMPERAGE [A]']
            hover_thrust = row['HOVER THRUST [g]']
            max_thrust = row['MAX THRUST [g]']
            print(f"DT_{drive_train_id} = DriveTrain({amperage},{hover_thrust},{max_thrust},{to_valid_variable_name(motor)},{to_valid_variable_name(prop)},'{number_of_cells}',1)")
            
import csv
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Motor:
    def __init__(self, link, name, weight, cost):
        self.link = link
        self.name = name
        self.weight = weight
        self.cost = cost

    def __repr__(self):
        return f"Motor(name='{self.name}', weight={self.weight}g, cost={self.cost} CAD)"

def parse_motor_data_from_tsv(file_path):
    """
    Parses motor data from a TSV file and creates a Motor object for each row.

    Args:
        file_path (str): Path to the TSV file.

    Returns:
        list: A list of Motor objects.
    """
    motors = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            link = row['LINK']
            name = row['NAME']
            weight = int(row['WEIGHT [g]'])
            cost = float(row['COST [CAD]'].replace('$', ''))
            motors.append(Motor(link, name, weight, cost))
    return motors

def to_valid_variable_name(s):
    """
    Converts a string into a valid Python variable name.

    Args:
        s (str): The input string.

    Returns:
        str: A valid Python variable name.
    """
    s = re.sub(r'[^0-9a-zA-Z_]', '_', s)  # Replace invalid characters with underscores
    s = re.sub(r'^[^a-zA-Z_]+', '', s)    # Remove leading characters that aren't letters or underscores
    return s

class DriveTrain:
    def __init__(self, amperage, hover_thrust, max_thrust, motor, prop, battery, number_of_batteries):
        self.amperage = amperage
        self.hover_thrust = hover_thrust
        self.max_thrust = max_thrust
        self.motor = motor
        self.prop = prop
        self.battery = battery
        self.number_of_batteries = number_of_batteries
        self.weight = self.motor.weight * 4 + self.prop.weight * self.prop.blades * 4 + self.battery.weight * self.number_of_batteries
        self.useful_thrust = self.hover_thrust - self.weight
        self.endurance = ((self.battery.capacity * self.number_of_batteries * 0.8) / (self.amperage * 1000)) * 60
        self.cost = self.motor.cost * 4 + self.prop.cost * 4 + self.battery.cost * self.number_of_batteries



# Example usage:
# motors = parse_motor_data_from_tsv('motors.tsv')
# for motor in motors:
#     print(motor)
# print(to_valid_variable_name("123 Invalid Name!"))
# plot_drivetrain_3d(drivetrains)
