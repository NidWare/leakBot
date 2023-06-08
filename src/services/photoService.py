from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
from . import avatarService


def getTelegramImage(user_name, name_text):
    avatarService.get_telegram_user_avatar(user_name, 'src/services/img/avatar')
    # Load the image of the iPhone screen
    img = Image.open('src/services/img/telegram.jpg')
    draw = ImageDraw.Draw(img)

    # Set font for name text and create the text object
    name_font = ImageFont.truetype("src/services/font/font.otf", 22)

    # Get the bounding box of the name text
    name_text_bb = draw.textbbox((0, 0), name_text, font=name_font)

    # Calculate the x-coordinate for the center of the navbar
    navbar_center_x = img.width / 2

    # Calculate the y-coordinate for the center of the navbar
    navbar_center_y = 50

    # Calculate the x-coordinate for the left side of the name text
    name_text_x = navbar_center_x - ((name_text_bb[2] - name_text_bb[0]) / 2)

    # Calculate the y-coordinate for the top of the name text
    name_text_y = navbar_center_y - ((name_text_bb[3] - name_text_bb[1]) / 2) + 30

    # Draw the name text on the navbar
    draw.text((name_text_x, name_text_y), name_text, font=name_font, fill=(0, 0, 0))

    # Load the user avatar image
    try:
        avatar = Image.open('src/services/img/avatar/{}.jpg'.format(user_name))
    except:
        avatar = Image.open('src/services/img/blocked.png')

    # Create a new RGBA image with white background
    avatar_alpha = Image.new("RGBA", avatar.size, (255, 255, 255, 0))

    # Convert the avatar image to RGBA mode
    avatar_rgba = avatar.convert("RGBA")

    # Resize the avatar image to 60x60 pixels
    avatar_resized = avatar_rgba.resize((60, 60), Image.ANTIALIAS)

    # Create a circular mask for the avatar
    mask = Image.new('L', avatar_resized.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, avatar_resized.size[0], avatar_resized.size[1]), fill=255)

    # Apply the circular mask to the resized avatar
    avatar_masked = ImageOps.fit(avatar_resized, mask.size, centering=(0.5, 0.5))
    avatar_masked.putalpha(mask)

    # Calculate the x-coordinate for the right side of the navbar
    navbar_right_x = img.width - 10

    # Calculate the y-coordinate for the top of the avatar image
    avatar_top_y = int(name_text_y + (name_text_bb[3] - name_text_bb[1]) / 10) - 10

    # Calculate the x-coordinate for the left side of the avatar image
    avatar_left_x = int(navbar_right_x - 60)

    # Paste the masked avatar image onto the navbar
    img.paste(avatar_masked, (avatar_left_x, avatar_top_y), avatar_masked)

    # Save the modified image
    img.save("src/services/img/user/{}.png".format(user_name))


def getInstagramImage(user_name, name_text):

    # Load the image of the iPhone screen
    img = Image.open('src/services/img/instagram.jpg')
    draw = ImageDraw.Draw(img)

    # Set font for name text and create the text object
    name_font = ImageFont.truetype("src/services/font/font.otf", 22)

    # Get the bounding box of the name text
    name_text_bb = draw.textbbox((0, 0), name_text, font=name_font)

    # Calculate the x-coordinate for the center of the navbar
    navbar_center_x = img.width / 2

    # Calculate the y-coordinate for the center of the navbar
    navbar_center_y = 50

    # Calculate the x-coordinate for the left side of the name text
    name_text_x = navbar_center_x - ((name_text_bb[2] - name_text_bb[0]) / 2)

    # Calculate the y-coordinate for the top of the name text
    name_text_y = navbar_center_y - ((name_text_bb[3] - name_text_bb[1]) / 2) + 55

    # Draw the name text on the navbar
    draw.text((name_text_x, name_text_y), name_text, font=name_font, fill=(0, 0, 0))

    try:
        avatar = Image.open('src/services/img/avatar/{}'.format(user_name))
    except:
        avatar = Image.open('src/services/img/blocked.png')

    # Create a new RGBA image with white background and paste the avatar alpha channel onto it
    avatar_alpha = Image.new("RGBA", avatar.size, (0, 0, 0, 0))
    avatar_alpha.putalpha(avatar.convert("L"))

    # Set the size of the avatar image to 60x60 pixels
    avatar_alpha = avatar_alpha.resize((60, 60))

    # Create a circular mask for the avatar
    mask = Image.new('L', avatar_alpha.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, avatar_alpha.size[0], avatar_alpha.size[1]), fill=255)

    # Apply the circular mask to the avatar
    avatar_alpha = ImageOps.fit(avatar_alpha, mask.size, centering=(0.5, 0.5))
    avatar_alpha.putalpha(mask)

    # Calculate the x-coordinate for the right side of the navbar
    navbar_right_x = img.width - 10

    # Calculate the y-coordinate for the top of the avatar image
    avatar_top_y = int(name_text_y + (name_text_bb[3] - name_text_bb[1]) / 10) - 10

    # Calculate the x-coordinate for the left side of the avatar image
    avatar_left_x = int(navbar_right_x - 500)

    # Paste the avatar image onto the navbar
    img.paste(avatar_alpha, (avatar_left_x, avatar_top_y), avatar_alpha)

    # Save the modified image
    img.save("src/services/img/user/{}.png".format(user_name))


def getFacebookImage(user_id, name_text):
    # Load the image of the iPhone screen
    img = Image.open('src/services/img/facebook.jpg')
    draw = ImageDraw.Draw(img)

    # Set font for name text and create the text object
    name_font = ImageFont.truetype("src/services/font/font.otf", 22)

    # Get the bounding box of the name text
    name_text_bb = draw.textbbox((0, 0), name_text, font=name_font)

    # Calculate the x-coordinate for the center of the navbar
    navbar_center_x = img.width / 2

    # Calculate the y-coordinate for the center of the navbar
    navbar_center_y = 50

    # Calculate the x-coordinate for the left side of the name text
    name_text_x = navbar_center_x - ((name_text_bb[2] - name_text_bb[0]) / 2)

    # Calculate the y-coordinate for the top of the name text
    name_text_y = navbar_center_y - ((name_text_bb[3] - name_text_bb[1]) / 2) + 48

    # Draw the name text on the navbar
    draw.text((name_text_x, name_text_y), name_text, font=name_font, fill=(0, 0, 0))

    # Save the modified image
    img.save("src/services/img/user/{}.png".format(user_id))


def delete_user_photo(name):
    # construct path to file
    path = f"src/services/img/user/{name}.jpg"
    # check if file exists
    if os.path.isfile(path):
        # delete file
        os.remove(path)
        print(f"{path} deleted successfully")
    else:
        print(f"{path} not found")

