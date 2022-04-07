##################### Extra Hard Starting Project ######################

# 1. Update the birthdays.csv

# 2. Check if today matches a birthday in the birthdays.csv

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

# 4. Send the letter generated in step 3 to that person's email address.
import datetime as dt
import smtplib
from random import randint
import pandas
import os

# CONSTANTS
PLACEHOLDER = '[NAME]'
MY_EMAIL = "patryktester5@yahoo.com"
MY_PASSWORD = "jgxjyyvchnanomwv"
HOST = "smtp.mail.yahoo.com"

number_of_letters = len(os.listdir('letter_templates'))

ORDINAL_NUMBERS_EXCEPTIONS = [11, 12, 13]
ORDINAL_NUMBERS_DICT = {
    "ST": [1],
    "ND": [2],
    "RD": [3],
    "TH": [0, 4, 5, 6, 7, 8, 9]
}

# get today's date
curr_date = dt.datetime.now()
today_tuple = (curr_date.month, curr_date.day)

# get birthdays using pandas into dict
data = pandas.read_csv("birthdays.csv")
birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}

# check if key in birthdays_dict = today's date as tuple
if today_tuple in birthdays_dict:
    # get values based on the key
    birthday_person = birthdays_dict[today_tuple]

    # get their age
    years_old = curr_date.year - birthday_person["year"]

    # set ordinal number default for exceptions (age 11,12 or 13)
    ordinal_number = "TH"

    # if the persons age isn't an exception (age 11,12 or 13)
    if years_old > 99 and years_old - 100 in ORDINAL_NUMBERS_EXCEPTIONS:
        pass
    elif years_old not in ORDINAL_NUMBERS_EXCEPTIONS:
        # get the last digit of their age
        last_digit = years_old % 10
        for key, value in ORDINAL_NUMBERS_DICT.items():
            if last_digit in value:
                ordinal_number = key

    # create subject line to be sent in the email
    subject = f"Subject: HAPPY {years_old}{ordinal_number} BIRTHDAY\n\n"

    try:
        # try to open random letter in the letter_templates
        with open(f"letter_templates/letter_{randint(1, number_of_letters)}.txt") as random_letter:
            letter = random_letter.read()
    except (FileNotFoundError, ValueError):
        # if file isn't found (doesn't exist) create a new one
        with open("letter_templates/letter_1.txt", mode="w") as create_letter:
            letter_content = "Dear [NAME],\n\nHappy Birthday!\n\nPatryk"
            create_letter.write(letter_content)
        with open("letter_templates/letter_1.txt") as get_letter:
            letter = get_letter.read()
    finally:
        # then replace the placeholder with person's name
        ready_letter = letter.replace(PLACEHOLDER, birthday_person["name"])

    # establish an SMTP connection and send the email
    with smtplib.SMTP(host=HOST) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=f"{birthday_person['email']}",
            msg=subject + ready_letter
        )
