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

print(Weather_info)

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


Body = f''' 
    I hope you're having a great week! Ryan finally got me a computer box, so i could start sending you emails, and man it's hard to type with these paws! There's no way im going anywhere near that mouse though, i'm nothing like those cats! 

    Anyways, Ryan said i should try and help your day go a little smoother, so i found some useful tips. He never told me what city we live in, so I'm just gonna guess every week, let me know if i'm getting close!

    I found out that today in {Weather_info[0]}, it's gonna be {Weather_info[3]} degrees, and {Weather_info[2].lower()} outside! {remark}

'''


Salutation = """   
Good luck with the rest of the week, I know you're gonna do great!


-Chico
             """



yag = yagmail.SMTP(user='mr.secretarychico@gmail.com', password=chico_password)

# sending the email
for i in range (0,len(EmailList)):
    
    Greeting = f"""Good Morning {EmailList[i][1]}!
    """
    message = Greeting + Body + Salutation
    yag.send(to=EmailList[i][0], subject=f'Chico\'s Check-In {MonthDay}', contents=message)
    print(f'Sent to {EmailList[i][1]}')