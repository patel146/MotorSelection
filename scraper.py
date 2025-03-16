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

BASE_URL = "https://hobbyking.com"
START_URL = "https://hobbyking.com/en_us/batteries-chargers.html#q=&idx=hbk_live_magento_en_us_products&dFR%5Bwarehouses%5D%5B0%5D=USA&dFR%5Bwarehouses%5D%5B1%5D=Global&dFR%5Bwarehouses_stock_data%5D%5B0%5D=USA%7C1&dFR%5Bwarehouses_stock_data%5D%5B1%5D=USA%7C2&dFR%5Bwarehouses_stock_data%5D%5B2%5D=USA%7C3&dFR%5Bwarehouses_stock_data%5D%5B3%5D=Global%7C1&dFR%5Bwarehouses_stock_data%5D%5B4%5D=Global%7C2&dFR%5Bwarehouses_stock_data%5D%5B5%5D=Global%7C3&hFR%5Bcategories.level0%5D%5B0%5D=Batteries%20%2F%20Chargers%20%2F%2F%2F%20Batteries&is_v=1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

urls = ["https://hobbyking.com/en_us/turnigy-2200mah-3s-25c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-2200mah-6s-60c-lipo-pack-w-xt60-connector.html", "https://hobbyking.com/en_us/turnigy-battery-heavy-duty-5000mah-6s-60c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-nano-tech-300mah-2s-70c-hr-technology.html", "https://hobbyking.com/en_us/turnigy-3500mah-2s-60c-lipo-pack-w-xt60-connector.html", "https://hobbyking.com/en_us/turnigy-2200mah-3s-40c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-1000mah-3s-20c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-rapid-6000mah-6s-22-2v-100c-lipo-battery-pack-w-ec5-connector.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-4000mah-8s-60c-lipo-battery-pack-xt90-ec5.html", "https://hobbyking.com/en_us/turnigy-2200mah-6s-40c-lipo-pack-w-xt60-connector.html", "https://hobbyking.com/en_us/turnigy-2200mah-6s-30c-lipo-pack-w-xt60-connector.html", "https://hobbyking.com/en_us/turnigy-nano-tech-450mah-4s-35c-lipo-pack-w-xt30-connector.html", "https://hobbyking.com/en_us/turnigy-nano-tech-300mah-2s-35c-lipo-pack-w-jst-ph-connector.html", "https://hobbyking.com/en_us/turnigy-nano-tech-300mah-2s-35c-lipo-pack-w-jst-connector.html", "https://hobbyking.com/en_us/turnigy-rapid-6000mah-6s-22-2v-100c-lipo-battery-pack-w-xt90-connector.html", "https://hobbyking.com/en_us/turnigy-rapid-6000mah-4s-14-8v-100c-lipo-battery-pack-w-ec5-connector.html", "https://hobbyking.com/en_us/turnigy-rapid-6000mah-4s-14-8v-100c-lipo-battery-pack-w-xt90-connector.html", "https://hobbyking.com/en_us/turnigy-rapid-6000mah-3s-11-1v-100c-lipo-battery-pack-w-xt90-connector.html", "https://hobbyking.com/en_us/turnigy-rapid-6000mah-2s-7-4v-100c-lipo-battery-pack-w-xt90-connector.html", "https://hobbyking.com/en_us/turnigy-rapid-5000mah-6s-22-2v-100c-lipo-battery-pack-w-xt90-connector.html", "https://hobbyking.com/en_us/turnigy-rapid-5000mah-3s-11-1v-100c-lipo-battery-pack-w-xt90-connector.html", "https://hobbyking.com/en_us/turnigy-rapid-5000mah-2s-7-4v-100c-lipo-battery-pack-w-ec5-connector.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-5200mah-6s-60c-lipo-battery-pack-w-ec5.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-5200mah-4s-60c-lipo-battery-pack-w-ec5.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-5200mah-4s-60c-lipo-battery-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-5200mah-3s-60c-lipo-battery-pack-w-ec5.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-5200mah-3s-60c-lipo-battery-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-6200mah-6s-60c-lipo-battery-pack-w-ec5.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-6200mah-6s-60c-lipo-battery-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-6200mah-4s-60c-lipo-battery-pack-w-ec5.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-6200mah-4s-60c-lipo-battery-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-6200mah-3s-60c-lipo-battery-pack-w-ec5.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-6200mah-3s-60c-lipo-battery-pack-w-tr.html", "https://hobbyking.com/en_us/turnigy-rapid-8000mah-4s2p-140c-hardcase-lipo-battery-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-rapid-8000mah-3s2p-140c-hardcase-lipo-battery-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-rapid-6500mah-4s2p-140c-hardcase-lipo-battery-pack-w-xt90-connector.html", "https://hobbyking.com/en_us/turnigy-5000mah-3s-20c-lipo-pack-w-xt-90.html", "https://hobbyking.com/en_us/turnigy-nano-tech-plus-5000mah-4s-70c-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-nano-tech-plus-5000mah-3s-70c-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-nano-tech-3300mah-4s-25c-lipo-pack-w-xt60.html", "https://hobbyking.com/en_us/turnigy-nano-tech-3300mah-2s-35c-lipo-pack-w-xt60.html", "https://hobbyking.com/en_us/turnigy-rapid-6500mah-2s2p-140c-hardcase-lipo-battery-pack-roar-approved.html", "https://hobbyking.com/en_us/turnigy-rapid-8000mah-2s2p-140c-hardcase-lipo-battery-pack-roar-approved.html", "https://hobbyking.com/en_us/turnigy-rapid-5500mah-4s2p-140c-hardcase-lipo-battery-pack-w-xt90-connector-roar-approved.html", "https://hobbyking.com/en_us/turnigy-rapid-5500mah-3s2p-140c-hardcase-lipo-battery-pack-w-xt60-connector-roar-approved.html", "https://hobbyking.com/en_us/turnigy-1300mah-4s-60c-lipo-pack-w-xt60.html", "https://hobbyking.com/en_us/turnigy-850mah-3s-60c-lipo-pack-w-xt30.html", "https://hobbyking.com/en_us/turnigy-450mah-4s-60c-lipo-pack-w-xt30.html", "https://hobbyking.com/en_us/turnigy-450mah-3s-60c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-plus-450mah-4s-70c-w-xt30.html", "https://hobbyking.com/en_us/graphene-panther-1300mah-6s-75c-lipo-pack-w-xt60.html", "https://hobbyking.com/en_us/turnigy-nano-tech-450mah-3s-45c-lipo-pack-w-xt30.html", "https://hobbyking.com/en_us/turnigy-nano-tech-plus-650mah-1s-70c-lipo-pack-w-jst-ph.html", "https://hobbyking.com/en_us/turnigy-nano-tech-plus-550mah-1s-70c-lipo-pack-w-jst-ph.html", "https://hobbyking.com/en_us/turnigy-350mah-2s1p-45c-lipo-pack-w-xt30.html", "https://hobbyking.com/en_us/turnigy-nano-tech-plus-6000mah-6s-70c-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-nano-tech-plus-3000mah-3s-70c-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-nano-tech-plus-1300mah-3s-70c-lipo-pack-w-xt60.html", "https://hobbyking.com/en_us/turnigy-nano-tech-600mah-1s-25c-lipo-pack-w-walkera.html", "https://hobbyking.com/en_us/turnigy-graphene-panther-1200mah-6s-75c-battery-pack-w-xt60.html", "https://hobbyking.com/en_us/turnigy-1000mah-6s-65c-lipo-pack-w-xt60.html", "https://hobbyking.com/en_us/turnigy-650mah-3s-65c-lipo-pack-w-xt30.html", "https://hobbyking.com/en_us/turnigy-graphene-panther-450mah-4s-75c.html", "https://hobbyking.com/en_us/turnigy-graphene-panther-450mah-3s-75c.html", "https://hobbyking.com/en_us/turnigy-high-capacity-14000mah-6s-12c-multi-rotor-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-high-capacity-16000mah-4s-12c-multi-rotor-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-high-capacity-16000mah-6s-12c-multi-rotor-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-high-capacity-12000mah-4s-12c-multi-rotor-lipo-pack-xt90.html", "https://hobbyking.com/en_us/turnigy-graphene-3000mah-4s-75c-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-graphene-3000mah-3s-75c-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-graphene-6000mah-6s-75c-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-graphene-5000mah-4s-75c-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-graphene-500mah-4s-75c-lipo-pack-w-xt30.html", "https://hobbyking.com/en_us/turnigy-graphene-6000mah-4s-75c-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-graphene-6000mah-3s-75c-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-graphene-4000mah-3s-75c-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-graphene-1000mah-6s-75c-lipo-pack-w-xt60.html", "https://hobbyking.com/en_us/turnigy-graphene-850mah-4s-75c-lipo-pack-w-xt60u.html", "https://hobbyking.com/en_us/turnigy-graphene-950mah-1s-75c-lipo-pack-w-jst-45syp-452p.html", "https://hobbyking.com/en_us/nano-tech-70c-1000mah-6s1p-22-2v.html", "https://hobbyking.com/en_us/turnigy-high-capacity-battery-8000mah-4s-12c-drone-lipo-pack-xt90.html", "https://hobbyking.com/en_us/turnigy-high-capacity-battery-8000mah-6s-12c-drone-lipo-pack-xt90.html", "https://hobbyking.com/en_us/turnigy-high-capacity-10000mah-4s-12c-multi-rotor-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-high-capacity-10000mah-6s-12c-multi-rotor-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-high-capacity-battery-12000mah-6s-12c-drone-lipo-pack-xt90.html", "https://hobbyking.com/en_us/turnigy-high-capacity-battery-20000mah-6s-12c-drone-lipo-pack-xt90.html", "https://hobbyking.com/en_us/turnigy-1400mah-4s-40c-lipo-pack-w-xt60.html", "https://hobbyking.com/en_us/turnigy-1400mah-3s-65c-lipo-pack-w-xt60.html", "https://hobbyking.com/en_us/turnigy-1400mah-4s-65c-lipo-pack-w-xt60.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-4000mah-6s-60c-lipoly-battery-pack-xt90.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2650mah-4s-30c-lipo-pack-wxt60.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2650mah-3s-30c-lipo-pack-wxt60.html", "https://hobbyking.com/en_us/turnigy-nano-tech-4000mah-4s-30c-lipo-pack-wxt60.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1400mah-2s-25c-lipo-pack-wxt60.html", "https://hobbyking.com/en_us/turnigy-nano-tech-850mah-3s-30c-lipo-pack-jst.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1300mah-4s-70c-lipo-pack-xt60-hr-tech.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1000mah-4s-70c-lipo-pack-xt60-hr-tech.html", "https://hobbyking.com/en_us/turnigy-nano-tech-750mah-1s-70c-lipo-pack-2pin-molex-hr-tech.html", "https://hobbyking.com/en_us/graphene-5000mah-6s-75c.html", "https://hobbyking.com/en_us/graphene-5000mah-3s-75c.html", "https://hobbyking.com/en_us/graphene-600mah-1s-75c.html", "https://hobbyking.com/en_us/graphene-950mah-2s-75c.html", "https://hobbyking.com/en_us/graphene-1600mah-4s-75c-normal-pack.html", "https://hobbyking.com/en_us/graphene-1300mah-4s-75c.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-5000mah-7s-60c-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-2650mah-3s-20c-lipo-pack-1.html", "https://hobbyking.com/en_us/turnigy-2200mah-2s-25c-lipo-pack-w-xt60.html", "https://hobbyking.com/en_us/1600-2s-30c-mini-car-battery.html", "https://hobbyking.com/en_us/turnigy-5000mah-6s-40c-lipo-pack-xt90.html", "https://hobbyking.com/en_us/turnigy-graphene-professional-12000mah-6s-15c-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-graphene-professional-10000mah-4s-15c-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-graphene-professional-8000mah-6s-15c-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-5000mah-5s-30c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-battery-5000mah-5s-25c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-battery-5000mah-5s-20c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-battery-5000mah-4s-25c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-battery-5000mah-3s-40c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-5000mah-3s-30c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-battery-5000mah-3s-25c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-5000mah-3s-20c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-5000mah-2s-30c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-5000mah-2s-20c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-battery-4500mah-6s-30c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-4000mah-5s-30c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-4000mah-4s-30c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-4000mah-3s-30c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-4000mah-2s-30c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-3600mah-4s-30c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-3600mah-3s-30c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-3300mah-6s-30c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-3300mah-5s-30c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-3300mah-4s-30c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-3000mah-6s-40c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-3000mah-4s-40c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-3000mah-3s-20c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-3000mah-2s-40c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-2650mah-3s-30c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-nano-tech-6000mah-4s-25-50c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-nano-tech-5000mah-6s-35-70c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-battery-nano-tech-5000mah-3s-65-130c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-nano-tech-4500mah-3s-35-70c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-nano-tech-2700mah-3s-65-130c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-heavy-duty-4000mah-4s-60c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-battery-heavy-duty-4000mah-3s-60c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-3300mah-3s-60c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-5000mah-4s-60c-lipo-pack-w-xt-90.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-5000mah-3s-60c-lipo-pack-w-xt-90.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-2200mah-3s-60c-lipo-pack-w-xt60.html", "https://hobbyking.com/en_us/turnigy-3000mah-5s-20c-lipo-pack-1.html", "https://hobbyking.com/en_us/turnigy-2000mah-1s-1c-lipoly-w-2-pin-jst-ph-connector.html", "https://hobbyking.com/en_us/turnigy-nano-tech-450mah-3s-65c-lipo-e-flite-compatible-blade-180cfx-eflb4503sj30.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1200mah-2s-15-30c-lipo-airsoft-pack-t-connector.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2000mah-2s-15-30c-lipo-airsoft-pack-t-connector.html", "https://hobbyking.com/en_us/turnigy-1500mah-3s-30c-lipo-e-flite-compatible-eflb15003s.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1200mah-3s-25-50c-lipo-airsoft-pack-1.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1200mah-2s-25-50c-lipo-airsoft-pack-1.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1200mah-3s-25-50c-lipo-airsoft-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1200mah-2s-25-50c-lipo-airsoft-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1500mah-2s-20-40c-lipo-airsoft-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1000mah-3s-20-40c-lipo-airsoft-pack-1.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1000mah-3s-20-40c-lipo-airsoft-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1000mah-2s-20-40c-lipo-airsoft-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1500mah-3s-35-70c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1500mah-2s-35-70c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1500mah-3s-25-50c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2100mah-2s1p-20-40c-lifepo4-receiver-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1450mah-2s1p-20-40c-lifepo4-receiver-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-3000mah-2s2p-20-40c-lipo-receiver-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2000mah-2s1p-20-40c-lipo-receiver-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2000mah-2s1p-20-40c-lifepo4-transmitter-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2100mah-2s1p-20c-lifepo4-transmitter-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2500mah-3s1p-5-10c-transmitter-lipo-pack-old-style-futaba-specs.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2500mah-3s1p-5-10c-transmitter-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-950mah-1s-25-50c-lipo-pack-walkera-v120-x100.html", "https://hobbyking.com/en_us/turnigy-nano-tech-750mah-1s-35-70c-lipo-pack-fits-nine-eagles-solo-pro-180.html", "https://hobbyking.com/en_us/turnigy-700mah-3s-60c-xt30.html", "https://hobbyking.com/en_us/turnigy-graphene-3000mah-3s-15c-w-xt60.html", "https://hobbyking.com/en_us/turnigy-2500mah-3s-30c-lipoly-pack-w-ec3-e-flite-compatible-eflb25003s30.html", "https://hobbyking.com/en_us/turnigy-1500mah-3s-20c-lipoly-pack-w-ec3-e-flite-compatible.html", "https://hobbyking.com/en_us/turnigy-1250mah-2s-20c-lipoly-pack-w-ec3-e-flite-compatible-eflb12502s.html", "https://hobbyking.com/en_us/turnigy-1250mah-3s-30c-lipo-pack-long.html", "https://hobbyking.com/en_us/turnigy-800mah-3s-20c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2000mah-2s-15-25c-lipo-airsoft-pack-1.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1800mah-2s-25-50c-lipo-airsoft-pack-1.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1800mah-2s-20-40c-lipo-airsoft-pack-1.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1800mah-2s-20-40c-lipo-airsoft-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1400mah-2s-15-25c-lipo-airsoft-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1300mah-2s-25-50c-lipo-airsoft-pack-1.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1300mah-2s-25-50c-lipo-airsoft-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1200mah-2s-15-25c-lipo-airsoft-pack-1.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1200mah-3s-15-25c-lipo-airsoft-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1200mah-2s-15-25c-lipo-airsoft-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-850mah-4s-25-50c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-850mah-3s-25-40c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-370mah-3s-25-40c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-350mah-1s-65-130c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2250mah-2s-65-130c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2200mah-3s-45-90c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2200mah-3s-35-70c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2200mah-2s-25-50c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1800mah-4s-35-70c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1800mah-3s-65-130c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1600mah-4s-25-50c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1600mah-3s-25-50c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1000mah-4s-45-90c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1000mah-3s-25-50c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1000mah-2s-25-50c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-800mah-3s-30c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-800mah-3s-20c-lipo-pack-e-flight-compatible-eflb0995.html",
        "https://hobbyking.com/en_us/turnigy-800mah-2s-30c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-800mah-2s-20c-lipo-pack-parkzone-compatible-pkz1032.html", "https://hobbyking.com/en_us/turnigy-5000mah-1s-20c-lipoly-single-cell.html", "https://hobbyking.com/en_us/turnigy-500mah-2s-20c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-3600mah-2s-12c-lipo-receiver-pack.html", "https://hobbyking.com/en_us/turnigy-2200mah-3s-30c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-2200mah-2s-30c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-1800mah-3s-40c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-1800mah-3s-20c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-1800mah-2s-20c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-1600mah-3s-30c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-1600mah-3s-20c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-1600mah-2s-30c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-1600mah-2s-20c-losi-mini-sct-pack-part-losb1212.html", "https://hobbyking.com/en_us/turnigy-1500mah-3s-25c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-1500mah-3s-20c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-1300mah-6s-35c-lipo-pack-450-helicopter-hk-trex-rave-e4-etc.html", "https://hobbyking.com/en_us/turnigy-1300mah-2s-20c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-1000mah-2s-30c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-1000mah-2s-20c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-rapid-6000mah-3s-11-1v-100c-lipo-battery-pack-w-xt60-connector.html", "https://hobbyking.com/en_us/turnigy-rapid-5000mah-2s-7-4v-100c-lipo-battery-pack-w-t-connector.html", "https://hobbyking.com/en_us/turnigy-rapid-5000mah-3s-11-1v-100c-lipo-battery-pack-w-xt60-connector.html", "https://hobbyking.com/en_us/rc-era-c189-md500-flybarless-rc-helicopter-replacement-7-4v-1200mah-smart-battery-pack.html", "https://hobbyking.com/en_us/rc-era-c186-mbb-bo-105-flybarless-rc-helicopter-replacement-7-4v-350mah-battery-pack.html", "https://hobbyking.com/en_us/turnigy-rapid-6000mah-3s-11-1v-100c-lipo-battery-pack-w-ec5-connector.html", "https://hobbyking.com/en_us/turnigy-rapid-6000mah-2s-7-4v-100c-lipo-battery-pack-w-ec5-connector.html", "https://hobbyking.com/en_us/turnigy-rapid-5000mah-6s-22-2v-100c-lipo-battery-pack-w-ec5-connector.html", "https://hobbyking.com/en_us/turnigy-rapid-5000mah-4s-14-8v-100c-lipo-battery-pack-w-ec5-connector.html", "https://hobbyking.com/en_us/turnigy-rapid-5000mah-4s-14-8v-100c-lipo-battery-pack-w-xt90-connector.html", "https://hobbyking.com/en_us/turnigy-rapid-5000mah-3s-11-1v-100c-lipo-battery-pack-w-ec5-connector.html", "https://hobbyking.com/en_us/turnigy-rapid-5000mah-2s-7-4v-100c-lipo-battery-pack-w-xt90-connector.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-6200mah-4s-60c-lipo-battery-pack-w-tr.html", "https://hobbyking.com/en_us/turnigy-nano-tech-plus-3000mah-3s-70c-lipo-battery-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-nano-tech-300mah-1s-20-40c-lipo-battery-losi-mini-compatible.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1300mah-2s1p-20-40c-lipo-receiver-battery-pack-w-jst-jr-type-connectors.html", "https://hobbyking.com/en_us/turnigy-nano-tech-3300mah-6s-25c-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-nano-tech-plus-850mah-4s-70c-lipo-pack-w-xt60.html", "https://hobbyking.com/en_us/turnigy-rapid-5500mah-2s2p-140c-hardcase-lipo-battery-pack-roar-approved.html", "https://hobbyking.com/en_us/turnigy-rapid-3000mah-2s1p-140c-hardcase-shorty-lipo-battery-pack-roar-approved.html", "https://hobbyking.com/en_us/turnigy-850mah-4s-60c-lipo-pack-w-xt30.html", "https://hobbyking.com/en_us/turnigy-nano-tech-350mah-2s-65c-lipo-pack-w-xt30.html", "https://hobbyking.com/en_us/turnigy-nano-tech-plus-1500mah-4s-70c-lipo-pack-w-xt60.html", "https://hobbyking.com/en_us/turnigy-nano-tech-plus-2200mah-4s-70c-lipo-pack-w-xt60.html", "https://hobbyking.com/en_us/turnigy-nano-tech-300mah-1s-45c-lipo-pack-w-jst-ph.html", "https://hobbyking.com/en_us/turnigy-nano-tech-300mah-2s-45c-lipo-pack-w-xt30.html", "https://hobbyking.com/en_us/turnigy-450mah-2s1p-45c-lipo-pack-w-xt30.html", "https://hobbyking.com/en_us/turnigy-nano-tech-500mah-1s-25-50c-lipo-pack-losi-mini-compatible-1.html", "https://hobbyking.com/en_us/turnigy-graphene-4000mah-4s-75c-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-2700mah-3s-20c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-high-capacity-4000mah-3s2p-12c-multi-rotor-lipo-pack-w-xt60.html", "https://hobbyking.com/en_us/turnigy-high-capacity-battery-6600mah-6s-12c-drone-lipo-pack-xt90.html", "https://hobbyking.com/en_us/turnigy-high-capacity-battery-20000mah-4s-12c-drone-lipo-pack-xt90.html", "https://hobbyking.com/en_us/turnigy-1400mah-3s-40c-lipo-pack-w-xt60.html", "https://hobbyking.com/en_us/turnigy-nano-tech-3000mah-3s-30c-lipo-pack-wxt60.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2200mah-3s-25c-lipo-pack-wxt60.html", "https://hobbyking.com/en_us/turnigy-nano-tech-5000mah-6s-70c-lipo-pack-w-xt-90-hr-tech.html", "https://hobbyking.com/en_us/turnigy-nano-tech-850mah-3s-70c-lipo-pack-xt60-hr-tech.html", "https://hobbyking.com/en_us/graphene-3000mah-6s-75c.html", "https://hobbyking.com/en_us/graphene-4000mah-6s-75c.html", "https://hobbyking.com/en_us/graphene-1600mah-4s-75c-square-pack.html", "https://hobbyking.com/en_us/turnigy-9xr-safety-protected-2200mah-3s-1-5c-transmitter-pack.html", "https://hobbyking.com/en_us/znter-micro-usb-charging-cable-for-usb-rechargeable-battery-2.html", "https://hobbyking.com/en_us/turnigy-battery-5000mah-2s-40c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-battery-3600mah-6s-30c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-3300mah-3s-30c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-3000mah-4s-20c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-1500mah-2s-25c-lipoly-battery-xt-60.html", "https://hobbyking.com/en_us/turnigy-nano-tech-6000mah-3s-25-50c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-nano-tech-5000mah-2s-45-90c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-nano-tech-5000mah-2s-35-70c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-battery-nano-tech-4500mah-6s-25-50c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-nano-tech-4500mah-5s-35-70c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-nano-tech-4000mah-6s-25-50c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2650mah-6s-45-90c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-nano-tech-2650mah-4s-35-70c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-5000mah-6s-20c-lipo-pack-w-xt-90.html", "https://hobbyking.com/en_us/turnigy-2200mah-1s-20c-lipoly-single-cell-1.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1000mah-3s-20-40c-lipo-airsoft-pack-t-connector.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1300mah-2s-25-50c-lipo-airsoft-pack-t-connector.html", "https://hobbyking.com/en_us/turnigy-nano-tech-300mah-2s-35-70c-lipo-pack-e-flite-eflb2002s25-micro-series-compatible.html", "https://hobbyking.com/en_us/turnigy-nano-tech-300mah-2s-45-90c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-300mah-1s-45-90c-lipo-pack-fits-nine-eagles-solo-pro-100.html", "https://hobbyking.com/en_us/turnigy-nano-tech-450mah-2s-65c-lipo-e-flite-compatible-blade-130x-eflb3002s35.html", "https://hobbyking.com/en_us/turnigy-nano-tech-300mah-2s-35-70c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-950mah-2s-25-50c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-1800mah-3s-20c-lipoly-pack-w-ec3-e-flite-compatible-eflb32003s.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2000mah-3s-15-25c-lipo-airsoft-pack-1.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2000mah-3s-15-25c-lipo-airsoft-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2000mah-2s-15-25c-lipo-airsoft-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1800mah-3s-20-40c-lipo-airsoft-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1800mah-2s-25-50c-lipo-airsoft-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1400mah-3s-15-25c-lipo-airsoft-pack-1.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1400mah-2s-15-25c-lipo-airsoft-pack-1.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1400mah-3s-15-25c-lipo-airsoft-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1300mah-3s-25-50c-lipo-airsoft-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2200mah-4s-45-90c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2200mah-4s-25-50c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1800mah-2s-25-50c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1300mah-3s-25-50c-lipo-pack.html", "https://hobbyking.com/en_us/zippy-compact-850mah-3s-35c-lipo-pack.html", "https://hobbyking.com/en_us/zippy-850mah-20c-single-cell.html", "https://hobbyking.com/en_us/turnigy-500mah-3s-20c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-2650mah-4s-20c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-2200mah-4s-40c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-1800mah-2s-30c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-1600mah-4s-20c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-1600mah-2s-20c-lipo-pack-losi-mini-compatible.html", "https://hobbyking.com/en_us/turnigy-1300mah-3s-30c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-1000mah-1s-20c-lipoly-single-cell.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2200mah-2s-30c-lifepo4-transmitter-receiver-pack-w-futaba-ph1-0-connector.html", "https://hobbyking.com/en_us/turnigy-nano-tech-850mah-2s-12c-lifepo4-transmitter-receiver-pack-w-jr-s-type-connector.html", "https://hobbyking.com/en_us/turnigy-graphene-panther-900mah-3s-75c-battery-pack-w-xt60-connector.html", "https://hobbyking.com/en_us/turnigy-nano-tech-300mah-3s-50c-lipo-pack-w-jst-connector.html", "https://hobbyking.com/en_us/turnigy-nano-tech-300mah-3s-35c-lipo-pack-w-jst-connector.html", "https://hobbyking.com/en_us/turnigy-nano-tech-350mah-2s-25-40c-lipo-battery-for-1-18-1-24-rc-crawlers.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-5200mah-6s-60c-lipo-battery-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-6200mah-3s-60c-lipo-battery-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-nano-tech-3300mah-6s-45c-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-nano-tech-3300mah-6s-35c-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-nano-tech-3300mah-4s-35c-lipo-pack-w-xt60.html", "https://hobbyking.com/en_us/turnigy-nano-tech-plus-1400mah-4s-70c-lipo-pack-w-xt60.html", "https://hobbyking.com/en_us/turnigy-nano-tech-500mah-2s-25c-lipo-pack-w-xt30.html", "https://hobbyking.com/en_us/turnigy-nano-tech-plus-450mah-3s-70c-w-xt30.html", "https://hobbyking.com/en_us/turnigy-200mah-1s-20c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-plus-5100mah-4s-70c-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/zippy-compact-4000mah-5s1p-40c.html", "https://hobbyking.com/en_us/turnigy-graphene-panther-650mah-3s-75c-battery-pack-w-xt30.html", "https://hobbyking.com/en_us/turnigy-650mah-4s-65c-lipo-pack-w-xt30.html", "https://hobbyking.com/en_us/turnigy-graphene-1300mah-3s-75c-lipo-pack-w-xt60.html", "https://hobbyking.com/en_us/turnigy-high-capacity-battery-6600mah-64s-12c-drone-lipo-pack-xt60.html", "https://hobbyking.com/en_us/turnigy-nano-tech-4000mah-6s-35-70c-lipo-pack-w-xt-90.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1800mah-3s-30c-lipo-pack-wxt60.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1300mah-2s-25c-lipo-pack-wxt60.html", "https://hobbyking.com/en_us/turnigy-nano-tech-4000mah-6s-70c-lipo-pack-w-xt-90-hr-tech.html", "https://hobbyking.com/en_us/turnigy-nano-tech-3000mah-6s-70c-lipo-pack-w-xt90-hr-tech.html", "https://hobbyking.com/en_us/graphene-650mah-4s-75c.html", "https://hobbyking.com/en_us/graphene-1000mah-3s-75c.html", "https://hobbyking.com/en_us/graphene-1000mah-4s-75c.html", "https://hobbyking.com/en_us/turnigy-2650mah-3s-1c-lipoly-tx-pack-futaba-jr-1.html", "https://hobbyking.com/en_us/turnigy-5000mah-6s-25c-battery.html", "https://hobbyking.com/en_us/turnigy-nano-tech-5000mah-6s-45-90c-lipo-pack-xt90.html", "https://hobbyking.com/en_us/turnigy-battery-3000mah-6s-30c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-nano-tech-6000mah-2s-25-50c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-nano-tech-5000mah-5s-25-50c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-nano-tech-5000mah-4s-25-50c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-battery-nano-tech-5000mah-3s-25-50c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-battery-nano-tech-4500mah-4s-35-70c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-nano-tech-4400mah-4s-65-130c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-heavy-duty-3300mah-6s-60c-lipo-pack-xt-90.html", "https://hobbyking.com/en_us/turnigy-battery-nano-tech-2700mah-6s-65-130c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-nano-tech-2650mah-6s-35-70c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-2200mah-2s-20c-lipo-pack-w-xt60.html", "https://hobbyking.com/en_us/turnigy-2200mah-2s-40c-lipo-pack-1.html", "https://hobbyking.com/en_us/turnigy-1200mah-1s-1c-lipoly-w-2-pin-jst-ph-connector.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1200mah-2s-25-50c-lipo-airsoft-pack-t-connector.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1500mah-2s-25-50c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1700mah-2s1p-20-40c-lifepo4-receiver-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1500mah-2s1p-20-40c-lipo-receiver-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-2100mah-3s1p-20-40c-lifepo4-transmitter-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-950mah-3s-25-50c-lipo-pack.html", "https://hobbyking.com/en_us/graphene-5000mah-3s-45c-w-xt90.html", "https://hobbyking.com/en_us/graphene-4000mah-6s-45c-w-xt90.html", "https://hobbyking.com/en_us/turnigy-3200mah-4s-20c-lipoly-pack-w-ec3-e-flite-compatible-eflb32004s.html", "https://hobbyking.com/en_us/turnigy-2800mah-4s-30c-lipoly-pack-w-ec3-e-flite-compatible-eflb28004s30.html", "https://hobbyking.com/en_us/zippy-compact-1800mah-3s-40c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1800mah-3s-25-50c-lipo-airsoft-pack-1.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1800mah-3s-25-50c-lipo-airsoft-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1200mah-3s-15-25c-lipo-airsoft-pack-1.html", "https://hobbyking.com/en_us/turnigy-nano-tech-460mah-3s-25-40c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-460mah-2s-25-40c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-370mah-2s-25-40c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-300mah-1s-35c-lipo-pack-suits-fbl100-and-blade-mcpx.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1800mah-2s-65c-130c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1300mah-3s-45-90c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-800mah-3s-40c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-2200mah-4s-30c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-1800mah-4s-40c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-1800mah-2s-12c-lipo-receiver-pack.html", "https://hobbyking.com/en_us/turnigy-1700mah-2s-20c-lipo-pack-suits-1-16th-monster-beatle-sct-buggy.html", "https://hobbyking.com/en_us/turnigy-1000mah-3s-30c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-1300mah-2s-20c-lipo-pack-suit-1-18th-truck.html", "https://hobbyking.com/en_us/turnigy-nano-tech-plus-3000mah-4s-70c-lipo-battery-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-nano-tech-260mah-2s-35-70c-lipo-battery.html", "https://hobbyking.com/en_us/turnigy-nano-tech-plus-500mah-3s-70c-lipo-pack-w-xt30.html", "https://hobbyking.com/en_us/turnigy-nano-tech-plus-950mah-2s-70c-lipo-pack-w-xt30.html", "https://hobbyking.com/en_us/turnigy-4000mah-6s-30c-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1500mah-life-3s-9-9v-transmitter-pack-taranis-compatible-1.html", "https://hobbyking.com/en_us/turnigy-nano-tech-5000mah-8s-65-130c-lipo-pack-xt90.html", "https://hobbyking.com/en_us/turnigy-nano-tech-550mah-2s1p-7-4v-65c-lipo.html", "https://hobbyking.com/en_us/turnigy-4000mah-3s-40c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-3300mah-2s-30c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-3000mah-5s-30c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-3000mah-3s-40c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-battery-nano-tech-2700mah-4s-65-130c-lipo-pack-xt-60.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-3300mah-4s-60c-lipo-pack-w-xt90.html", "https://hobbyking.com/en_us/turnigy-2200mah-1s-40c-lipoly-single-cell-1.html", "https://hobbyking.com/en_us/turnigy-heavy-duty-2200mah-4s-60c-lipo-pack-w-xt60-connector.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1200mah-3s-15-25c-lipo-airsoft-pack-t-connector.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1550mah-6s-65-130c-lipo-pack-450l-heli.html", "https://hobbyking.com/en_us/turnigy-nano-tech-750mah-1s-35-70c-lipo-pack-walkera-v120d02s-qr-infra-x-qr-w100s.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1500mah-3s-20-40c-lipo-airsoft-pack.html", "https://hobbyking.com/en_us/turnigy-nano-tech-300mah-1s-45c-lipo-pack-suits-fbl100-and-blade-mcpx.html", "https://hobbyking.com/en_us/turnigy-nano-tech-3000mah-2s1p-20-40c-lifepo4-receiver-pack.html", "https://hobbyking.com/en_us/turnigy-5000mah-4s-40c-lipo-pack-with-xt90.html", "https://hobbyking.com/en_us/turnigy-3200mah-3s-30c-lipoly-pack-w-ec3-e-flite-compatible-eflb32003s30.html", "https://hobbyking.com/en_us/turnigy-nano-tech-1300mah-3s-25-50c-lipo-airsoft-pack-1.html", "https://hobbyking.com/en_us/turnigy-nano-tech-850mah-2s-25-40c-lipo-pack.html", "https://hobbyking.com/en_us/turnigy-1450mah-3s-11-1v-transmitter-lipoly-pack.html"]


def test_connection(URL):
    response = requests.get(URL, headers=headers)
    print("Connection Status Code: ", response.status_code)


def get_raw_html(URL):
    response = requests.get(URL, headers=headers)
    return response.text


def get_html_soup(URL):
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def get_battery_list():
    response = requests.get(START_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    batteries = []
    for item in soup.find_all("a", attrs={"class": "algolia-clearfix link -name"}):
        batteries.append(item)

        time.sleep(0.01)  # Be polite to the server

    return batteries


def get_battery_price(soup):
    price = soup.find(id=re.compile(r"^product-price-\d+")).text
    price = price.replace("Price", "").strip()
    price = price.replace("CA$", "").strip()
    price = float(price)
    return price


def get_battery_name(soup):
    name = soup.find("h2", class_="product-name mobile-display").text
    return name


def get_battery_data(soup):
    bolded = [s.text for s in soup.find_all("strong")]
    return bolded


def get_battery_capacity(battery_data):
    input_str = ' '.join(battery_data)
    pattern = r"(\d+)\s*mAh"
    match = re.search(pattern, input_str)
    if match:
        capacity = match.group(1)  # Extract the capacity value
        capacity = capacity.replace("mAh", "").strip()
        capacity = capacity.replace(" ", "")
        capacity = float(capacity)
    else:
        capacity = 0
    return capacity


def get_battery_weight(battery_data):
    input_str = ' '.join(battery_data)
    pattern = r"(\d+)\s*g"
    match = re.search(pattern, input_str)
    if match:
        weight = match.group(1)  # Extract the weight value
        weight = weight.replace(" ", "")
        weight = weight.replace("g", "")
        weight = float(weight)
    else:
        print("Weight not found.")
    return weight


def extract_config_voltage_cell_count(battery_data):
    input_str = ' '.join(battery_data)
    battery_spec = next((item for item in input_str if re.search(
        r"(\d+)S1P\s*/\s*(\d+(\.\d+)?)v\s*/\s*(\d+)Cell", item)), None)

    if battery_spec:
        battery_spec = battery_spec.replace(" ", "")
        # Extract relevant values using regex
        match = re.match(r'(?P<config>\d+S\d+P)/(?P<voltage>\d+\.\d+)v/(?P<cell_count>\d+)Cell', battery_spec)

        if match:
            config = match.group('config')   # e.g., '6S1P'
            voltage = match.group('voltage')  # e.g., '22.2'
            cell_count = match.group('cell_count')  # e.g., '6'

            return config, voltage, cell_count
        else:
            print("Pattern not found in the extracted battery spec.")
            print(battery_data)
    else:
        print("Battery specification not found in the list.")
        print(battery_data)


def get_battery_voltage(battery_data):
    input_str = ' '.join(battery_data)
    match = re.search(r"(\d+\.\d+)v", input_str, re.IGNORECASE)
    voltage = match.group(1)  # Extract the voltage value
    voltage = voltage.replace("v", "").strip()
    voltage = float(voltage)
    return voltage


def get_battery_cell_count(battery_data, name):
    try:
        input_str = ' '.join(battery_data)
        match = re.search(r"(\d+)\s?Cell", input_str, re.IGNORECASE)
        cell_count = match.group(1)  # Extract the cell count value
        cell_count = cell_count.replace("Cell", "").strip()
        cell_count = int(cell_count)
    except:
        cell_count = get_battery_cell_count_from_name(name)
    return cell_count


def get_battery_cell_count_from_name(name: str):
    match = re.search(r"(\d+)\s?S", name, re.IGNORECASE)
    cell_count = match.group(1).upper()  # Extract the cell count value
    cell_count = cell_count.replace("S", "").strip()
    cell_count = int(cell_count)
    return cell_count


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


Batteries = []


def create_battery(url: str):
    soup = get_html_soup(url)

    name = get_battery_name(soup)
    capacity = get_battery_capacity(get_battery_data(soup))
    price = get_battery_price(soup)
    weight = get_battery_weight(get_battery_data(soup))
    voltage = get_battery_voltage(get_battery_data(soup))
    cell_count = get_battery_cell_count(get_battery_data(soup), name)
    watt_hours = capacity * voltage / 1000
    specific_energy = watt_hours / weight
    wh_per_dollar = watt_hours / price
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

    Batteries.append(created_battery)

    return created_battery


def write_battery_data_to_csv(battery_data: BatteryData, file_name: str):
    # Define the headers for the CSV file (this should match the dataclass fields)
    headers = [
        "url", "name", "capacity", "price", "weight", "voltage", "cell_count",
        "watt_hours", "specific_energy", "wh_per_dollar", "under_100_wh"
    ]

    # Open the CSV file in append mode ('a') so that we don't overwrite existing data
    with open(file_name, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        # Write the header only if the file is empty (i.e., it's the first write)
        if file.tell() == 0:  # Check if the file is empty
            writer.writeheader()

        # Write the data of the BatteryData instance
        writer.writerow({
            "url": battery_data.url,
            "name": battery_data.name,
            "capacity": battery_data.capacity,
            "price": battery_data.price,
            "weight": battery_data.weight,
            "voltage": battery_data.voltage,
            "cell_count": battery_data.cell_count,
            "watt_hours": battery_data.watt_hours,
            "specific_energy": battery_data.specific_energy,
            "wh_per_dollar": battery_data.wh_per_dollar,
            "under_100_wh": battery_data.under_100_wh
        })


def main():
    test_connection(START_URL)
    total_batteries = len(urls)

    # print(get_battery_data(get_html_soup(urls[0])))

    for index, url in enumerate(urls):
        try:
            print(f"Processing battery {index} of {total_batteries} total batteries")
            created_battery = create_battery(url)
            print(f"Processed {url}")
            write_battery_data_to_csv(created_battery, "data/hobby_king_battery_data.csv")
            print(f"Written {url} to CSV")
        except Exception as error:
            print(f"Error processing {url}: {error}")
            logger.exception(error)

    # capacity = get_battery_capacity(get_battery_data(soup))
    # price = get_battery_price(soup)
    # weight = get_battery_weight(get_battery_data(soup))
    # voltage = get_battery_voltage(get_battery_data(soup))
    # cell_count = get_battery_cell_count(get_battery_data(soup))
    # watt_hours = capacity * voltage / 1000
    # specific_energy = watt_hours / weight
    # wh_per_dollar = watt_hours / price
    # under_100_wh = watt_hours < 100

    # print("Capacity: ", capacity)
    # print("Watt Hours: ", watt_hours)
    # print("Price: ", price)
    # print("Weight: ", weight)
    # print("Voltage: ", voltage)
    # print("Cell Count: ", cell_count)
    # print("Specific Energy: ", specific_energy)
    # print("Wh per Dollar: ", wh_per_dollar)
    # print("Under 100 Wh: ", under_100_wh)


if __name__ == "__main__":
    main()
