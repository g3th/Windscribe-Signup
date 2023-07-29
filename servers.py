import requests
import subprocess
import time

from pathlib import Path
from bs4 import BeautifulSoup as soup

configuration_download_page_links = []
page = 'https://www.vpngate.net/en/'


class DownloadOvpnConfig:

    def __init__(self):

        self.vpn_gate_request = requests.get(page)
        self.parse_vpn_gate_request = soup(self.vpn_gate_request.text, 'html.parser')
        self.obtain_all_page_links = self.parse_vpn_gate_request.find_all(href=True)
        self.all_page_links = ''

    def get_all_page_links(self):

        self.all_page_links = list(self.obtain_all_page_links)
        for link in self.all_page_links:
            if 'do_openvpn.aspx' in str(link):
                configuration_download_page_links.append(str(link).split('"')[1].replace('&amp;', '&'))

        return configuration_download_page_links


def download_config(config_url, file_number):
    download = config_url
    fetch_configuration_file_bytes = requests.get(config_url).content
    with open('config_files/config' + str(file_number) + '.ovpn', 'wb') as open_vpn_file:
        open_vpn_file.write(fetch_configuration_file_bytes)


def get_ovpn_configuration_link(page_link):
    config_download_page_links = page_link
    download_page_request = requests.get(config_download_page_links)
    download_page_links = soup(download_page_request.text, 'html.parser')
    obtain_download_page_links = download_page_links.find_all(href=True)
    ovpn_configuration_link = page[:-4] + str(obtain_download_page_links[35:36]).split('"')[1].replace('&amp;', '&')
    return ovpn_configuration_link


class connect_to_vpn:

    def __init__(self):

        self.ovpn_config = ['nmcli', 'connection', 'import', 'type', 'openvpn', 'file']
        self.connect = ['nmcli', 'connection', 'up']
        self.delete_connection = ['nmcli', 'connection', 'delete', 'id']

    def set_up_nmcli_connection(self, index):
        self.ovpn_config.insert(6, str(Path(__file__).parent) + '/config_files/config' + str(index) + '.ovpn')
        self.connect.insert(3, 'config' + str(index))
        self.delete_connection.insert(4, 'config' + str(index))
        nmcli_add_vpn = subprocess.run(self.ovpn_config, shell=False, stdout=subprocess.DEVNULL)
        nmcli_connect_vpn = subprocess.run(self.connect, shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        return nmcli_connect_vpn.stderr

    def delete_list_elements(self):
        del self.ovpn_config[6]
        del self.connect[3]
        del self.delete_connection[4]

    def ping_connection(self):
        ping_command = ['ping', '-c1', '8.8.8.8']
        ping_the_connection = subprocess.run(ping_command, shell=False, stdout=subprocess.PIPE)
        return ping_the_connection.stdout

    def fetch_IPaddr(self):
        while True:
            try:
                fetch_current_ip_address = requests.get('http://httpbin.org/ip')
                scrape_current_ip_url = requests.get('https://www.showmyip.com/')
                fetch_current_city = soup(scrape_current_ip_url.text, 'html.parser')
                current_ip_city = fetch_current_city.find_all('tr')
                human_readable_ip_address = fetch_current_ip_address.text.split('"')[3].strip(" ")
                human_readable_city = current_ip_city[4].text.replace('City', '').strip()
                return human_readable_ip_address, human_readable_city
            except IndexError:
                print("HTTP Bin Timeout: Retrying in 3 seconds.")
                time.sleep(3)

    def delete_nmcli_connection(self):
        subprocess.run(self.delete_connection, shell=False, stdout=subprocess.DEVNULL)
