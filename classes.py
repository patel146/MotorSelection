
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

class DrivetrainData:
    def __init__(self, motor, propeller, motor_weight, propeller_weight_per_blade,
                 propeller_configuration, motor_cost, propeller_cost, battery_voltage):
        self.motor = motor
        self.propeller = propeller
        self.motor_weight = motor_weight
        self.propeller_weight_per_blade = propeller_weight_per_blade
        self.propeller_configuration = propeller_configuration
        self.motor_cost = motor_cost
        self.propeller_cost = propeller_cost
        self.battery_voltage = battery_voltage
        self.performance_data = []  # List of PerformanceData objects

    def add_performance_data(self, throttle, power, thrust):
        self.performance_data.append(PerformanceData(throttle, power, thrust))

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
      interpolation_func = interp1d(throttle, thrust, kind='linear', fill_value="extrapolate")
      interpolation_func_quadratic = interp1d(throttle, thrust, kind='quadratic', fill_value="extrapolate")
      x_values = np.linspace(0, 100, 100)
      plt.plot(x_values, interpolation_func(x_values), linestyle='--', color='r', label='Approximation linear')
      plt.plot(x_values, interpolation_func_quadratic(x_values), linestyle='--', color='k', label='Approximation quadratic')
      
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
