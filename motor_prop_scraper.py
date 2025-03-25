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


      
