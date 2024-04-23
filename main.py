import datetime as dt
import pandas
import smtplib
import random
import os

MY_EMAIL = "rahuldhingraajd@gmail.com"
MY_PASSWORD = "xcbjwfvrioofdazw"


def new_data():
    """takes new data from the user and returns a pandas dataframe"""
    name = input("Enter the name of the person: ")
    email = input("Enter a valid email address: ")
    dd, mm, yy = map(int, input("Enter the date of birth as DD/MM/YYYY format ").split("/"))
    person_data = {0: {'Name': name,
                       'email': email,
                       'DD': dd,
                       'MM': mm,
                       'YYYY': yy, }}
    person_data = pandas.DataFrame.from_dict(person_data, orient='index')
    return person_data


def present_day():
    """returns current day and month"""
    now = dt.datetime.now()
    current_month = now.month
    current_day = now.day
    return current_day, current_month


def get_data():
    """Gets data from the CSV file and returns list of dictionaries"""
    try:
        data = pandas.read_csv("birthday_data.csv")
    except FileNotFoundError:
        print("No Data found..\n Let's create some records now")
        updated_dataframe = new_data()
        updated_dataframe.to_csv("birthday_data.csv", mode='a', index=False, header=True)
        data = pandas.read_csv("birthday_data.csv")
    finally:
        stored_dictionary = data.to_dict('records')
        return stored_dictionary


def selecting_random_quotes(name):
    """Takes the name of the person and generates a personalised message"""
    file_for_message = random.choice(os.listdir("./letter_templates"))
    with open(f"./letter_templates/{file_for_message}") as temp_file:
        content = (temp_file.read()).replace('[NAME]', name)
    return content


def send_email(subject, message, email):
    """Takes subject, message and receiver's email and sends the email"""
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=email, msg=f"Subject:{subject} \n\n {message}")
    print("Email sent successfully!")


day, month = present_day()
list_of_people = get_data()

for elements in list_of_people:
    if elements['DD'] == day:
        receiver_name = elements['Name']
        receiver_email = elements['email']
        message_to_send = selecting_random_quotes(receiver_name)
        send_email(subject=f"Happy Birthday {receiver_name}", message=message_to_send, email=receiver_email)
