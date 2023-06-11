#import required python packages
import dotenv
import os
from datetime import datetime, date, timedelta
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#load dotenv variables
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

#current date
now = datetime.now()

#check if the notifier is allowed to run
def allowed_to_run():
    if 'SEND_MAIL' in os.environ and os.environ['SEND_MAIL'].lower() == 'true' and int(os.environ['ALLOWED_DAYS_START']) <= now.day <= int(os.environ['ALLOWED_DAYS_END']) and int(os.environ['ALLOWED_HOURS_START']) <= now.hour <= int(os.environ['ALLOWED_HOURS_END']):
        return True
    return False

#retrieve the date of the Monday that falls within the first week of a new month
def get_new_month_monday():
    first_day_of_next_month = date(now.year, now.month, 1) + timedelta(days=32)
    first_day_of_next_month = date(first_day_of_next_month.year, first_day_of_next_month.month, 1)
    weekday = first_day_of_next_month.weekday()
    days_to_next_monday = (7 - weekday + 0) % 7
    next_month_first_monday = first_day_of_next_month + timedelta(days=days_to_next_monday)
    return next_month_first_monday

def check_for_new_schedule(next_month_first_monday):
    url = f"https://www.eversports.nl/api/eventsession/calendar?facilityId={os.environ['EVERSPORTS_FACILITY_ID']}&startDate={next_month_first_monday}&activeEventType=training"
    
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        if (json_data['status'] == 'success'):
            data_length = len(json_data['data']['html'])
            if (data_length >= 5000):
                return True
            else:
                return False
    else:
        return False
    
#reset the SEND_MAIL variable at the first day of the month
if (now.day == 1):
    os.environ['SEND_MAIL'] = 'true'
    dotenv.set_key(dotenv_file, 'SEND_MAIL', os.environ['SEND_MAIL'])

#function that sends the email notification
def send_notification():
    
    msg = MIMEMultipart()
    msg['FROM'] = os.environ['EMAIL_SENDER']
    msg['To'] = os.environ['EMAIL_RECEIVER']
    msg['Subject'] = os.environ['EMAIL_SUBJECT']

    msg.attach(MIMEText(os.environ['EMAIL_MESSAGE'], 'plain'))

    try:
        server = smtplib.SMTP(os.environ['SMTP_SERVER'], os.environ['SMTP_PORT'])
        server.starttls()

        server.login(os.environ['SMTP_USERNAME'], os.environ['SMTP_PASSWORD'])
        server.sendmail(os.environ['EMAIL_SENDER'], os.environ['EMAIL_RECEIVER'], msg.as_string())

        server.quit()

        os.environ['SEND_MAIL'] = 'false'
        dotenv.set_key(dotenv_file, 'SEND_MAIL', os.environ['SEND_MAIL'])
        print('Notification sent successfully!')
    except Exception as error:
        print('An error occured while sending the notification:', str(error))

#main function that executes the other functions
print(f'{now} - The script has been executed')
if allowed_to_run():
    next_month_first_monday = get_new_month_monday()
    if check_for_new_schedule(next_month_first_monday):
        send_notification()