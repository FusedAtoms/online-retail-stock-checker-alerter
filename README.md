# online-retail-stock-checker-alerter
Checks online retail stores for item stock and alerts if found

Currently being used for PS5 stock, can be edited to support more stores and products

# I don't know what python is:
## ONLY WORKS ON WINDOWS 10 x64
- Create a Twilio account here https://www.twilio.com/ 
- Get Account SID, auth token, a twilio phone number and verify your own phone number from Twilio
- Make sure to install latest chrome update (Version 86)
- Download stock_alerter.rar on https://github.com/FusedAtoms/online-retail-stock-checker-alerter/releases/tag/v0.1
- Extract into a folder
- Run stock_alerter.exe
- You will be prompted for twilio information for program to be able to send text messages to you
- All set, if stock is found you will receive a text message every 5 minutes while it lasts

# I know what python is:
- (Optional) Built using PyInstaller (pip install PyInstaller)
- pip install selenium 
- donwload selenium webdriver for chrome and put on same relative path as stock_alerter.py/stock_alerter.exe
- pip install twilio
- run stock_alerter.py
