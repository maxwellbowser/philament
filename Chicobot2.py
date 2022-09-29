import numbers
import yagmail
import keyring
import pickle
import time
from bs4 import BeautifulSoup
import requests
import random
from datetime import date



chico_password = keyring.get_password('panch', 'chico')

with open('Email_list.pickle', 'rb') as f:
    EmailList = pickle.load(f)

with open('List of cities.txt') as r:
    temp_var2 = r.read()

cities = temp_var2.split(' ')
cities.pop()
randomnum = random.randint(0,len(cities))

numbers = [0, 1]
WeeklyLink = 'https://www.tiktok.com/@ricowright83/video/7132354256476048686?is_from_webapp=1&sender_device=pc'

x = random.choices(numbers, weights = (92, 8))

if x == [1]:
    WeeklyLink = 'https://www.tiktok.com/@sock.my.this.nutz/video/7032330308221504795?is_from_webapp=1&sender_device=pc&web_id=7148631246494500394'



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

#Getting Weather
def weather(city):
    city = city.replace(" ", "+")
    res = requests.get(f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
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


todaysDate = date.today()
MonthDay = str(todaysDate)[5:]

if int(Weather_info[3]) >= 90:
    remark = 'Wow thats hot, make sure you stay cool!'
elif int(Weather_info[3]) < 90 and int(Weather_info[3]) >= 70:
    remark = 'Its gonna be perfect outside! If you ask me, thats great dog walking weather!'
elif int(Weather_info[3]) < 70 and int(Weather_info[3]) >= 40:
    remark = 'Mmmm I hope chilly weather is coming soon!'
else:
    remark = 'Man thats chilly! I hope Ryan puts some hot cocoa in my bowl!'


Greeting = f"""Good Morning {EmailList[1][1]}!
    """

Body = f''' 
    I hope you're having a great week so far! I got to bark at a cat today and Ryan took me for a walk, so I've got no complaints with my life.

    I'm still learning how to use this internet, and it's so cool, did you know that people take funny videos of dogs?? <a href={WeeklyLink}>Check out this one!</a> 

    Still figuring out where I live but I'm pretty sure we're in the USA. Today in {Weather_info[0]}, it's gonna be {Weather_info[3]} degrees, and {Weather_info[2].lower()} outside! {remark}
'''


Salutation = """   
Sending lots of love, I hope you're feeling it!

-Chico :)


p.s. Hey guys, this is Ryan. I asked Chico if I could start putting pictures of him in his emails and he was alright with it so here ya go, enjoy!
             """

message = Greeting + Body + Salutation

yag = yagmail.SMTP(user='mr.secretarychico@gmail.com', password=chico_password)
yag.send(to=EmailList[1][0], subject=f'Chico\'s Check-In {MonthDay}', contents=message, attachments='Chico-picture.jpeg')


# sending the email
'''
for i in range (0,len(EmailList)):
    
    Greeting = f"""Good Morning {EmailList[i][1]}!
    """
    message = Greeting + Body + Salutation
    yag.send(to=EmailList[i][0], subject=f'Chico\'s Check-In {MonthDay}', contents=message, attachments='Chico-picture.jpeg')
    print(f'Sent to {EmailList[i][1]}')

'''