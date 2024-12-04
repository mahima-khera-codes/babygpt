import os

from flask import Flask, make_response, jsonify, send_from_directory, Response

from flask.cli import with_appcontext

from flask_cors import CORS

from apscheduler.schedulers.background import BackgroundScheduler

from app import db

import click

import sys

from dotenv import load_dotenv


mongo = db.init_db()

from app.auth import token

from app.crons.campaign import campaign_mail,MailValidator
from app.crons.reject_mail import reject_mail
from app.crons.send_notification import cron_messages,recruit_cron_messages,tms_cron_messages,zapier_cron_messages
from app.crons.calculatebounces import calculate_bounce_rate
from app.crons.imap_util import bounced_mail,mail_reminder
from app.crons.campaigns_details import update_completion_time,campaign_details

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True,static_url_path='')
    app.config.from_mapping()

    CORS(app)
    UPLOAD_FOLDER = os.getcwd() + '/attached_documents/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
    dotenv_path = os.path.join(APP_ROOT, '.env')
    load_dotenv(dotenv_path)
    #This condition will run only if pytest cammand will run
    if "pytest" in sys.modules:
        app.config['ENV'] = "production"
        app.config['to'] = "testingattach0@gmail.com"
        app.config['cc'] = "cctestingrecruit@mailinator.com"
        app.config['bcc'] = "bcctestingrecruit@mailinator.com"
        app.config['origin'] = "hr"
        app.config['service'] = None
        app.config['localtextkey'] = None
        app.config['twilioSid'] = None
        app.config['twilioToken'] = None
        app.config['twilio_number'] = None

    else:
        app.config['ENV'] = os.getenv('ENVIRONMENT')
        app.config['to'] = os.getenv('to')
        app.config['cc'] = os.getenv('cc')
        app.config['bcc'] = os.getenv('bcc')
        app.config['origin'] = os.getenv('origin')
        app.config['service'] = os.getenv('service')
        app.config['localtextkey'] = os.getenv('localtextkey')
        app.config['twilioSid'] = os.getenv('twilioSid')
        app.config['twilioToken'] = os.getenv('twilioToken')
        app.config['twilio_number'] = os.getenv('twilio_number')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.errorhandler(400)
    def not_found(error):
        return make_response(jsonify(error='Not found'), 400)

    @app.route('/')
    def base():
        return "Notification system is online", 200
    
    @app.route('/images/<path:path>')
    def send_file(path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], path)

    @app.errorhandler(500)
    def error_500(error):
        return make_response({}, 500)

    
    from app.api import notify
    from app.slack.api import dispatch
    from app.slack.api import slack_channel
    from app.slack.api import slack_settings
    from app.email.api import email_preview
    from app.api import mail_settings
    from app.api import message_create
    from app.api import campaign
    from app.api import settings
    from app.api import seeds
    
    app.register_blueprint(notify.bp)
    app.register_blueprint(dispatch.bp)
    app.register_blueprint(slack_channel.bp)
    app.register_blueprint(slack_settings.bp)
    app.register_blueprint(email_preview.bp)
    app.register_blueprint(mail_settings.bp)
    app.register_blueprint(message_create.bp)
    app.register_blueprint(campaign.bp)
    app.register_blueprint(settings.bp)
    app.register_blueprint(seeds.bp)
    
    if "pytest" in sys.modules:
        return app

    schduled_messages_scheduler = BackgroundScheduler()
    schduled_messages_scheduler.add_job(cron_messages,trigger='interval',seconds=3)
    schduled_messages_scheduler.start()

    tms_schduled_messages_scheduler = BackgroundScheduler()
    tms_schduled_messages_scheduler.add_job(tms_cron_messages,trigger='interval',seconds=3)
    tms_schduled_messages_scheduler.start()

    recruit_schduled_messages_scheduler = BackgroundScheduler()
    recruit_schduled_messages_scheduler.add_job(recruit_cron_messages,trigger='interval',seconds=3)
    recruit_schduled_messages_scheduler.start()

    reject_mail_scheduler = BackgroundScheduler()
    reject_mail_scheduler.add_job(reject_mail, trigger='interval', minutes=5)
    reject_mail_scheduler.start()

    email_validator_scheduler = BackgroundScheduler()
    email_validator_scheduler.add_job(MailValidator, trigger='interval', seconds=10)
    email_validator_scheduler.start()

    campaign_mail_scheduler = BackgroundScheduler()
    campaign_mail_scheduler.add_job(campaign_mail, trigger='interval', seconds=5)
    campaign_mail_scheduler.start()

    bounced_mail_scheduler = BackgroundScheduler()
    bounced_mail_scheduler.add_job(bounced_mail, trigger='interval', minutes=5)
    bounced_mail_scheduler.start()

    calculate_bounce_rate_scheduler = BackgroundScheduler()
    calculate_bounce_rate_scheduler.add_job(calculate_bounce_rate, trigger='interval', seconds=8)
    calculate_bounce_rate_scheduler.start()

    mail_reminder_scheduler = BackgroundScheduler()
    mail_reminder_scheduler.add_job(mail_reminder, trigger='cron', day_of_week='mon-sat',hour=13,minute=7)
    mail_reminder_scheduler.start()

    update_completion_time_scheduler = BackgroundScheduler()
    update_completion_time_scheduler.add_job(update_completion_time, trigger='interval', seconds=5)
    update_completion_time_scheduler.start()

    campaign_details_update_scheduler = BackgroundScheduler()
    campaign_details_update_scheduler.add_job(campaign_details, trigger='interval', seconds=5)
    campaign_details_update_scheduler.start()

    try:
        print("create app..")
        return app
    except:
        tms_schduled_messages_scheduler.shutdown()
        schduled_messages_scheduler.shutdown()
        recruit_schduled_messages_scheduler.shutdown()
        reject_mail_scheduler.shutdown()
        email_validator_scheduler.shutdown()
        campaign_mail_scheduler.shutdown()
        bounced_mail_scheduler.shutdown()
        calculate_bounce_rate_scheduler.shutdown()
        update_completion_time_scheduler.shutdown()
        campaign_details_update_scheduler.shutdown()
        

