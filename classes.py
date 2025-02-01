
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import hashlib


class DrivetrainData:
    def __init__(self, motor, propeller, motor_weight, propeller_weight_per_blade,
                 propeller_configuration, motor_cost, propeller_cost, battery_voltage, cell_count):
        self.motor = motor
        self.propeller = propeller
        self.motor_weight = motor_weight
        self.propeller_weight_per_blade = propeller_weight_per_blade
        self.propeller_configuration = propeller_configuration
        self.motor_cost = motor_cost
        self.propeller_cost = propeller_cost
        self.battery_voltage = battery_voltage
        self.cell_count = cell_count
        self.performance_data = []  # List of PerformanceData objects

    def add_performance_data(self, throttle, power, thrust):
        self.performance_data.append(PerformanceData(throttle, power, thrust))
        
    def cost(self):
        return self.motor_cost*4 + self.propeller_cost*4

    def plot_performance_data(self):
        performance_data = self.performance_data
        # Extract throttle percentages and thrust values
        throttle = [data.throttle for data in performance_data]
        thrust = [data.thrust for data in performance_data]

        # Create the plot
        plt.figure(figsize=(8, 6))
        plt.plot(throttle, thrust, marker='o', linestyle='-', color='b', label='Thrust vs Throttle')

        # Add labels and title
        plt.xlabel('Throttle (%)', fontsize=12)
        plt.ylabel('Thrust (g)', fontsize=12)
        plt.title('Performance Data: Throttle vs Thrust', fontsize=14)

        # Approximation
        interpolation_func_quadratic = interp1d(throttle, thrust, kind='quadratic', fill_value="extrapolate")
        x_values = np.linspace(0, 100, 100)
        plt.plot(x_values, interpolation_func_quadratic(x_values),
                 linestyle='--', color='k', label='Approximation quadratic')

        # Add grid and legend
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(fontsize=10)

        # Show the plot
        plt.tight_layout()
        plt.show()

    def __repr__(self):
        return (f"DrivetrainData(motor={self.motor}, propeller={self.propeller}, motor_weight={self.motor_weight}, "
                f"propeller_weight_per_blade={self.propeller_weight_per_blade}, "
                f"propeller_configuration={self.propeller_configuration}, motor_cost={self.motor_cost}, "
                f"propeller_cost={self.propeller_cost}, battery_voltage={self.battery_voltage}, "
                f"performance_data={self.performance_data})")


class PerformanceData:
    def __init__(self, throttle, power, thrust):
        self.throttle = throttle
        self.power = power
        self.thrust = thrust

    def __repr__(self):
        return f"PerformanceData(throttle={self.throttle}, power={self.power}, thrust={self.thrust})"


class Battery:
    def __init__(self, name, weight, cost, voltage, cell_count, capacity_milliamp_hours):
        self.name = name
        self.weight = weight
        self.cost = cost
        self.voltage = voltage
        self.cell_count = cell_count
        self.capacity_milliamp_hours = capacity_milliamp_hours
        self.capacity_watt_hours = (capacity_milliamp_hours / 1000) * voltage

    def __repr__(self):
        return (f"Battery(name={self.name}, weight={self.weight}, cost={self.cost}, "
                f"voltage={self.voltage}, capacity_milliamp_hours={self.capacity_milliamp_hours}, "
                f"capacity_watt_hours={self.capacity_watt_hours:.2f})")


class DroneConfiguration:
    def __init__(self, drivetrain: DrivetrainData, battery: Battery, number_of_batteries):
        self.drivetrain = drivetrain
        self.battery = battery
        self.number_of_batteries = number_of_batteries
        # Generate a unique ID by concatenating key attributes and hashing it
        id_string = f"{drivetrain.motor}_{drivetrain.propeller}_{battery.name}_{number_of_batteries}"

        # Create a hash from the concatenated string
        # Taking only the first 8 characters for brevity
        self.id = hashlib.md5(id_string.encode('utf-8')).hexdigest()[:8]
        
    def __repr__(self):
        return (f"DroneConfiguration(id={self.id}, "
                f"drivetrain=({self.drivetrain}), "
                f"battery=({self.battery}), "
                f"number_of_batteries={self.number_of_batteries})")
        
    def cost(self):
        return self.drivetrain.cost() + self.battery.cost * self.number_of_batteries

    def max_thrust(self):
        '''
        returns: max thrust of a single motor
        '''
        self.drivetrain.performance_data.sort(key=lambda x: x.thrust, reverse=True)
        return self.drivetrain.performance_data[0].thrust

    def interpolate_thrust_from_throttle(self, throttle_setting):
        throttle = np.array([data.throttle for data in self.drivetrain.performance_data])
        thrust = np.array([data.thrust for data in self.drivetrain.performance_data])
        interpolation_func = interp1d(throttle, thrust, kind='linear', fill_value="extrapolate")
        return interpolation_func(throttle_setting)

    def interpolate_power_from_throttle(self, throttle_setting):
        throttle = np.array([data.throttle for data in self.drivetrain.performance_data])
        power = np.array([data.power for data in self.drivetrain.performance_data])
        interpolation_func = interp1d(throttle, power, kind='linear', fill_value="extrapolate")
        return interpolation_func(throttle_setting)

    def interpolate_throttle_from_thrust(self, thrust_setting):
        throttle = np.array([data.throttle for data in self.drivetrain.performance_data])
        thrust = np.array([data.thrust for data in self.drivetrain.performance_data])
        interpolation_func = interp1d(thrust, throttle, kind='linear', fill_value="extrapolate")
        return interpolation_func(thrust_setting)

    def ideal_throttle_setting(self, thrust_to_weight_ratio):
        target_thrust = self.max_thrust() / thrust_to_weight_ratio
        return self.interpolate_throttle_from_thrust(target_thrust)

    def ideal_total_power_setting(self, thrust_to_weight_ratio):
        return self.interpolate_power_from_throttle(self.ideal_throttle_setting(thrust_to_weight_ratio))*4

    def weight(self):
        motor_and_prop_weight = (self.drivetrain.motor_weight +
                                 self.drivetrain.propeller_weight_per_blade*self.drivetrain.propeller_configuration)*4
        battery_weight = self.battery.weight*self.number_of_batteries
        return motor_and_prop_weight + battery_weight

    def total_hover_thrust(self, thrust_to_weight_ratio):
        '''
        returns: hover thrust (defined by thrust to weight ratio) of all four motors combined
        '''
        individual_hover_thrust = self.interpolate_thrust_from_throttle(
            self.ideal_throttle_setting(thrust_to_weight_ratio))
        return individual_hover_thrust*4

    def total_useful_hover_thrust(self, thrust_to_weight_ratio):
        return self.total_hover_thrust(thrust_to_weight_ratio) - self.weight()
    
    def total_available_weight_capacity(self):
        '''
        drone is capped at 15kg MTOW
        '''
        return 15000 - self.weight()

    def naive_endurance(self, thrust_to_weight_ratio):
        '''
        returns: naive endurance estimate in minutes
        '''
        fudge_factor = 0.8
        total_battery_capacity = self.battery.capacity_watt_hours * self.number_of_batteries * fudge_factor
        return (total_battery_capacity / self.ideal_total_power_setting(thrust_to_weight_ratio))*60

    def plot_endurance_vs_useful_thrust(self, thrust_to_weight_ratio):
        # Create the plot
        plt.figure(figsize=(8, 6))
        plt.scatter(self.naive_endurance(thrust_to_weight_ratio), self.total_useful_hover_thrust(
            thrust_to_weight_ratio), marker='o', linestyle='-', color='b', label=f'{self.id}')

        # Add labels and title
        plt.xlabel('Endurance [min.]', fontsize=12)
        plt.ylabel('Useful Thrust (g)', fontsize=12)
        plt.title('Performance Data: Endurance vs. Useful Thrust', fontsize=14)

        # Add grid and legend
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(fontsize=10)

        print(self)
        # Show the plot
        plt.tight_layout()
        plt.show()