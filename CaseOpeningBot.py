from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

from discord_webhooks import DiscordWebhooks

from datetime import datetime

from pyfiglet import Figlet

import questionary
from questionary import Validator, ValidationError

from os import system, name
from time import sleep


# Classes
class NameValidator(Validator):
    def validate(self, document):
        if len(document.text) == 0:
            raise ValidationError(
                message="Please enter a value",
                cursor_position=len(document.text),
            )


# Functions
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def inputUsername():
    userElement = driver.find_element_by_id("username")
    userElement.clear()
    userElement.send_keys(username)


def inputPassword():
    passwordElem = driver.find_element_by_id("password")
    passwordElem.clear()
    passwordElem.send_keys(password)


def submitButton():
    button = driver.find_element_by_xpath("//button[contains(text(),'Log In')]")
    button.send_keys(Keys.RETURN)
    driver.implicitly_wait(30)


def submitKeyButton():
    keyButton = driver.find_element_by_xpath(
        "//body/div[@id='root']/div[1]/div[1]/div[1]/div[1]/div[3]/div[2]/div[1]/div[3]/a[3]/img[1]")
    keyButton.click()
    driver.implicitly_wait(30)


def findKeyNumber():
    keyNumber = driver.find_element_by_xpath(
        "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]")
    numberOfKeys = int(keyNumber.text)  # number of keys
    return numberOfKeys


def useKey():
    key = driver.find_element_by_xpath("//button[contains(text(),'Use A Golden Key')]")
    key.click()
    driver.implicitly_wait(30)


def chooseMode():
    answer = questionary.select(
        "What mode do you want to use?",
        choices=["1) Force Load Keys", "2) Open Cases"],
    ).ask()
    return answer

## Main code

ChromeDriverManager("2.26", log_level=0).install() # make it so webdriver_manager doesn't print logs to console

f = Figlet(font='slant')
questionary.print(f.renderText('TunesBot'), style="fg:darkred")

mode = chooseMode()  # Choose mode
questionary.print('Loading mode...', style="fg:darkred")
sleep(1)
clear()

# Get username and password
print("Enter your login information."
      "")
username = questionary.text("Username:", validate=NameValidator).ask()
password = input(f"? Password: ")

##############################################################################
# Discord
discordWebhook = 'https://discord.com/api/webhooks/792858525386539048/YCw-58sqII1WeF3oRFHMkeOQMIn2P6xBk-MWPX-Y7p_kuZ0m-1Ltn9Tv38we9tGfCw1I'

webhook = DiscordWebhooks(discordWebhook)
time = datetime.utcfromtimestamp(1609123273)
webhook.set_content(title='<:twitch:792948187207696414> Click to watch stream <:twitch:792948187207696414>',
                    url='https://www.twitch.tv/directory/game/Aim%20Gods', color=0xf8e71c, timestamp=str(time))
webhook.set_thumbnail(
    url='https://pbs.twimg.com/profile_images/1221031786114736128/WX_zv0XN_400x400.jpg')  # Attaches a thumbnail
webhook.set_footer(text="TunesBot",
                   icon_url="https://pbs.twimg.com/profile_images/1221031786114736128/WX_zv0XN_400x400.jpg")  #
# Attaches a footer
webhook.add_field(name="-------------------------------",
                  value=str(username) + ", you have no keys @here <:noosethink:792948666070466561>.")

##############################################################################

# Headless
headless = questionary.confirm("Do you want to run headless? (Improves performance)", default=True).ask()
chrome_options = webdriver.ChromeOptions()
if headless:
    chrome_options.headless = True
    questionary.print('Running headless browser...', style="fg:darkred")
else:
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# Open browser

driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=chrome_options) # Initiate browser windows
driver.get("https://aimgods.finalmouse.com/auth/log-in")  # Open browser on this URL

# Login
inputUsername()  # Input the username into the text field
inputPassword()  # Input the username into the text field
submitButton()  # Submit the username and password to log in

# Click key button
submitKeyButton()  # Click the button with the image of the key

# Read number of keys
keys = findKeyNumber()

while True:
    if mode[0] == '1':
        if keys == 0:
            counter = 0
            while counter < 10:
                while keys == 0 and counter < 10:
                    counter += 1
                    driver.refresh()
                    driver.implicitly_wait(5)
                cont = questionary.confirm("Do you want to continue force refreshing?", default=True).ask()
                if cont:
                    counter = 0
                else:
                    break
        print("You have " + str(keys) + " keys.")
        break

    elif mode[0] == '2':
        while keys > 1:
            useKey()  # Click use key button

            # Click play again button
            elem = driver.find_element_by_xpath("//button[contains(text(),'Play Again!')]")
            elem.click()
            driver.implicitly_wait(30)

        webhook.send()
        break

    else:
        print("Invalid mode")
        mode = chooseMode()
driver.close()
