'''
Aim: Convert a list of links (scraped through in-console JS) into a structured database focussing on the performance of motor-propeller combinations

Method:
- Get all links from https://database.tytorobotics.com/tests (couldn't find a computer friendly database file containing all the information).
- Convert each link into markdown using markdownify, should make it easier to isolate important features.
- Download the csv file from each link
- Combine the motor name, propeller name and csv data
- ???
- profit


'''

import os
from markdownify import markdownify
import requests
from pathlib import PureWindowsPath

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import csv
import pandas as pd


def concatenate_txt_files(folder_path, output_file):
    """
    Concatenates all .txt files in a given folder into a single output file.
    
    :param folder_path: Path to the folder containing .txt files.
    :param output_file: Path to the output file.
    """
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".txt"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read() + "\n")  # Ensure each file's content is separated by a newline
    print(f"All text files concatenated into {output_file}")

# concatenate_txt_files("data/tytolinks", "data/compiled_tyto_links.txt")


def get_markdown_from_url(url):
  """
  Fetches the content from a URL and converts it to markdown.

  Args:
    url: The URL to fetch content from.

  Returns:
    The markdown content from the URL.
  """

  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    html_content = response.content.decode('utf-8')
    markdown_content = markdownify(html_content)
    return markdown_content
  except requests.exceptions.RequestException as e:
    print(f"Error fetching URL: {e}")
    return None
  
def test_selenium():
   driver = webdriver.Firefox()
   driver.get("http://www.python.org")

def get_latest_file(directory):
    """Find the most recently downloaded file in the given directory."""
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".csv")]
    return max(files, key=os.path.getctime) if files else None

def add_column_to_csv(csv_file_path, column_name, column_value):
   df = pd.read_csv(csv_file_path)
   number_of_rows = df.shape[0]
   column_values = [column_value for i in range(number_of_rows)]
   df[column_name] = column_values
   df.to_csv(csv_file_path, index=False)

def download_csv(url):
   driver = webdriver.Firefox()
   driver.get(url)
   try:
     csv_button = driver.find_element(By.CLASS_NAME, "buttons-csv")
   except Exception as e:
     print("No csv button, quitting")
     return None

   try:
    motor_name = driver.find_element(By.XPATH, "/html/body/div/div/main/div/div/div/div[2]/div[2]/div[1]/div/a").text
    propeller_name = driver.find_element(By.XPATH, "/html/body/div/div/main/div/div/div/div[2]/div[2]/div[2]/div/a").text
   except Exception as e:
     print(e)
     motor_name = url
     propeller_name = 'undefined'
     
   print(motor_name)
   print(propeller_name)
   csv_button.click()
   driver.close()

   latest_csv_file_path = get_latest_file(PureWindowsPath(r"c:\Users\patel\Dropbox\My PC (LAPTOP-KIK1NF3V)\Downloads"))
   add_column_to_csv(latest_csv_file_path, "Motor_Name", motor_name)
   add_column_to_csv(latest_csv_file_path, "Propeller_Name", propeller_name)

def number_of_files(directory):
  lst = os.listdir(directory) # your directory path
  number_files = len(lst)
  return number_files

def normalize_throttle(csv_file,export_folder='data/tyto_throttled_csv/'):
  df = pd.read_csv(csv_file)
  throttles = df['Throttle (µs)']
  max_throttle = max(throttles)
  min_throttle = min(throttles)

  new_throttles = (throttles - min_throttle) / (max_throttle - min_throttle)

  df.rename(columns={'Throttle (µs)':'Throttle'}, inplace=True)
  df['Throttle']=new_throttles
  
  csv_file_object = PureWindowsPath(csv_file)
  file_name = csv_file_object.name
  export_path = export_folder+file_name
  print(export_path)
  df.to_csv(export_path, index=False)
  
def combine_csvs(directory,export_file='data/compiled_tyto_data.csv'):
  csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

  # Create an empty list to store DataFrames
  dfs = []

  # Read each CSV file and append to list
  for file in csv_files:
      file_path = os.path.join(directory, file)
      df = pd.read_csv(file_path)  # Read CSV file
      dfs.append(df)

  # Combine all DataFrames into one
  combined_df = pd.concat(dfs, ignore_index=True)
  combined_df.to_csv(export_file,index=False)
  
  
if __name__ == "__main__":
  combine_csvs('data/tyto_throttled_csv')


