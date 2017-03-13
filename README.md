Latest Version: 1.2.1

# AdidasQueuer

# Setup

0. Download & Install python 3.x from https://www.python.org/downloads/. Be sure to check "Add to PATH" when installing.
1. Open cmd as Administrator
2. Change directory to AdidasQueuer folder. Example: `cd C:\Users\Hunter\Desktop\AdidasQueuer`
2. `pip3 install -r requirements.txt`

# Run

0. Add proxies(if any) to proxies.txt
1. Open cmd as Administrator
2. Change directory to AdidasQueuer folder. Example: `cd C:\Users\Hunter\Desktop\AdidasQueuer`
3. `python3 AdidasQueuer.py`

# How it Works
This will take all your proxies(if provided) and refresh the adidas splash page url you provide. It may seem like nothing is happening, but don't worry, it is still refreshing in the background. Once one of the proxies gets through the queue, it will open a chrome session and take you to the size selection page, from there you can just add to card and process as normal. If one makes it through the queue, the others will still keep trying and will always keep trying until they either get through queue or you exit the script.

For simply questions please Google it first
DM me on twitter @hunter_bdm for further questions.

# Testing
You can test with any adidas page that has a google captcha