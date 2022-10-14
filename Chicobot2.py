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
    I hope you have an amazing weekend, there's so much fun stuff in the world, go enjoy it! ʕ•ᴥ•ʔﾉ♡

    -Chico & Ryan :)  

    p.s.
    Hi Alyssa, I had an amazing week with you, thank you for being such a great girlfriend

    Hugs & Kisses,
    Ryan
    """
    message = Greeting + Body + Salutation
    yag.send(to=EmailList[i][0], subject=f'Chico\'s Check-In {MonthDay}',
             contents=message, attachments=Weekly_picture)
    print(f'Sent to {EmailList[i][1]}')


todaysDate = date.today()
MonthDay = str(todaysDate)[5:]


# I'm putting all the things that will change email to email up here for easy access
Weekly_picture = 'Ella_pic 10-13.jpeg'
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
elif int(Weather_info[3]) < 90 and int(Weather_info[3]) >= 70:
    remark = 'If you ask me, that\'s great dog walking weather!'
elif int(Weather_info[3]) < 70 and int(Weather_info[3]) >= 40:
    remark = 'Man I hope chilly weather is coming soon!'
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
                 'Good luck with the rest of the week, I know you\'re gonna do great!', 'I hope you have an amazing day, there\'s so much fun stuff in the world, go enjoy it!']


Body = f''' 

    Happy Friday🎉🎉! I hope your week has been going well, I'm excited for the weekend!

    Ryan's been using the computer to do dumb homework all week, so i haven't been able to write you an email! Thankfully, I had plenty of time to cruise instagram and MAN do I have some cute news.
    
    Since 2014, the National Park Service (NPS) has been holding a competition known as Fat Bear Week. In the months before winter, brown bears all around Alaska start fattening up to prepare for hibernation. The NPS chooses of the fattest bears, and people vote on their favorites, march madness style!

    This years winner was bear #747, who was given the nickname '<a href=https://www.instagram.com/p/CjmDqqbjTqG/>Bear Force One</a>'. This big boy weighs over 1,400 pounds and is just so SO chonky. I'm already excited for next years competition, and if you wanna learn more about this, <a href=https://explore.org/fat-bear-week>click here!</a>
    
    For today's weather, in {Weather_info[0]}, it's gonna be {Weather_info[3]} degrees and {Weather_info[2].lower()} outside! {remark}
    
    I've also attached a cute picture of my big sister Ella! Sometimes she hogs her toys or tries to eat my treats, but she's still a good girl.
    '''


Salutation = """   
I hope you have an amazing weekend, there's so much fun stuff in the world, go enjoy it!

-Chico :)



p.s.
Just as a little explanation for this email, incase someone signed you up. These will be cute weekly / twice-a-week emails from my dog Chico! If you would like to be removed from this list, just send an email back saying cancel or please stop. Otherwise, I hope you enjoy these emails as much as I do!

Thanks,
-Ryan
"""


everyone = False

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
