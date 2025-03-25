
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import hashlib
import math
from typing import List


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

    def weight(self):
        return self.motor_weight*4 + self.propeller_weight_per_blade*8

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
        self.specific_energy = self.capacity_watt_hours / self.weight
        self.cost_specific_energy = self.capacity_watt_hours / (self.cost+0.0001)

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

    def battery_weight(self):
        return self.battery.weight * self.number_of_batteries

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

    def drag_force(self, velocity, frontal_area=0.25, Cd=0.6, air_density=1.293):
        '''
        frontal area in m2
        velocity in m/s
        returns Drag Force in N
        '''
        drag_newtons = 0.5*Cd*air_density*(velocity**2)*frontal_area
        drag_kgs = drag_newtons / 9.81
        drag_grams = drag_kgs * 1000
        return drag_grams

    def thrust_for_cruise(self, cruise_velocity):
        thrust = math.sqrt(self.drag_force(cruise_velocity)**2 + self.weight()**2)
        return thrust

    def available_payload_at_cruise(self, thrust_to_weight_ratio, cruise_velocity):
        available_thrust = (self.max_thrust() / thrust_to_weight_ratio) * 4
        angle = math.atan(self.drag_force(cruise_velocity)/self.weight())  # radians
        total_weight = math.cos(angle)*available_thrust
        available_payload = total_weight - self.weight()
        return available_payload

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

    # def carpet_plot_Cd(self):
    #     # Define the range of thrust_to_weight_ratio
    #     thrust_to_weight_ratios = np.linspace(1.2, 2.2, 10)  # Adjust the range and number of points as needed
    #     Cd_values = np.linspace(0.4,0.75,10)
    #     fig, ax = plt.subplots()
    #     ax.set_ylim([0,20000])
    #     ax.set_xlim([0,60])

    #     # Create a grid for endurance and hover thrust for all drone configurations
    #     endurance = []
    #     available_payload_at_cruise = []
    #     for ratio in thrust_to_weight_ratios:
    #         endurance.append(self.naive_endurance(thrust_to_weight_ratio=ratio))
    #         available_payload_at_cruise.append(self.available_payload_at_cruise(thrust_to_weight_ratio=ratio, cruise_velocity=10))

    #     # Create a carpet plot (or line plot) with thrust_to_weight_ratio as the third variable
    #     plt.plot(endurance, available_payload_at_cruise, label=f'{self.id}')
    #     plt.scatter(endurance, available_payload_at_cruise, c=thrust_to_weight_ratios, cmap='viridis', s=10)  # Color by thrust_to_weight_ratio

    #     # Add labels and legend
    #     plt.colorbar(label="Thrust-to-Weight Ratio")
    #     plt.xlabel("Naive Endurance [min.]")
    #     plt.ylabel("Available Payload at Cruise [g]")
    #     # plt.legend(title="Drone Configurations")
    #     plt.title("Carpet Plot of Endurance vs. Available payload at cruise")
    #     plt.show()

    def carpet_plot_Cd(self):
        # Define the range of thrust_to_weight_ratio and Cd values
        thrust_to_weight_ratios = np.linspace(1.2, 2.2, 10)  # Adjust the range and number of points as needed
        Cd_values = np.linspace(0.4, 0.75, 10)
        fig, ax = plt.subplots()
        ax.set_ylim([0, 20000])
        ax.set_xlim([0, 60])

        # Create lists for endurance and available payload at cruise
        endurance = []
        available_payload_at_cruise = []
        Cd_data = []

        for Cd in Cd_values:
            for ratio in thrust_to_weight_ratios:
                self.drag_force = lambda v: 0.5 * Cd * 1.293 * \
                    (v**2) * 0.25 / 9.81 * 1000  # Modify drag function dynamically
                endurance.append(self.naive_endurance(thrust_to_weight_ratio=ratio))
                available_payload_at_cruise.append(self.available_payload_at_cruise(
                    thrust_to_weight_ratio=ratio, cruise_velocity=10))
                Cd_data.append(Cd)

        # Create a carpet plot with Cd as an additional variable
        scatter = plt.scatter(endurance, available_payload_at_cruise, c=Cd_data,
                              cmap='plasma', s=10)  # Color by Cd value
        plt.colorbar(scatter, label="Drag Coefficient (Cd)")
        plt.xlabel("Naive Endurance [min.]")
        plt.ylabel("Available Payload at Cruise [g]")
        plt.title("Carpet Plot of Endurance vs. Available Payload at Cruise with Cd Variation")
        plt.show()

    def carpet_plot_velocity(self):
        # Define the range of thrust_to_weight_ratio and Cd values
        thrust_to_weight_ratios = np.linspace(1.2, 2.2, 10)  # Adjust the range and number of points as needed
        velocity_values = np.linspace(10, 50, 100)
        fig, ax = plt.subplots()
        ax.set_ylim([0, 20000])
        ax.set_xlim([0, 60])

        # Create lists for endurance and available payload at cruise
        endurance = []
        available_payload_at_cruise = []
        velocity_data = []

        for velocity in velocity_values:
            for ratio in thrust_to_weight_ratios:
                self.drag_force = lambda v: 0.5 * 0.5 * 1.293 * \
                    (velocity**2) * 0.25 / 9.81 * 1000  # Modify drag function dynamically
                endurance.append(self.naive_endurance(thrust_to_weight_ratio=ratio))
                available_payload_at_cruise.append(self.available_payload_at_cruise(
                    thrust_to_weight_ratio=ratio, cruise_velocity=velocity))
                velocity_data.append(velocity)

        # Create a carpet plot with Cd as an additional variable
        scatter = plt.scatter(endurance, available_payload_at_cruise, c=velocity_data,
                              cmap='plasma', s=10)  # Color by Cd value
        plt.colorbar(scatter, label="Cruise Velocity (m/s)")
        plt.xlabel("Naive Endurance [min.]")
        plt.ylabel("Available Payload at Cruise [g]")
        plt.title("Carpet Plot of Endurance vs. Available Payload at Cruise with Velocity Variation")
        plt.show()

    def summary(self, carpetPlot=False):
        print(self.weight())
        print(self.total_available_weight_capacity())

        print(self.drivetrain.weight())
        print(self.battery_weight())
        print(self.max_thrust()*4)
        if carpetPlot:
            self.carpet_plot_Cd()

    def get_battery_configuration(self, batteries, target_capacity):
        ''' Finds an optimal battery configuration

        Args:
            batteries: A list of available batteries List[Battery]
            target capacity: The target capacity we are trying to reach. float.

        Returns:
            A list of batteries that meet the target capacity while minimizing weight. 
        '''
        # Sort batteries by capacity_watt_hours in descending order
        batteries.sort(key=lambda x: x.capacity_watt_hours, reverse=True)

        battery_config = []
        current_capacity = 0

        for battery in batteries:
            if battery.cell_count == 6:
                diff = target_capacity - current_capacity
                if diff < 0:
                    break
                if diff > 0:
                    viable_number_of_batteries = math.floor(diff / battery.capacity_watt_hours)
                    if viable_number_of_batteries > 0:
                        for i in range(viable_number_of_batteries):
                            battery_config.append(battery)
                            current_capacity += battery.capacity_watt_hours

        return battery_config

    def drone_summary_given_battery_config(self, battery_config, thrust_to_weight_ratio, velocity):
        naive_endurance = 0

        total_battery_capacity_watt_hours = 0
        total_battery_cost = 0
        total_battery_weight = 0

        for battery in battery_config:
            fudge_factor = 0.8
            battery_capacity = battery.capacity_watt_hours * fudge_factor
            naive_endurance += (battery_capacity / self.ideal_total_power_setting(thrust_to_weight_ratio))*60
            total_battery_capacity_watt_hours += battery.capacity_watt_hours
            total_battery_cost += battery.cost
            total_battery_weight += battery.weight

        def weight():
            motor_and_prop_weight = (self.drivetrain.motor_weight +
                                     self.drivetrain.propeller_weight_per_blade*self.drivetrain.propeller_configuration)*4
            return motor_and_prop_weight + total_battery_weight

        def available_payload_at_cruise():
            available_thrust = (self.max_thrust() / thrust_to_weight_ratio) * 4
            angle = math.atan(self.drag_force(velocity)/weight())  # radians
            total_weight = math.cos(angle)*available_thrust
            available_payload = total_weight - weight()
            return available_payload

        return available_payload_at_cruise(), naive_endurance


class BatteryConfiguration:
    def __init__(self, name, batteries: List[Battery]):
        self.name = name
        self.batteries = batteries

    def weight(self):
        return sum(battery.weight for battery in self.batteries)

    def average_weight(self):
        return self.weight() / len(self.batteries)

    def number_of_batteries(self):
        return len(self.batteries)

    def total_waste_weight(self, waste_weight_per_battery):
        return self.number_of_batteries()*waste_weight_per_battery

    def useful_weight(self, waste_weight_per_battery):
        return self.weight() - self.total_waste_weight(waste_weight_per_battery)

    def weight_efficiency(self, waste_weight_per_battery):
        return waste_weight_per_battery / self.average_weight()


large_batteries = BatteryConfiguration("large batteries", [
    Battery("Turnigy High Capacity 20000mAh 6S 12C Lipo Pack w/XT90", 2630, 302.28, 22.2, 6, 20000),
    Battery("Turnigy High Capacity 20000mAh 6S 12C Lipo Pack w/XT90", 2630, 302.28, 22.2, 6, 20000),
    Battery("Turnigy High Capacity 14000mAh 6S 12C Lipo Pack w/XT90", 1820, 212.27, 22.2, 6, 14000)
])

small_batteries = BatteryConfiguration("small batteries", [
    Battery("Turnigy 4500mAh 6S 30C Lipo Pack w/XT-90", 745, 61.83, 22.2, 6, 4500),
    Battery("Turnigy 4500mAh 6S 30C Lipo Pack w/XT-90", 745, 61.83, 22.2, 6, 4500),
    Battery("Turnigy 4500mAh 6S 30C Lipo Pack w/XT-90", 745, 61.83, 22.2, 6, 4500),
    Battery("Turnigy 4500mAh 6S 30C Lipo Pack w/XT-90", 745, 61.83, 22.2, 6, 4500),
    Battery("Turnigy 4500mAh 6S 30C Lipo Pack w/XT-90", 745, 61.83, 22.2, 6, 4500),
    Battery("Turnigy 4500mAh 6S 30C Lipo Pack w/XT-90", 745, 61.83, 22.2, 6, 4500),
    Battery("Turnigy 4500mAh 6S 30C Lipo Pack w/XT-90", 745, 61.83, 22.2, 6, 4500),
    Battery("Turnigy 4500mAh 6S 30C Lipo Pack w/XT-90", 745, 61.83, 22.2, 6, 4500),
    Battery("Turnigy 4500mAh 6S 30C Lipo Pack w/XT-90", 745, 61.83, 22.2, 6, 4500),
    Battery("Turnigy 4500mAh 6S 30C Lipo Pack w/XT-90", 745, 61.83, 22.2, 6, 4500),
    Battery("Turnigy 4500mAh 6S 30C Lipo Pack w/XT-90", 745, 61.83, 22.2, 6, 4500)
])


class BatteryComparison:
    def __init__(self, configurations: List[BatteryConfiguration]):
        self.configurations = configurations

    def compare_makeup(self, per_battery_waste_weight):
        conf1 = self.configurations[0]
        conf2 = self.configurations[1]

        weight_dist = {
            'Useful': np.array([conf1.useful_weight(per_battery_waste_weight), conf2.useful_weight(per_battery_waste_weight)]),
            'Waste': np.array([conf1.total_waste_weight(per_battery_waste_weight), conf2.total_waste_weight(per_battery_waste_weight)]),
        }

        # plt.bar([0, 1], [conf1.weight(), conf2.weight()],  color=['r', 'b'], label=[conf1.name, conf2.name])
        plt.bar([0, 1], weight_dist['Useful'])
        plt.bar([0, 1], weight_dist['Waste'], color='r')
        plt.xlabel = 'configuration'
        plt.ylabel = 'weight [g]'
        plt.legend()
        plt.show()

    def test_efficiency(self, waste_weight_per_battery_range):
        conf1 = self.configurations[0]
        conf2 = self.configurations[1]
        effs1 = []
        effs2 = []
        diff = []
        for waste_weight in waste_weight_per_battery_range:
            effs1.append(conf1.weight_efficiency(waste_weight))
            effs2.append(conf2.weight_efficiency(waste_weight))
            diff.append(conf1.weight_efficiency(waste_weight) - conf2.weight_efficiency(waste_weight))

        plt.plot(waste_weight_per_battery_range, effs1, label=conf1.name)
        plt.plot(waste_weight_per_battery_range, effs2, label=conf2.name)
        plt.plot(waste_weight_per_battery_range, diff, label="efficiency difference", color='r')
        plt.legend()
        plt.ylabel("Weight Efficiency (waste weight/average battery weight)")
        plt.xlabel("Assumed weight of cables + connectors per battery")
        plt.show()


large_vs_small = BatteryComparison([small_batteries, large_batteries])

if __name__ == "__main__":
    large_vs_small.compare_makeup(50)
    # large_vs_small.test_efficiency(np.linspace(1, 500, 10))
