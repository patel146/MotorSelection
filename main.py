import pprint
import csv
import matplotlib.pyplot as plt

drivetrains = []

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
    def __init__(self, motor: Motor, prop: Propeller, battery: Battery, thrust: float, amperage: float, max_thrust: float):
        self.motor = motor
        self.prop = prop
        self.battery = battery
        self.components = [motor,prop,battery]
        self.amperage = amperage
        self.weight = sum(component.weight for component in self.components)
        self.cost = sum(component.cost for component in self.components)
        self.thrust = thrust*4 # thrust in grams assuming 75% throttle
        self.useful_thrust = (self.thrust) - self.weight
        self.endurance = ((self.battery.capacity*0.8/1000) / (self.amperage*4)) * 60 # gives endurance in minutes 
        self.max_thrust = max_thrust
        self.thrust_to_weight_ratio =  (self.max_thrust * 4) / self.thrust
        drivetrains.append(self)
        
KDE4213XF360 = Motor(230,155,"KDE4213XF360")
KDE4215XF465 = Motor(250,180,"KDE4215XF465")
KDE5215XF435 = Motor(305,245,"KDE5215XF435")

DUAL18p5x6p3 = Propeller(18.8,155,2,"DUAL18p5x6p3")
TRIPLE18p5x6p3 = Propeller(18.8,230,3,"TRIPLE18p5x6p3")
DUAL15p5x5p3 = Propeller(14.7,175,2,"DUAL15p5x5p3")

TURNIGY_20x6s = Battery(2630,208.66,20000,6,"TURNIGY_20x6s")
DBL_TURNIGY_20x6s = Battery(2630*2,208.66*2,20000*2,6,"DBL_TURNIGY_20x6s")
TURNIGY_16x6s = Battery(2015,170,16000,6,"TURNIGY_16x6s")
DBL_TURNIGY_16x6s = Battery(2015*2,170*2,16000*2,6,"DBL_TURNIGY_16x6s")
TURNIGY_20x4s = Battery(1775,155,20000,4,"TURNIGY_20x4s")
DBL_TURNIGY_20x4s = Battery(1775*2,155*2,20000*2,4,"DBL_TURNIGY_20x4s")

DT1 = DriveTrain(KDE4213XF360,DUAL18p5x6p3,TURNIGY_20x6s,2811,17.9,4035)

DT2 = DriveTrain(Motor(230,155,"KDE4213XF360"),
                 Propeller(18.8,230,3,"TRIPLE18p5x6p3"),
                 TURNIGY_20x6s,
                 3064,
                 21.6,
                 4320)

DT3 = DriveTrain(KDE4215XF465,
                 DUAL18p5x6p3,
                 TURNIGY_20x6s,
                 4250,
                 36.9,
                 5608)

DT4 = DriveTrain(KDE4215XF465,
                 DUAL15p5x5p3,
                 TURNIGY_20x6s,
                 3124,
                 23.7,
                 4691)

DT4 = DriveTrain(KDE5215XF435,
                 DUAL18p5x6p3,
                 TURNIGY_20x6s,
                 5077,
                 41.8,
                 7279)

DT4 = DriveTrain(KDE5215XF435,
                 DUAL15p5x5p3,
                 TURNIGY_20x6s,
                 3320,
                 26.5,
                 5227)

DT1p1 = DriveTrain(KDE4213XF360,DUAL18p5x6p3,DBL_TURNIGY_20x6s,2811,17.9,4035)

DT2p1 = DriveTrain(Motor(230,155,"KDE4213XF360"),
                 Propeller(18.8,230,3,"TRIPLE18p5x6p3"),
                 DBL_TURNIGY_20x6s,
                 3064,
                 21.6,
                 4320)

DT3p1 = DriveTrain(KDE4215XF465,
                 DUAL18p5x6p3,
                 DBL_TURNIGY_20x6s,
                 4250,
                 36.9,
                 5608)

DT4p1 = DriveTrain(KDE4215XF465,
                 DUAL15p5x5p3,
                 DBL_TURNIGY_20x6s,
                 3124,
                 23.7,
                 4691)

DT5p1 = DriveTrain(KDE5215XF435,
                 DUAL18p5x6p3,
                 DBL_TURNIGY_20x6s,
                 5077,
                 41.8,
                 7279)

DT6p1 = DriveTrain(KDE5215XF435,
                 DUAL15p5x5p3,
                 DBL_TURNIGY_20x6s,
                 3320,
                 26.5,
                 5227)

DT1 = DriveTrain(KDE4213XF360,DUAL18p5x6p3,TURNIGY_16x6s,2811,17.9,4035)

DT2 = DriveTrain(Motor(230,155,"KDE4213XF360"),
                 Propeller(18.8,230,3,"TRIPLE18p5x6p3"),
                 TURNIGY_16x6s,
                 3064,
                 21.6,
                 4320)

DT3 = DriveTrain(KDE4215XF465,
                 DUAL18p5x6p3,
                 TURNIGY_16x6s,
                 4250,
                 36.9,
                 5608)

DT4 = DriveTrain(KDE4215XF465,
                 DUAL15p5x5p3,
                 TURNIGY_16x6s,
                 3124,
                 23.7,
                 4691)

DT4 = DriveTrain(KDE5215XF435,
                 DUAL18p5x6p3,
                 TURNIGY_16x6s,
                 5077,
                 41.8,
                 7279)

DT4 = DriveTrain(KDE5215XF435,
                 DUAL15p5x5p3,
                 TURNIGY_16x6s,
                 3320,
                 26.5,
                 5227)

DT1p1 = DriveTrain(KDE4213XF360,DUAL18p5x6p3,DBL_TURNIGY_16x6s,2811,17.9,4035)

DT2p1 = DriveTrain(Motor(230,155,"KDE4213XF360"),
                 Propeller(18.8,230,3,"TRIPLE18p5x6p3"),
                 DBL_TURNIGY_16x6s,
                 3064,
                 21.6,
                 4320)

DT3p1 = DriveTrain(KDE4215XF465,
                 DUAL18p5x6p3,
                 DBL_TURNIGY_16x6s,
                 4250,
                 36.9,
                 5608)

DT4p1 = DriveTrain(KDE4215XF465,
                 DUAL15p5x5p3,
                 DBL_TURNIGY_16x6s,
                 3124,
                 23.7,
                 4691)

DT5p1 = DriveTrain(KDE5215XF435,
                 DUAL18p5x6p3,
                 DBL_TURNIGY_16x6s,
                 5077,
                 41.8,
                 7279)

DT6p1 = DriveTrain(KDE5215XF435,
                 DUAL15p5x5p3,
                 DBL_TURNIGY_16x6s,
                 3320,
                 26.5,
                 5227)

DT1 = DriveTrain(KDE4213XF360,DUAL18p5x6p3,TURNIGY_20x6s,2811,17.9,4035)

DT2 = DriveTrain(Motor(230,155,"KDE4213XF360"),
                 Propeller(18.8,230,3,"TRIPLE18p5x6p3"),
                 TURNIGY_20x6s,
                 3064,
                 21.6,
                 4320)

DT3 = DriveTrain(KDE4215XF465,
                 DUAL18p5x6p3,
                 TURNIGY_20x6s,
                 4250,
                 36.9,
                 5608)

DT4 = DriveTrain(KDE4215XF465,
                 DUAL15p5x5p3,
                 TURNIGY_20x6s,
                 3124,
                 23.7,
                 4691)

DT4 = DriveTrain(KDE5215XF435,
                 DUAL18p5x6p3,
                 TURNIGY_20x6s,
                 5077,
                 41.8,
                 7279)

DT4 = DriveTrain(KDE5215XF435,
                 DUAL15p5x5p3,
                 TURNIGY_20x6s,
                 3320,
                 26.5,
                 5227)

DT1p1 = DriveTrain(KDE4213XF360,DUAL18p5x6p3,DBL_TURNIGY_20x6s,2811,17.9,4035)

DT2p1 = DriveTrain(Motor(230,155,"KDE4213XF360"),
                 Propeller(18.8,230,3,"TRIPLE18p5x6p3"),
                 DBL_TURNIGY_20x6s,
                 3064,
                 21.6,
                 4320)

DT3p1 = DriveTrain(KDE4215XF465,
                 DUAL18p5x6p3,
                 DBL_TURNIGY_20x6s,
                 4250,
                 36.9,
                 5608)

DT4p1 = DriveTrain(KDE4215XF465,
                 DUAL15p5x5p3,
                 DBL_TURNIGY_20x6s,
                 3124,
                 23.7,
                 4691)

DT5p1 = DriveTrain(KDE5215XF435,
                 DUAL18p5x6p3,
                 DBL_TURNIGY_20x6s,
                 5077,
                 41.8,
                 7279)

DT6p1 = DriveTrain(KDE5215XF435,
                 DUAL15p5x5p3,
                 DBL_TURNIGY_20x6s,
                 3320,
                 26.5,
                 5227)

DT1 = DriveTrain(KDE4213XF360,DUAL18p5x6p3,TURNIGY_20x4s,2811,17.9,4035)

DT2 = DriveTrain(Motor(230,155,"KDE4213XF360"),
                 Propeller(18.8,230,3,"TRIPLE18p5x6p3"),
                 TURNIGY_20x4s,
                 3064,
                 21.6,
                 4320)

DT3 = DriveTrain(KDE4215XF465,
                 DUAL18p5x6p3,
                 TURNIGY_20x4s,
                 4250,
                 36.9,
                 5608)

DT4 = DriveTrain(KDE4215XF465,
                 DUAL15p5x5p3,
                 TURNIGY_20x4s,
                 3124,
                 23.7,
                 4691)

DT4 = DriveTrain(KDE5215XF435,
                 DUAL18p5x6p3,
                 TURNIGY_20x4s,
                 5077,
                 41.8,
                 7279)

DT4 = DriveTrain(KDE5215XF435,
                 DUAL15p5x5p3,
                 TURNIGY_20x4s,
                 3320,
                 26.5,
                 5227)

DT1p1 = DriveTrain(KDE4213XF360,DUAL18p5x6p3,DBL_TURNIGY_20x4s,2811,17.9,4035)

DT2p1 = DriveTrain(Motor(230,155,"KDE4213XF360"),
                 Propeller(18.8,230,3,"TRIPLE18p5x6p3"),
                 DBL_TURNIGY_20x4s,
                 3064,
                 21.6,
                 4320)

DT3p1 = DriveTrain(KDE4215XF465,
                 DUAL18p5x6p3,
                 DBL_TURNIGY_20x4s,
                 4250,
                 36.9,
                 5608)

DT4p1 = DriveTrain(KDE4215XF465,
                 DUAL15p5x5p3,
                 DBL_TURNIGY_20x4s,
                 3124,
                 23.7,
                 4691)

DT5p1 = DriveTrain(KDE5215XF435,
                 DUAL18p5x6p3,
                 DBL_TURNIGY_20x4s,
                 5077,
                 41.8,
                 7279)

DT6p1 = DriveTrain(KDE5215XF435,
                 DUAL15p5x5p3,
                 DBL_TURNIGY_20x4s,
                 3320,
                 26.5,
                 5227)


pprint.pp(DT1.__dict__)

results_file = "results.csv"

data = []

for dt in drivetrains:
    data.append([dt.motor.name,dt.prop.name,dt.battery.name,dt.endurance,dt.useful_thrust,dt.thrust_to_weight_ratio])

with open(results_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Write each row to the CSV file

    writer.writerows(data)
    
def plot_last_two_columns(csv_file_path):
    """
    Reads a CSV file, extracts the last two columns, and plots them on an x-y plot.
    
    Args:
        csv_file_path (str): Path to the CSV file.
    """
    x_data = []
    y_data = []
    
    # Read the CSV file
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 2:
                continue  # Skip rows that don't have enough columns
            # Extract the last two columns
            x_data.append(float(row[-3]))
            y_data.append(float(row[-2]))
    
    # Plot the data
    plt.figure(figsize=(8, 6))
    plt.scatter(x_data, y_data)
    plt.xlabel('Endurance [min]')
    plt.ylabel('Useful Thrust [g]')
    plt.title('Useful Thrust vs Endurance')
    plt.legend()
    plt.grid(True)
    plt.show()
    

print(f"Data has been written to {results_file}")
plot_last_two_columns('results.csv')