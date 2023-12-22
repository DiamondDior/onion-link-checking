import requests
from bs4 import BeautifulSoup
import logging

# Setup logging , on error see script_log.log and send to me
logging.basicConfig(filename='script_log.log', level=logging.INFO, format=''%(asctime)s %(levelname)s:%(message)s'')

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# Tor Connection Check
logging.info("Tor Connection Check")
try:
    system_ip = requests.get('https://ident.me', proxies=proxies).text
    tor_ip_list = requests.get('https://check.torproject.org/exit-addresses').text
    if system_ip in tor_ip_list:
        logging.info(f'Tor_IP: {system_ip}')
        logging.info("Tor Connection Success")
    else:
        logging.error('IP not in Tor exit node list')
except Exception as e:
    logging.error(f"Error establishing Tor connection: {e}")
    exit()

# Read Onion URLs from a File
in_file = input("Submit the URL File: ")
try:
    input_file = open(in_file, 'r')
except FileNotFoundError:
    logging.error("File not found")
    exit()

# Web Scraping through Tor
for url in input_file:
    url = url.strip()
    try:
        response = requests.get(url, proxies=proxies, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            page_title = soup.title.string if soup.title else 'No title'
            logging.info(f'Active: {url} - {page_title}')
        else:
            logging.info(f'Inactive (HTTP {response.status_code}): {url}')
    except requests.RequestException as e:
        logging.error(f'Error accessing {url}: {e}')

input_file.close()
