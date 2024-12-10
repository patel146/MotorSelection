import pprint
import csv

class PhysicalComponent:
    def __init__(self, weight: float, cost: float, name: str):
        self.weight = weight  # Weight in grams
        self.cost = cost      # Cost in dollars
        self.name = name

# Define a Motor as a subclass of PhysicalComponent
class Motor(PhysicalComponent):
    def __init__(self, weight: float, cost: float, name: str):
        super().__init__(weight, cost, name)  # Initialize weight and cost from PhysicalComponent  
        self.weight = weight*4

# Define Propeller as a subclass of PhysicalComponent
class Propeller(PhysicalComponent):
    def __init__(self, weight_per_blade: float, cost: float, number_of_blades: int, name: str):
        super().__init__(weight_per_blade, cost, name)
        self.weight = weight_per_blade * number_of_blades * 4

# Define Battery as a subclass of PhysicalComponent
class Battery(PhysicalComponent):
    def __init__(self, weight: float, cost: float, capacity: float, number_of_cells: int, name: str):
        super().__init__(weight, cost, name)
        self.capacity = capacity  # Capacity in mAh
        self.number_of_cells = number_of_cells # 4s, 6s etc.
        self.voltage = self.number_of_cells * 4.2    # Voltage in volts

# Define DriveTrain with type hints
class DriveTrain:
    def __init__(self, motor: Motor, prop: Propeller, battery: Battery, thrust: float, amperage: float):
        self.motor = motor
        self.prop = prop
        self.battery = battery
        self.components = [motor,prop,battery]
        self.amperage = amperage
        self.weight = sum(component.weight for component in self.components)
        self.cost = sum(component.cost for component in self.components)
        self.thrust = thrust*4 # thrust in grams assuming 75% throttle
        self.useful_thrust = (self.thrust) - self.weight
        self.endurance = ((self.battery.capacity/1000) / (self.amperage*4)) * 60 # gives endurance in minutes 
        
KDE4213XF360 = Motor(230,155,"KDE4213XF360")
DUAL18p5x6p3 = Propeller(18.8,155,2,"DUAL18p5x6p3")
TURNIGY_20x6s = Battery(2630,208.66,20000,6,"TURNIGY_20x6s")

DT1 = DriveTrain(KDE4213XF360,DUAL18p5x6p3,TURNIGY_20x6s,2811,17.9)

pprint.pp(DT1.__dict__)

results_file = "results.csv"

with open(results_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Write each row to the CSV file
    data = [DT1.motor.name,DT1.prop.name,DT1.battery.name,DT1.endurance,DT1.useful_thrust]
    writer.writerow(data)

print(f"Data has been written to {results_file}")