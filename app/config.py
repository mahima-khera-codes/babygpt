import os
import sys
from dotenv import load_dotenv

APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

default_unsub = "<div style='text-align: center'><a href='{}unsubscribe_mail/{}/{}'>Unsubscribe</a></div>"
"""
#Sharing slack app with other workspace related urls
slack_redirect_url = 'https://app.slack.com/'
oauth_url = 'https://slack.com/api/oauth.v2.access'
client_id = '124720392913.1351927574339'
client_secret = '456458283bbb8cdd7e4dc8edeaa77ff5'
"""
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
if "pytest" in sys.modules:
    oauth_url = "https://slack.com/api/oauth.v2.access"
    client_id = "xyz"
    client_secret = "xyz"
    account_name = "devrecruit"
    secret_key = "gUuWrJauOiLcFSDCL5TM1heITeBVcL"
else:
    if os.getenv("oauth_url") is not None:
        oauth_url = os.getenv("oauth_url")
    else:
        raise Exception ('missing oauth_url')
    if os.getenv("client_id") is not None:
        client_id = os.getenv("client_id")
    else:
        raise Exception ('missing client_id')
    if os.getenv("client_secret") is not None:
        client_secret = os.getenv("client_secret")
    else:
        raise Exception ('missing client_secret')
#this is base url for pytest
if "pytest" in sys.modules:
    base_url = "http://127.0.0.1:5000/"
else:
    if os.getenv("base_url") is None:
        raise Exception ('missing base url')
    else:
        base_url = os.getenv("base_url")
dev_accounts = ['notify_hr_staging','devrecruit','rocketrecruit']

smtp_counts = {
    'smtp.gmail.com' : 100,
    'smtp.office365.com' : 50,
    'smtp.mail.yahoo.com': 100,
    'smtp.zoho.com': 50,
    'smtp.mail.me.com' : 1000
}

#bounced_mail_since = '1-Jan-2020'
#remind_mail_since = '1-Jan-2020'


hard_bounce_status = ["5.0.0","5.1.0","5.1.1","5.1.2","5.1.3","5.1.4","5.1.5","5.1.6","5.1.7","5.1.8","5.2.3","5.2.4","5.3.0","5.3.2","5.3.3","5.3.2","5.3.3","5.3.4","5.4.0","5.4.1","5.4.2","5.4.3","5.4.4","5.4.6","5.4.7","5.5.0","5.5.1","5.5.2","5.5.4","5.5.5","5.6.0","5.6.1","5.6.2","5.6.3","5.6.4","5.6.5","5.7.0","5.7.1","5.7.2","5.7.3","5.7.4","5.7.5","5.7.6","5.7.7"]
soft_bounce_status = ["5.2.0","5.2.1","5.2.2","5.3.1","5.4.5","5.5.3"]


default_unsubscribe_html = "<div style='text-align: center'><a href='{}unsubscribe_mail/{}/{}'>Unsubscribe</a></div>"
dates_converter = [
    "dateofjoining",
    "dob",
    "date",
    "interview_date",
    "training_completion_date",
    "termination_date",
    "next_increment_date",
    "start_increment_date",
    "fromDate",
    "toDate",
    "reporting_date"
    ]
message_needs={
    "simple_message":[
            "message_type",

            "message_key",

            ],

    "notfication_message":[

            "message_type",
            
            "user",
            
            "message_key"],
            
    "button_message":[

            "message_type",
            
            "message_key"
                ]        
            }


if os.getenv("fcm_api_key") is None:
    fcm_api_key = "AAAAFHNjgwc:APA91bFKVxkuZIoK5qA1zSHTIe9cAE45pcbwegefBMSYRYBOti8dCk0JsFVW0BmfEKwf3Y4s-RbPdMF7rjEWX9Igl99OcUjS9btZe_cWR-rsqeHug6KG7x32mWa1ElMvIogQoNH3c01r"
else:
    fcm_api_key = os.getenv("fcm_api_key")
