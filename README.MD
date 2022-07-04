# Windscribe Account Maker #

## 10GB Account with Email Verification ##

### Completely automates the registration process, and creates 5 accounts ###

This account maker uses VPN Gate and Developer Email api in order to register for a free
Windscribe account. 

It will select a random VPN Gate server, connect with Network-Manager, and ping google to determine if the connection is valid. In the future Tracert might be added to determine speed and discard slow connections.

It will then launch the browser, generate user credentials (username, 10 digit alpha-numeric password and email), enter the credentials into the open automated-browser and take a screenshot of the browser.

The Pillow image library will crop the screenshot, leaving just the captcha box in order for Tesseract to work its magic (or get it wrong, mostly by one letter).

Finally the automation will enter the captcha, create the account, and fetch the verfication link.

The program works most times, however since Tesseract is involved, it does not have a 100% captcha-recognition rate. There is also the likelyhood of current temporary email domain quickly being blocked.

---------------------------------------------------------------

### Requires: ##

Network Manager and OpenVPN:

```sudo apt-get install network-manager-gnome-openvpn && apt-get install openvpn```

Tesseract:

```sudo apt-get install tesseract-ocr```

Chromedriver:

```sudo apt-get install chromium-driver```

Selenium:

```pip3 install selenium```

Pytesseract library:

```pip3 install pytesseract```

Pillow Library:

```pip3 install Pillow```

Beautiful Soup 4:

```pip3 install bs4```
