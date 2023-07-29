#!/usr/bin/python3

import servers
import time
import os
import shutil
import concurrent.futures
from requests.exceptions import ConnectionError
from urllib3.exceptions import ProtocolError

from header import titleHeader
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from pathlib import Path
from generator import password_generator, username_generator, write_credentials_to_file
from registration import registration_process
from email_confirmation import confirmation_email

vpngate = 'https://www.vpngate.net/en/'
browser_screenshot_file_path = 'config_files/my_screenshot.png'
captcha_screenshot_file_path = 'config_files/captcha_image.png'
file_path = str(Path(__file__).parent)
p = password_generator()
u = username_generator()
connect = servers.connect_to_vpn()
open_vpn = servers.DownloadOvpnConfig()
tempmail = confirmation_email()

if __name__ == '__main__':

    downloading_links_list = []
    futures_list = []
    downloading_urls = []
    configuration_number = 1
    user_directory = str(Path(__file__).parent)

    try:
        current_time = ' '.join(time.ctime().split(" ")[1:3]) + " " + str(time.ctime()).split(" ")[4]
        file_creation_time = (' '.join(
            time.ctime(os.path.getctime(user_directory + "/config_files/config1.ovpn")).split(" ")[1:3]) +
                              " " + str(
                    time.ctime(os.path.getctime(user_directory + "/config_files/config1.ovpn")).split(" ")[4]))
    except FileNotFoundError:
        current_time = 0
        file_creation_time = 0

    titleHeader()
    while True:
        print("Using Open VPN may be considerably slower, due to the service being")
        print("primarily suited to research and educational purposes. Some OVPN connections")
        print("may not work, others may be slow, and yet others will be denied by the temp email api.\n")
        user_input = input("Would you like to skip Open VPN connection and use your own VPN? (y/n)")
        if user_input == 'y':
            openvpn_skip_connection = True
            break
        elif user_input == 'n':
            openvpn_skip_connection = False
            break
        else:
            print("Invalid value")

    if current_time != file_creation_time and not openvpn_skip_connection or current_time == 0 and not openvpn_skip_connection:
        shutil.rmtree(file_path + '/config_files')
        os.makedirs(file_path + '/config_files')

        with open('config_files/openvpn_config_url_list', 'a') as openvpn_urls:
            for link in open_vpn.get_all_page_links():
                openvpn_urls.write(vpngate + link + "\n")
        openvpn_urls.close()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            with open('config_files/openvpn_config_url_list', 'r') as configs:

                for line in configs.readlines():
                    thread = executor.submit(servers.get_ovpn_configuration_link, line)
                    futures_list.append(thread)

                print('Creating OVPN.config download pages list')

                for returned_value in futures_list:
                    result = returned_value.result()
                    downloading_urls.append(result)

                print('Downloading OVPN configuration files')

                for url in downloading_urls:
                    executor.submit(servers.download_config, url, str(configuration_number))
                    configuration_number += 1
    elif current_time == file_creation_time and not openvpn_skip_connection:
        print("Downloaded files are recent. Skipping")
        time.sleep(4)

    # Start Index at chosen location (i.e. index = 40), as long as not exceeding number of total downloaded vpn configs
    # It is recommended to start this at 30 or 40, as IPs early in the list are unlikely to work
    index = 55
    number_of_created_accounts = 0
    while number_of_created_accounts < 5:
        flag = 0
        titleHeader()
        if not openvpn_skip_connection:
            print('Connecting to VPN...')
            if 'Error' in str(connect.set_up_nmcli_connection(index)):
                print('Connection Refused')
                time.sleep(0.5)
                flag = 1
            if '0 received' in str(connect.ping_connection()):
                print('Connection Timed Out')
                time.sleep(0.5)
                flag = 1
            elif flag == 0:
                print('Connection Successful. Current IP: {}'.format(
                    connect.fetch_IPaddr()[0] + ' - City: ' + connect.fetch_IPaddr()[1]))
        try:
            registration = registration_process()
            username = u.generate_a_username()
            password = p.generate_password(10)
            email = str(tempmail.create_an_email_address()) + '@developermail.com'
            registration.enter_signup_credentials(username, password, email)
            time.sleep(2)
            registration.take_browser_screenshot(browser_screenshot_file_path)
            registration.resize_the_screenshot()
            captcha_result = registration.read_captcha_by_ocr(captcha_screenshot_file_path).strip()

            if registration.enter_captcha(captcha_result):
                print('Tesseract read it wrong, restarting...')
                time.sleep(2)
                registration.close_browser()

            else:
                tempmail.get_confirmation_link_email()
                tempmail.click_confirmation_link()
                registration.delete_all_screenshots(browser_screenshot_file_path, captcha_screenshot_file_path)
                write_credentials_to_file(username, password, email)
                registration.close_browser()
                number_of_created_accounts += 1

        except (ConnectionResetError, ProtocolError, ConnectionError):
            print("Aborted, trying new connection")
            time.sleep(1.8)
            index += 1

        except (ElementNotInteractableException, NoSuchElementException):
            print("Aborted, trying new connection")
            time.sleep(1.8)
            index += 1

        index += 1
        if not openvpn_skip_connection:
            connect.delete_nmcli_connection()
            connect.delete_list_elements()
