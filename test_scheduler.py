import schedule
import time
import math 

seconds = time.time()

x = seconds % 3600
minutes = math.floor(seconds/60)
hours = math.floor(x/3600)

def job():
    print('this is the job function')
    print(f'The time is ' + str(hours)+ ':' + str(minutes) + ':' + str(seconds))

schedule.every(20).seconds.do(job)

schedule.every().day.at("06:40").do(job)
print('after scheduleing stuff')

while True:
    print('in the while loop')
    schedule.run_pending
    job()
    time.sleep(1)