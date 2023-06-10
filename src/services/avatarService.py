import os
import requests
import re
import time

import instaloader

from bs4 import BeautifulSoup

#todo: refactor this code to different services


def get_telegram_user_avatar(username, save_directory):
    # Retrieve the HTML content of the user's profile page
    profile_url = f"https://t.me/{username}"
    response = requests.get(profile_url)
    html_content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the avatar image URL within the parsed HTML
    avatar_element = soup.find('img', class_='tgme_page_photo_image')
    if avatar_element:
        avatar_url = avatar_element['src']
        avatar_response = requests.get(avatar_url)

        # Save the avatar image
        avatar_file_path = os.path.join(save_directory, f"{username}.jpg")
        with open(avatar_file_path, 'wb') as file:
            file.write(avatar_response.content)

        return avatar_file_path

    return None


def get_telegram_user_name(username):
    # Retrieve the HTML content of the user's profile page
    profile_url = f"https://t.me/{username}"
    response = requests.get(profile_url)
    html_content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the user's name within the parsed HTML
    name_element = soup.find('div', class_='tgme_page_title')
    if name_element:
        name = name_element.text.strip()
        return name

    return 'Contact'


def extract_instagram_nickname(string):
    # Regular expression pattern to match Instagram profile URLs
    pattern = r'(?:http[s]?://)?(?:www\.)?(?:instagram\.com/)([\w\.\_]+)'

    # Search for the pattern in the input string
    match = re.search(pattern, string)

    if match:
        # Extract the nickname (username) from the matched group
        nickname = match.group(1)
        return nickname

    return None


def extract_facebook_name_from_page(url):
    # Send a GET request to the Facebook profile page
    response = requests.get(url)
    print(response.content)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the element containing the profile name
        profile_name_element = soup.find('h1', class_='_2nlw _2nlv')

        if profile_name_element:
            # Extract the profile name text
            profile_name = profile_name_element.text

            # Split the profile name into first name and last name
            names = profile_name.split()

            if len(names) > 1:
                first_name = names[0]
                last_name = names[1]
                return first_name, last_name
            else:
                return names[0], ''

    return None, None


def extract_telegram_nickname(text):
    # Regular expression pattern to match Telegram nicknames
    pattern = r"(?:@|t\.me/|https?://t\.me/)(\w+)"

    # Find the first match in the text
    match = re.search(pattern, text)

    if match:
        # Extract the nickname from the match
        nickname = match.group(1)
        return nickname

    # If no match found, return None
    return None


#todo: BLOCKER FIX IT
def get_instagram_avatar(nickname):
    # Create an instance of Instaloader
    loader = instaloader.Instaloader()

    loader.login("kakalulu11", "kakalulu7677")
    time.sleep(2)

    try:
        # Load the profile based on the nickname
        profile = instaloader.Profile.from_username(loader.context, nickname)

        time.sleep(3)

        # Download the profile picture (avatar)
        loader.download_profilepic(profile.username)

        # Get the default saved filename
        filename = loader.context.filename_template

        # Construct the new filename with the desired format
        new_filename = f"{nickname}.jpg"

        # Construct the destination directory and filename
        destination = os.path.join("src/services/img/avatar", new_filename)

        # Rename the downloaded profile picture to the desired filename and move it to the destination directory
        os.rename(filename, destination)

        print("Instagram avatar saved successfully.")
    except instaloader.exceptions.ProfileNotExistsException:
        print("Profile does not exist.")
    except Exception as e:
        print("An error occurred:", str(e))

