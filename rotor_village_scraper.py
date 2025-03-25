import os
import json
from parsera import Parsera
from dotenv import load_dotenv
from scraper import get_html_soup, headers, write_battery_data_to_csv
from BatteryData import BatteryData
import requests
from bs4 import BeautifulSoup
import time
import re
from dataclasses import dataclass
from typing import List
import csv
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


urls_rotor_village = ["https://rotorvillage.ca/smc-hcl-rs-22-2v-1600mah-lipo-xt60/", "https://rotorvillage.ca/smc-hcl-rs-22-2v-1400mah-lipo-xt60/", "https://rotorvillage.ca/gnb-7200mah-6s-70c-xt60/", "https://rotorvillage.ca/gnb-1300mah-6s-160c-hv-lipo-xt60/", "https://rotorvillage.ca/gnb-1100mah-6s-160c-hv-lipo-xt60/", "https://rotorvillage.ca/gnb-880mah-6s-hv-160c-xt30/", "https://rotorvillage.ca/gnb-650mah-6s-hv-160c-xt30/", "https://rotorvillage.ca/gnb-1530mah-6s-160c-lipo-xt60/", "https://rotorvillage.ca/gnb-1500mah-6s-160c-lipo-xt60/", "https://rotorvillage.ca/tattu-r-line-v5-0-1480mah-6s-150c-lipo-xt60/", "https://rotorvillage.ca/rvs-6s2p-10-000mah-li-ion-battery/", "https://rotorvillage.ca/rvs-6s1p-4000mah-50a-li-ion-battery/", "https://rotorvillage.ca/rvs-6s2p-8000mah-50a-li-ion-battery/", "https://rotorvillage.ca/gnb-1400mah-6s-160c-lipo-xt60/", "https://rotorvillage.ca/gnb-2600mah-6s-120c-lipo-xt60/", "https://rotorvillage.ca/gnb-1400mah-6s-120c-lipo-xt60/", "https://rotorvillage.ca/bonka-u2-ultra-light-2200mah-6s-22-2v-130c-xt60/", "https://rotorvillage.ca/bonka-u2-ultra-light-1100mah-6s-22-2v-130c-xt60/", "https://rotorvillage.ca/bonka-u2-1380mah-6s-180c-xt60/", "https://rotorvillage.ca/auline-22-2v-6s2p-8000mah-li-ion-battery-xt60/", "https://rotorvillage.ca/tattu-r-line-v5-0-1800mah-6s-150c-xt60/", "https://rotorvillage.ca/tattu-r-line-v5-0-1550mah-6s-150c-xt60/", "https://rotorvillage.ca/tattu-r-line-v5-0-1050mah-6s-150c-xt60/", "https://rotorvillage.ca/tattu-r-line-v5-0-850mah-6s-150c-xt30/", "https://rotorvillage.ca/auline-21700-4000mah-6s-22-2v-a45-li-ion-battery-xt60/",
                      "https://rotorvillage.ca/gnb-7000mah-6s-70c-xt60/", "https://rotorvillage.ca/tattu-r-line-2200mah-6s-95c-lipo-xt60/", "https://rotorvillage.ca/gnb-1300mah-6s-120c-lipo-xt60/", "https://rotorvillage.ca/gnb-650mah-6s-120c-lipo-xt30/", "https://rotorvillage.ca/gnb-850mah-6s-60c-lipo-xt30/", "https://rotorvillage.ca/gnb-450mah-6s-80c-lipo-xt30/", "https://rotorvillage.ca/gnb-1100mah-6s-120c-lipo-xt60/", "https://rotorvillage.ca/gnb-3000mah-6s-100c-xt60/", "https://rotorvillage.ca/gnb-2300mah-6s-50c-lipo-xt60-1/", "https://rotorvillage.ca/gnb-1100mah-6s-120c-hv-lipo-xt60/", "https://rotorvillage.ca/gnb-4500mah-6s-110c-xt60/", "https://rotorvillage.ca/gnb-1850mah-6s-120c-xt60/", "https://rotorvillage.ca/gnb-930mah-6s-120c-lipo-xt60/", "https://rotorvillage.ca/gnb-1100mah-6s-hv-60c-lipo-xt60/", "https://rotorvillage.ca/tattu-r-line-v5-0-1400mah-6s-150c-lipo-xt60/", "https://rotorvillage.ca/tattu-r-line-v5-0-1200mah-6s-150c-lipo-xt60/", "https://rotorvillage.ca/tattu-r-line-550mah-6s-95c-lipo-xt30/", "https://rotorvillage.ca/gnb-1300mah-6s-120c-xt60/", "https://rotorvillage.ca/gnb-long-range-1700mah-6s-60c-lipo-xt60-hv-4-35/", "https://rotorvillage.ca/gnb-1500mah-6s-120c-hv-lipo-xt60/", "https://rotorvillage.ca/gnb-530mah-hv-6s-90c-lipo-xt30-hv4-35/", "https://rotorvillage.ca/gnb-380mah-6s-hv-90c-lipo-xt30-4-35v/", "https://rotorvillage.ca/tattu-r-line-4-0-1300mah-6s-130c-lipo-xt60/", "https://rotorvillage.ca/gnb-1350mah-6s-100c-lipo-xt60/", "https://rotorvillage.ca/tattu-r-line-650mah-6s-95c-lipo-xt30/", "https://rotorvillage.ca/gnb-2200mah-6s-120c-lipo-xt60/"]

# url: str
# name: str


def get_name(soup):
    name = soup.find("h1", class_="productView-title").text
    return name

# capacity: float


def get_capacity(name):
    capacity = name.replace(" ", "")
    match = re.search(r"(\d+)(MAH)", capacity, re.IGNORECASE)
    capacity = match.group(1)
    capacity = float(capacity)
    return capacity

# price: float


def get_price(soup):
    price = soup.find("span", class_="price price--withoutTax").text
    price = price.replace("$", "")
    price = float(price)
    return price

# weight: float


def get_weight(soup):
    tab_description = soup.find("div", class_="tabs-contents")
    if tab_description:
        for line in tab_description.stripped_strings:
            if "weight" in line.lower():
                ore = line
    matches = re.finditer(r'(\d+)(g|gr)', ore, re.IGNORECASE)

    # Extract the match with the largest number
    largest_match = max((m for m in matches), key=lambda m: int(m.group(1)), default=None)

    weight = largest_match.group().replace(' ', '').strip()
    weight = weight.lower().replace("g", '')
    weight = float(weight)
    return weight

    # voltage: float


def get_voltage(name):
    match = re.search(r"(\d+\.\d+)v", name, re.IGNORECASE)
    if match:
        voltage = match.group(1).upper()
        voltage = voltage.replace("V", "")
        voltage = float(voltage)
    else:
        match = re.search(r"(\d+)S", name, re.IGNORECASE)
        if match:
            cell_count = match.group(1).upper()
            cell_count = cell_count.replace("S", '')
            cell_count = int(cell_count)
            voltage = cell_count * 3.7
            voltage = float(voltage)
    return voltage

    # cell_count: int


def get_cell_count(voltage):
    cell_count = voltage / 3.7
    cell_count = round(cell_count)
    return cell_count

    # watt_hours: float


def get_watt_hours(capacity, voltage):
    watt_hours = capacity * voltage / 1000
    return watt_hours

    # specific_energy: float


def get_specific_energy(watt_hours, weight):
    specific_energy = watt_hours / weight
    return specific_energy

    # wh_per_dollar: float


def get_wh_per_dollar(watt_hours, price):
    wh_per_dollar = watt_hours / price
    return wh_per_dollar

    # under_100_wh: bool


def test():
    soup = get_html_soup(urls_rotor_village[0])
    name = get_name(soup)
    print(name)
    capacity = get_capacity(name)
    print(capacity)
    price = get_price(soup)
    print(price)
    weight = get_weight(soup)
    print(weight)
    voltage = get_voltage(name)
    print(voltage)
    cell_count = get_cell_count(voltage)
    print(cell_count)
    watt_hours = get_watt_hours(capacity, voltage)
    print(watt_hours)
    specific_energy = get_specific_energy(watt_hours, weight)
    print(specific_energy)
    wh_per_dollar = get_wh_per_dollar(watt_hours, price)
    print(wh_per_dollar)


def create_battery(url: str):
    soup = get_html_soup(url)

    name = get_name(soup)
    capacity = get_capacity(name)
    price = get_price(soup)
    weight = get_weight(soup)
    voltage = get_voltage(name)
    cell_count = get_cell_count(voltage)
    watt_hours = get_watt_hours(capacity, voltage)
    specific_energy = get_specific_energy(watt_hours, weight)
    wh_per_dollar = get_wh_per_dollar(watt_hours, price)
    under_100_wh = watt_hours < 100

    created_battery = BatteryData(
        url=url,
        name=name,
        capacity=capacity,
        price=price,
        weight=weight,
        voltage=voltage,
        cell_count=cell_count,
        watt_hours=watt_hours,
        specific_energy=specific_energy,
        wh_per_dollar=wh_per_dollar,
        under_100_wh=under_100_wh
    )

    return created_battery


if __name__ == "__main__":
    total_batteries = len(urls_rotor_village)

    for index, url in enumerate(urls_rotor_village):
        try:
            print(f"Processing battery {index} of {total_batteries} total batteries")
            created_battery = create_battery(url)
            print(f"Processed {url}")
            write_battery_data_to_csv(created_battery, "data/rotor_village_battery_data.csv")
            print(f"Written {url} to CSV")
        except Exception as error:
            print(f"Error processing {url}: {error}")
            logger.exception(error)
