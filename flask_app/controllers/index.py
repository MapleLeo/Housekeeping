from flask import render_template
from flask_app import app


@app.route('/')
def index():
    return render_template('index.html')

# debug
from flask_app.models.housekeeper import Housekeeper
from flask_app.models.job import Job
from flask_app.models.application import Application
from flask_app.models.notification import Notification
import json

@app.route('/debug')
def debug():

    # print(Application.get_for_housekeeper_account(1)[0].notification_count);
    tmp = Application.get_by_customer_with_job_and_housekeeper(1)
    print(tmp[0].resume)
    # Notification.save({
    #     'message': 'message1',
    #     'is_from_customer': 0,
    #     'application_id': 1,
    # })
    print(json.dumps(Notification.get_raw_by_application({'application_id': 1, 'is_from_customer': 0})))
    return json.dumps(Notification.get_raw_by_application({'application_id': 1, 'is_from_customer': 0}))