# online-retail-stock-checker-alerter
Checks online retail stores for item stock and alerts if found

Currently being used for PS5 stock, can be edited to support more stores and products

# I don't know what python is:
## ONLY WORKS ON WINDOWS
- Create a Twilio account here https://www.twilio.com/ 
- Get Account SID, auth token, a twilio phone number and verify your own phone number
- Make sure to install latest chrome update (Version 86)
- Run stock_alerter.exe on dist/stock_alerter folder
- You will be prompted for twilio information to be able to send text messages

# I know what python is:
- (Optional) Built using PyInstaller (pip install PyInstaller)
- pip install selenium 
- donwload selenium webdriver for chrome and put on same relative path as stock_alerter.py/stock_alerter.exe
- pip install twilio
- run stock_alerter.py
