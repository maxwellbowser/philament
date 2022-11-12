from calendar import week
import numbers
import yagmail
import keyring
import pickle
import time
from bs4 import BeautifulSoup
import requests
import random
from datetime import date


def cute_messages_for_alyssa(i):
    Greeting = f"""{timed_greeting} {EmailList[i][1]} <3!
            """

    Salutation = """   
    I'm glad I get to spend so much time with you. I love you so much! <3

    -Chico & Ryan :)  
    """
    message = Greeting + Body + Salutation
    yag.send(to=EmailList[i][0], subject=f'Chico\'s Check-In {MonthDay}',
             contents=message, attachments=Weekly_picture)
    print(f'Sent to {EmailList[i][1]}')


todaysDate = date.today()
MonthDay = str(todaysDate)[5:]


# I'm putting all the things that will change email to email up here for easy access
Weekly_picture = 'Chico 10-31-2022.jpeg'
WeeklyLink = 'https://www.tiktok.com/@ripkenthebatdog/video/7127058382502120747?is_from_webapp=1&sender_device=pc&web_id=7148631246494500394'

# I like to call this the Rick-Roll Randomizer
numbers = [0, 1]
x = random.choices(numbers, weights=(92, 8))
if x == [1]:
    WeeklyLink = 'https://www.tiktok.com/@sock.my.this.nutz/video/7032330308221504795?is_from_webapp=1&sender_device=pc&web_id=7148631246494500394'


# Loading the email list and list of cities
with open('Email_list.pickle', 'rb') as f:
    EmailList = pickle.load(f)
with open('List of cities.txt') as r:
    temp_var2 = r.read()

# Getting Weather and also formatting the list of random cities
cities = temp_var2.split(' ')
cities.pop()
randomnum = random.randint(0, len(cities))
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


def weather(city):
    city = city.replace(" ", "+")
    res = requests.get(
        f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
    # print("Searching...\n")
    soup = BeautifulSoup(res.text, 'html.parser')
    location = soup.select('#wob_loc')[0].getText().strip()
    time = soup.select('#wob_dts')[0].getText().strip()
    info = soup.select('#wob_dc')[0].getText().strip()
    weather = soup.select('#wob_tm')[0].getText().strip()
    return location, time, info, weather


city = cities[randomnum]
city = city+" weather"
Weather_info = weather(city)


# Determining remark based on the temperature returned from the weather function
if int(Weather_info[3]) >= 90:
    remark = 'Wow thats hot, make sure you stay cool!'
elif int(Weather_info[3]) < 90 and int(Weather_info[3]) >= 65:
    remark = 'If you ask me, that\'s great dog walking weather!'
elif int(Weather_info[3]) < 65 and int(Weather_info[3]) >= 35:
    remark = 'That sounds like great christmas weather to me!'
else:
    remark = 'Man thats chilly! I hope Ryan puts some hot cocoa in my bowl!'

# Generating the email greeting based on the time of day!
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
if int(current_time[:2]) <= 12:
    timed_greeting = 'Good Morning'
elif int(current_time[:2]) > 12 and int(current_time[:2]) < 17:
    timed_greeting = 'Good Afternoon'
elif int(current_time[:2]) >= 17:
    timed_greeting = 'Good Evening'

# Eventually add a way to randomize endings!
random_ending = ['Hope your day is as wonderful as you are!', 'Sending lots of love, I hope you\'re feeling it!', 'You got this!',
                 'Good luck with the rest of the week, I know you\'re gonna do great!', 'I hope you have an amazing day, there\'s so much fun stuff in the world, go enjoy it!',
                 '']


Body = f''' 

Long time no see, Happy Halloween! I hope your week has been going well, hopefully you're not too spooked out!

This is going to be a shorter email, since Ryan is taking me to hand out candy to the kids in the neighborhood. I'm super excited, I love seeing all the kids in their costumes, and I think I get to eat all the chocolate they don't want!

For today's weather, in {Weather_info[0]}, it's gonna be {Weather_info[3]} degrees and {Weather_info[2].lower()} outside! {remark}
        '''


Salutation = f"""   
Happy trick or treating!
-Chico :)


p.s.
Just as a little explanation for this email, incase someone signed you up. These will be cute weekly emails from my dog Chico! If you would like to be removed from this list, just send an email back saying cancel or please stop. Otherwise, I hope you enjoy these emails as much as I do!

Thanks,
-Ryan
"""


everyone = True

chico_password = keyring.get_password('panch', 'chico')
yag = yagmail.SMTP(user='mr.secretarychico@gmail.com', password=chico_password)

# sending the email to everyone
if everyone == True:
    for i in range(0, len(EmailList)):

        if i == 2:
            cute_messages_for_alyssa(i)

        else:
            Greeting = f"""{timed_greeting} {EmailList[i][1]}!
            """
            message = Greeting + Body + Salutation
            yag.send(
                to=EmailList[i][0], subject=f'Chico\'s Check-In {MonthDay}', contents=message, attachments=Weekly_picture)
            print(f'Sent to {EmailList[i][1]}')


# just to me (testing)
else:
    Greeting = f'{timed_greeting} {EmailList[1][1]}!'

    message = Greeting + Body + Salutation
    yag.send(to=EmailList[1][0], subject=f'Chico\'s Check-In {MonthDay}',
             contents=message, attachments=Weekly_picture)
    print(f'Sent to {EmailList[1][1]}')
