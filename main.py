import telebot
import sqlite3
import src.messages
import datetime
import random
import os
import src.services.photoService
import src.services.avatarService
from src.keyBoards import get_welcome_keyboard, get_search_keyboard, get_buy_keyboard, get_check_payment_keyboard, get_payment_keyboard
from src.services.dateService import random_date
from src.config import token, wallet

user_state = {}

bot = telebot.TeleBot(token)

# Step 1: Welcome message with buttons "Search" and "Info"
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, src.messages.WELCOME_TEXT, reply_markup=get_welcome_keyboard())


# Step 2: Handling callback query for "Search" option
@bot.callback_query_handler(func=lambda call: call.data == 'search')
def handle_search_option(call):
    bot.send_message(call.message.chat.id, src.messages.SEARCH_TEXT, reply_markup=get_search_keyboard())


# Step 3: Handling callback query for contact options (phone, telegram, instagram, facebook)
@bot.callback_query_handler(func=lambda call: call.data in ['phone', 'telegram', 'instagram', 'facebook'])
def handle_contact_option(call):
    user_state[call.message.chat.id] = call.data
    bot.send_message(call.message.chat.id, src.messages.RESPONSE_TEXT_GET_CONTACT[call.data])


# Step 4: Handling user input and displaying loader
@bot.message_handler(func=lambda message: True)
def handle_user_input(message):
    if user_state[message.chat.id] is not None:
        # Display loader message
        send_loader(message)

        bot.send_message(message.chat.id, get_contact_found_message(message))
        contact_name = user_state[message.chat.id].capitalize()
        del user_state[message.chat.id]
        # Display the buy options
        bot.send_message(message.chat.id, src.messages.PHOTOS_FOUND.format(contact_name), reply_markup=get_buy_keyboard())


def get_contact_found_message(message):
    if user_state.get(message.chat.id) is None:
        return src.messages.NO_CONTACT_TYPE

    if user_state[message.chat.id] == 'phone':
        response_text = src.messages.RESPONSE_TEXT_FOUND_CONTACT[user_state[message.chat.id]].format(message.text, get_random_date(), get_random_date(), get_random_date())

    elif user_state[message.chat.id] == 'telegram':
        nickname = src.services.avatarService.extract_telegram_nickname(message.text)
        src.services.avatarService.get_telegram_user_avatar(nickname, 'src/services/img/avatar/')
        src.services.photoService.getTelegramImage(nickname, src.services.avatarService.get_telegram_user_name(nickname))
        response_text = src.messages.RESPONSE_TEXT_FOUND_CONTACT[user_state[message.chat.id]].format(message.text, get_random_date(), get_random_date(), get_random_date())

        try:
            send_photo_with_name(message.chat.id, nickname)
        except:
            print('exception because of user name')
            pass
    elif user_state[message.chat.id] == 'instagram':

        nickname = src.services.avatarService.extract_instagram_nickname(message.text)
        # src.services.avatarService.get(nickname, 'src/services/img/avatar/')
        src.services.photoService.getInstagramImage(nickname, nickname)
        # src.services.avatarService.get_telegram_user_name(nickname))

        response_text = src.messages.RESPONSE_TEXT_FOUND_CONTACT[user_state[message.chat.id]].format(message.text, get_random_date(), get_random_date(), get_random_date())

        try:
            send_photo_with_name(message.chat.id, nickname)
        except:
            print('exception because of user name')
            pass

    elif user_state[message.chat.id] == 'facebook':
        response_text = src.messages.RESPONSE_TEXT_FOUND_CONTACT[user_state[message.chat.id]].format('Facebook Page Name', message.text, get_random_date(), get_random_date(), get_random_date())

        try:
            send_photo_with_name(message.chat.id, message.from_user.name)
        except:
            print('exception because of user name')
            pass
    else:
        response_text = src.messages.NO_CONTACT_TYPE

    return response_text


def send_photo_with_name(chat_id, name):
    # Define the path of the photo
    photo_path = f'src/services/img/user/{name}.png'

    # Check if the photo file exists
    if not os.path.isfile(photo_path):
        print(f"Photo file not found for name: {name}")
        return

    try:
        with open(photo_path, 'rb') as photo_file:
            # Send the photo to the specified chat ID
            bot.send_photo(chat_id, photo_file)
            print(f"Photo sent successfully for name: {name}")
    except Exception as e:
        print(f"Failed to send photo for name: {name}. Error: {e}")


def send_photo_with_instagram_name(chat_id, name):
    # Define the path of the photo
    photo_path = f'src/services/img/user/{name}_inst.png'

    # Check if the photo file exists
    if not os.path.isfile(photo_path):
        print(f"Photo file not found for name: {name}")
        return

    try:
        with open(photo_path, 'rb') as photo_file:
            # Send the photo to the specified chat ID
            bot.send_photo(chat_id, photo_file)
            print(f"Photo sent successfully for name: {name}")
    except Exception as e:
        print(f"Failed to send photo for name: {name}. Error: {e}")

# Step 7: Handling callback query for "Buy" and "Buy an unlimited service subscription" options
@bot.callback_query_handler(func=lambda call: call.data in ['buy', 'unlimited'])
def handle_buy_option(call):
    bot.send_message(call.message.chat.id, src.messages.CHOOSE_OPTION, reply_markup=get_payment_keyboard(call.data))


# Step 9: Handling callback query for "Payment" and "Instructions" options
@bot.callback_query_handler(func=lambda call: call.data.startswith('payment') or call.data == 'instructions' or call.data == 'cancel')
def handle_payment_option(call):
    # Establishing connection to SQLite database
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    if call.data.startswith('payment'):
        service_type = call.data.split('_')[1]
        user_id = call.message.chat.id  # Get the user_id from the message

        # Check if an order already exists for the user
        cursor.execute("SELECT * FROM orders WHERE user_id = ? AND is_payed = 0", (user_id,))
        existing_order = cursor.fetchone()

        if existing_order:
            # An order already exists, display the message
            bot.send_message(call.message.chat.id, src.messages.PAY_LAST_ORDER)
        else:
            # Calculate the sum for the new order
            sum_exists = True
            new_sum = 7.05  # Default sum value

            while sum_exists:
                # Check if the calculated sum already exists in the orders table
                cursor.execute("SELECT * FROM orders WHERE sum = ?", (new_sum,))
                existing_sum_order = cursor.fetchone()

                if existing_sum_order:
                    # Increment the sum and check again
                    new_sum += 0.1
                else:
                    sum_exists = False

            current_datetime = str(datetime.datetime.utcnow().timestamp())
            current_datetime = current_datetime.split('.')[0]
            # Insert new order into the 'orders' table with user_id and unique sum
            cursor.execute('''INSERT INTO orders (date, sum, is_payed, wallet, user_id)
                              VALUES (?, ?, 0, ?, ?)''', (current_datetime, new_sum, wallet, user_id))
            conn.commit()
            bot.send_message(call.message.chat.id, src.messages.WAITING_FOR_PAYMENT.format(new_sum),
                             reply_markup=get_check_payment_keyboard())
    elif call.data == 'instructions':
        bot.send_message(call.message.chat.id, "Here are the instructions.")
    elif call.data == 'cancel':
        print('data canceled ' + str(call.message.chat.id))
        user_id = call.message.chat.id  # Get the user_id from the message

        bot.send_message(call.message.chat.id, "Order is canceled.")
        # Delete the order for the user from the 'orders' table
        cursor.execute("DELETE FROM orders WHERE user_id = ?", (str(user_id),))
        conn.commit()

    # Closing the connection
    cursor.close()
    conn.close()


# Step 11: Handling callback query for checking payment status
@bot.callback_query_handler(func=lambda call: call.data == 'check_payment')
def handle_check_payment(call):
    # Establishing connection to SQLite database
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    # Retrieve the last order from the database
    cursor.execute("SELECT is_payed FROM orders WHERE user_id = {} ORDER BY id DESC LIMIT 1".format(str(call.message.chat.id)))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result and result[0] == 1:
        bot.send_message(call.message.chat.id, "You bought it.")
        send_random_file_from_directory(call.message.chat.id)
        bot.send_message(call.message.chat.id, src.messages.CHOOSE_OPTION, reply_markup=get_welcome_keyboard())
    else:
        bot.send_message(call.message.chat.id, "You didn't buy it.")


def send_loader(message):
    loader_message = bot.send_message(message.chat.id, "⏳ Searching... 0% \n\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️")

    # Simulate processing time
    for i in range(10, 100, 10):
        loader_text = f"⏳ Searching... {i}%\n\n {'🟩' * (i // 10)}{'⬜️' * (10 - i // 10)}"
        bot.edit_message_text(loader_text, message.chat.id, loader_message.message_id)

    # Edit the loader message to indicate completion
    bot.edit_message_text("Page found in database\n\n✅ Sending material... 100%\n\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩", message.chat.id,
                          loader_message.message_id)


def get_random_date():
    return random_date()


def send_random_file_from_directory(chat_id):
    directory = "./archives"  # Path to the directory with files

    # Count the files in the directory
    file_count = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])

    if file_count == 0:
        print("No files found in the directory.")
        return

    # Generate a random number within the file count
    random_number = random.randint(1, file_count)

    # Get the file name based on the random number
    file_name = str(random_number) + '.rar'

    # Send the file using Telegram bot
    file_path = os.path.join(directory, file_name)
    try:
        with open(file_path, "rb") as file:
            bot.send_document(chat_id, file)
            print(f"Sent file: {file_name}")
    except FileNotFoundError:
        print(f"File not found: {file_name}")
    except Exception as e:
        print(f"Error sending file: {file_name}\n{str(e)}")


bot.polling(none_stop=True)
