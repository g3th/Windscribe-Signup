# Windscribe Account Maker (Kali/Debian/Linux) #

## 10GB Account with Email Verification ##

### Completely automates the registration process, and creates 5 accounts ###

https://user-images.githubusercontent.com/74467654/178326839-48104687-10f5-4c82-ba00-daea1f1372fb.mp4

*Important : Likely current temp email will be blocked by sysadmins. If you have valid Temp-Email RapidApi api-key (Basic, free) let me know.*

Uses VPN Gate and Developer Email api in order to register for free Windscribe account. 

Downloads and selects VPN Gate ovpn config using threading, and connects with nmcli.

Launches chrome, generates credentials (user, 10 digit alpha-num pass and email), takes browser screenshot.

Enters captchas, solves w/ Tesseract and fetches verfication link.

Due to free nature of VPN Gate, it might take a long time. It is recommended to start VPN Index at a integer greater than 30, due to the fact that previous VPN IPs in the list are blocked, as they are mainly used for University research and are not residential.

The errors will automatically be detected and the script restarted. These mainly are:

1) Cloudflare blocks (i.e. Access Denied, IUAM etc)
2) Blocked elements in page (i.e. click button is not clickable by automation)
3) Timeouts, refused connections etc...
4) Tesseract getting it wrong sometimes

It was built only as an excercise, not to abuse a service, and 5 accounts are more than enough.

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
