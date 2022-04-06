##################### Extra Hard Starting Project ######################

# 1. Update the birthdays.csv

# 2. Check if today matches a birthday in the birthdays.csv

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

# 4. Send the letter generated in step 3 to that person's email address.


import datetime as dt
import smtplib
from random import  choice
import pandas

curr_date = dt.datetime.now()

data = pandas.read_csv("birthdays.csv")
all_contacts_details = data.to_dict(orient="records")

today = dt.datetime(year=curr_date.year, month=curr_date.month, day=curr_date.day)

for person in all_contacts_details:
    if person["month"] == today.month and person["day"] == today.day:
        print(f"ITS YOUR BIRTHDAY {person['name']}")
    else:
        print(f"ITS NOT YOUR BIRTHDAY {person['name']}")


