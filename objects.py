import csv
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from typing import List

class Component:
    def __init__(self, link, name, weight, cost):
        self.link = link
        self.name = name
        self.weight = weight
        self.cost = cost

    def __repr__(self):
        return f"Component(name='{self.name}', weight={self.weight}g, cost={self.cost} CAD)"
    
class Battery(Component):
    def __init__(self, link, name, weight, cost,capacity):
        super().__init__(link, name, weight, cost)
        self.capacity = capacity
        
class Propeller(Component):
    def __init__(self, link, name, weight, cost, blades):
        super().__init__(link, name, weight, cost)
        self.blades = blades
        

KDE4014XF_380 = Component('https://www.kdedirect.com/collections/uas-multi-rotor-brushless-motors/products/kde4014xf-380', 'KDE4014XF-380', 215.0, 198.36)
KDE4213XF_360 = Component('https://www.kdedirect.com/collections/uas-multi-rotor-brushless-motors/products/KDE4213XF-360', 'KDE4213XF-360', 230.0, 219.61)
KDE4215XF_465 = Component('https://www.kdedirect.com/collections/uas-multi-rotor-brushless-motors/products/KDE4215XF-465', 'KDE4215XF-465', 250.0, 255.04)
KDE5215XF_220 = Component('https://www.kdedirect.com/collections/uas-multi-rotor-brushless-motors/products/KDE5215XF-220', 'KDE5215XF-220', 360.0, 361.3)
KDE7208XF_135 = Component('https://www.kdedirect.com/collections/uas-multi-rotor-brushless-motors/products/KDE7208XF-135', 'KDE7208XF-135', 445.0, 559.66)
Turnigy_20000mAh_4S = Battery('https://hobbyking.com/en_us/turnigy-high-capacity-battery-20000mah-4s-12c-drone-lipo-pack-xt90.html', 'Turnigy 20000mAh 4S', 1775.0, 217.82,20000)      
Turnigy_20000mAh_6S = Battery('https://hobbyking.com/en_us/turnigy-high-capacity-battery-20000mah-6s-12c-drone-lipo-pack-xt90.html', 'Turnigy 20000mAh 6S', 2630.0, 296.01,20000)      
Turnigy_16000mAh_6S = Battery('https://hobbyking.com/en_us/turnigy-high-capacity-16000mah-6s-12c-multi-rotor-lipo-pack-w-xt90.html', 'Turnigy 16000mAh 6S', 2015.0, 240.57,16000)      
Turnigy_5000mah_8S = Battery('https://hobbyking.com/en_us/turnigy-nano-tech-5000mah-8s-65-130c-lipo-pack-xt90.html', 'Turnigy 5000mah 8S', 1066.0, 117.46,5000)
_18p5__x_6_3_DUAL_EDN__KDE_ = Propeller('https://www.kdedirect.com/collections/multi-rotor-propeller-blades/products/kde-cf185-dp', '18.5" x 6.3 DUAL‐EDN (KDE)', 37.6, 219.61,2)       
_18p5__x_6_3_TRIPLE_EDN__KDE_ = Propeller('https://www.kdedirect.com/collections/multi-rotor-propeller-blades/products/kde-cf185-tp', '18.5" x 6.3 TRIPLE‐EDN (KDE)', 56.4, 325.88,3)   
_21p5__x_7_3_DUAL_EDN__KDE_ = Propeller('https://www.kdedirect.com/collections/multi-rotor-propeller-blades/products/kde-cf215-dp', '21.5" x 7.3 DUAL‐EDN (KDE)', 51.6, 262.12,2)       
_21p5__x_7_3_TRIPLE_EDN__KDE_ = Propeller('https://www.kdedirect.com/collections/multi-rotor-propeller-blades/products/kde-cf215-tp', '21.5" x 7.3 TRIPLE‐EDN (KDE)', 77.4, 389.64,3)

drivetrains=  []

class DriveTrain:
    def __init__(self,amperage, hover_thrust, max_thrust, motor: Component, prop: Propeller, battery: Battery, id, number_of_batteries):
        self.id = id
        self.amperage = amperage * 4
        self.hover_thrust = hover_thrust * 4
        self.max_thrust = max_thrust * 4
        self.motor = motor
        self.prop = prop
        self.battery = battery
        self.number_of_batteries = number_of_batteries
        self.weight = self.motor.weight*4 + self.prop.weight * self.prop.blades * 4 + self.battery.weight * self.number_of_batteries
        self.useful_thrust = self.hover_thrust - self.weight
        self.thrust_to_weight = self.max_thrust / self.hover_thrust
        self.endurance = ((self.battery.capacity * self.number_of_batteries * 0.8) / (self.amperage*1000))*60
        self.cost = self.motor.cost*4 + self.prop.cost * 4 + self.battery.cost * self.number_of_batteries
        drivetrains.append(self)
        
        
DT_5 = DriveTrain(18.2,2978,4019,KDE4014XF_380,_18p5__x_6_3_DUAL_EDN__KDE_,Turnigy_20000mAh_6S,'5',1)
DT_6 = DriveTrain(22.4,3226,4318,KDE4014XF_380,_18p5__x_6_3_TRIPLE_EDN__KDE_,Turnigy_20000mAh_6S,'6',1)
DT_13 = DriveTrain(10.7,1562,2336,KDE4213XF_360,_18p5__x_6_3_DUAL_EDN__KDE_,Turnigy_20000mAh_4S,'13',1)
DT_14 = DriveTrain(13,1783,2575,KDE4213XF_360,_18p5__x_6_3_TRIPLE_EDN__KDE_,Turnigy_20000mAh_4S,'14',1)
DT_17 = DriveTrain(17.9,2811,4035,KDE4213XF_360,_18p5__x_6_3_DUAL_EDN__KDE_,Turnigy_20000mAh_6S,'17',1)
DT_18 = DriveTrain(21.6,3064,4320,KDE4213XF_360,_18p5__x_6_3_TRIPLE_EDN__KDE_,Turnigy_20000mAh_6S,'18',1)
DT_25 = DriveTrain(21.3,2412,3470,KDE4215XF_465,_18p5__x_6_3_DUAL_EDN__KDE_,Turnigy_20000mAh_4S,'25',2)
DT_26 = DriveTrain(26.1,2732,3837,KDE4215XF_465,_18p5__x_6_3_TRIPLE_EDN__KDE_,Turnigy_20000mAh_4S,'26',1)
DT_29 = DriveTrain(36.9,4250,5608,KDE4215XF_465,_18p5__x_6_3_DUAL_EDN__KDE_,Turnigy_20000mAh_6S,'29',1)
DT_41 = DriveTrain(7.5,1635,2467,KDE5215XF_220,_18p5__x_6_3_DUAL_EDN__KDE_,Turnigy_20000mAh_6S,'41',1)
DT_42 = DriveTrain(9,2016,2967,KDE5215XF_220,_18p5__x_6_3_TRIPLE_EDN__KDE_,Turnigy_20000mAh_6S,'42',1)
DT_43 = DriveTrain(12.6,2705,4012,KDE5215XF_220,_21p5__x_7_3_DUAL_EDN__KDE_,Turnigy_20000mAh_6S,'43',2)
DT_44 = DriveTrain(16.3,3070,4506,KDE5215XF_220,_21p5__x_7_3_TRIPLE_EDN__KDE_,Turnigy_20000mAh_6S,'44',2)
DT_45 = DriveTrain(10.3,2574,3880,KDE5215XF_220,_18p5__x_6_3_DUAL_EDN__KDE_,Turnigy_5000mah_8S,'45',4)
DT_46 = DriveTrain(13.7,3098,4551,KDE5215XF_220,_18p5__x_6_3_TRIPLE_EDN__KDE_,Turnigy_5000mah_8S,'46',4)
DT_47 = DriveTrain(18.5,4097,5955,KDE5215XF_220,_21p5__x_7_3_DUAL_EDN__KDE_,Turnigy_5000mah_8S,'47',4)
DT_48 = DriveTrain(22.4,4595,6495,KDE5215XF_220,_21p5__x_7_3_TRIPLE_EDN__KDE_,Turnigy_5000mah_8S,'48',4)

DT_5x = DriveTrain(18.2,2978,4019,KDE4014XF_380,_18p5__x_6_3_DUAL_EDN__KDE_,Turnigy_16000mAh_6S,'5x',1)
DT_6x = DriveTrain(22.4,3226,4318,KDE4014XF_380,_18p5__x_6_3_TRIPLE_EDN__KDE_,Turnigy_16000mAh_6S,'6x',1)
DT_17x = DriveTrain(17.9,2811,4035,KDE4213XF_360,_18p5__x_6_3_DUAL_EDN__KDE_,Turnigy_16000mAh_6S,'17x',1)
DT_18x = DriveTrain(21.6,3064,4320,KDE4213XF_360,_18p5__x_6_3_TRIPLE_EDN__KDE_,Turnigy_16000mAh_6S,'18x',1)
DT_29x = DriveTrain(36.9,4250,5608,KDE4215XF_465,_18p5__x_6_3_DUAL_EDN__KDE_,Turnigy_16000mAh_6S,'29x',1)
DT_41x = DriveTrain(7.5,1635,2467,KDE5215XF_220,_18p5__x_6_3_DUAL_EDN__KDE_,Turnigy_16000mAh_6S,'41x',2)
DT_42x = DriveTrain(9,2016,2967,KDE5215XF_220,_18p5__x_6_3_TRIPLE_EDN__KDE_,Turnigy_16000mAh_6S,'42x',1)
DT_43x = DriveTrain(12.6,2705,4012,KDE5215XF_220,_21p5__x_7_3_DUAL_EDN__KDE_,Turnigy_16000mAh_6S,'43x',2)
DT_43x2 = DriveTrain(12.6,2705,4012,KDE5215XF_220,_21p5__x_7_3_DUAL_EDN__KDE_,Turnigy_16000mAh_6S,'43x2',3)
DT_44x = DriveTrain(16.3,3070,4506,KDE5215XF_220,_21p5__x_7_3_TRIPLE_EDN__KDE_,Turnigy_16000mAh_6S,'44x',1)
DT_CURRENT = DriveTrain(17.9,2811,4035,KDE4213XF_360,_18p5__x_6_3_DUAL_EDN__KDE_,Turnigy_20000mAh_6S,'C',1)
DT_CURRENTx = DriveTrain(21.6,3064,4320,KDE4213XF_360,_18p5__x_6_3_TRIPLE_EDN__KDE_,Turnigy_20000mAh_6S,'CT',1)
DT_CURRENTy = DriveTrain(17.9,2811,4035,KDE4213XF_360,_18p5__x_6_3_DUAL_EDN__KDE_,Turnigy_20000mAh_6S,'Cy',2)
DT_CURRENTy1 = DriveTrain(21.6,3064,4320,KDE4213XF_360,_18p5__x_6_3_TRIPLE_EDN__KDE_,Turnigy_20000mAh_6S,'CTy',2)
DT_CURRENTz = DriveTrain(17.9,2811,4035,KDE4213XF_360,_18p5__x_6_3_DUAL_EDN__KDE_,Turnigy_16000mAh_6S,'Cz',2)
DT_CURRENTz1 = DriveTrain(21.6,3064,4320,KDE4213XF_360,_18p5__x_6_3_TRIPLE_EDN__KDE_,Turnigy_16000mAh_6S,'CTz',2)


def plot_drivetrain_3d(drivetrains):
    """
    Creates a 3D plot for DriveTrain objects showing useful thrust, endurance, and cost.

    Args:
        drivetrains (list): A list of DriveTrain objects.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    useful_thrust = [dt.useful_thrust for dt in drivetrains]
    endurance = [dt.endurance for dt in drivetrains]
    cost = [dt.cost for dt in drivetrains]

    ax.scatter(useful_thrust, endurance, cost, c='b', marker='o')
    
    for i, dt in enumerate(drivetrains):
        ax.text(useful_thrust[i], endurance[i], cost[i], dt.id, color='black', fontsize=10)
    
    ax.set_xlabel('Useful Thrust (g)')
    ax.set_ylabel('Endurance (minutes)')
    ax.set_zlabel('Cost (CAD)')
    
    plt.title('DriveTrain Performance')
    plt.show()
    
def plot_drivetrain_2d(drivetrains):
    """
    Creates 3 separate 2D plots for DriveTrain objects showing relationships between:
    - Useful Thrust vs Endurance
    - Useful Thrust vs Cost
    - Endurance vs Cost

    Args:
        drivetrains (list): A list of DriveTrain objects.
    """
    useful_thrust = [dt.useful_thrust for dt in drivetrains]
    hover_thrust = [dt.hover_thrust for dt in drivetrains]
    endurance = [dt.endurance for dt in drivetrains]
    cost = [dt.cost for dt in drivetrains]
    ids = [dt.id for dt in drivetrains]

    # Plot 1: Useful Thrust vs Endurance
    plt.figure(figsize=(8, 6))
    plt.scatter(useful_thrust, endurance, c='b', marker='o')
    for i, dt_id in enumerate(ids):
        plt.text(useful_thrust[i], endurance[i], dt_id, color='black', fontsize=10)
    plt.xlabel('Useful Thrust (g)')
    plt.ylabel('Endurance (minutes)')
    plt.title('Useful Thrust vs Endurance')
    plt.grid(True)
    plt.show()
    
    # Plot 1a: Hover Thrust vs Endurance
    plt.figure(figsize=(8, 6))
    plt.scatter(hover_thrust, endurance, c='b', marker='o')
    for i, dt_id in enumerate(ids):
        plt.text(hover_thrust[i], endurance[i], dt_id, color='black', fontsize=10)
    plt.xlabel('Hover Thrust (g)')
    plt.ylabel('Endurance (minutes)')
    plt.title('Hover Thrust vs Endurance')
    plt.grid(True)
    plt.show()

    # Plot 2: Useful Thrust vs Cost
    plt.figure(figsize=(8, 6))
    plt.scatter(useful_thrust, cost, c='g', marker='o')
    for i, dt_id in enumerate(ids):
        plt.text(useful_thrust[i], cost[i], dt_id, color='black', fontsize=10)
    plt.xlabel('Useful Thrust (g)')
    plt.ylabel('Cost (CAD)')
    plt.title('Useful Thrust vs Cost')
    plt.grid(True)
    plt.show()

    # Plot 3: Endurance vs Cost
    plt.figure(figsize=(8, 6))
    plt.scatter(endurance, cost, c='r', marker='o')
    for i, dt_id in enumerate(ids):
        plt.text(endurance[i], cost[i], dt_id, color='black', fontsize=10)
    plt.xlabel('Endurance (minutes)')
    plt.ylabel('Cost (CAD)')
    plt.title('Endurance vs Cost')
    plt.grid(True)
    plt.show()
    
# plot_drivetrain_2d(drivetrains)
# print(DT_43x.weight)
# print(DT_43x.useful_thrust)
# print(DT_43x.thrust_to_weight)
# print(DT_43x.useful_thrust+DT_43x.weight)
# print('\n')
# print(DT_43.weight)
# print(DT_43.useful_thrust)
# print(DT_43.useful_thrust+DT_43x.weight)

# print(DT_43.useful_thrust)
# print(DT_43x.useful_thrust)
# print(DT_44.useful_thrust)

print(DT_CURRENTy.useful_thrust)