from dataclasses import dataclass


@dataclass
class BatteryData:
    url: str
    name: str
    capacity: float
    price: float
    weight: float
    voltage: float
    cell_count: int
    watt_hours: float
    specific_energy: float
    wh_per_dollar: float
    under_100_wh: bool
