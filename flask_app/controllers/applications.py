from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.application import Application
from flask_app.models.notification import Notification

@app.route('/application/<int:id>/approve', methods=['POST'])
def approve_application(id):
    if 'customer_id' not in session:
        return redirect('/logout')
    Application.set_status(id, "APPROVED")
    return redirect('/customer/dashboard')

@app.route('/application/<int:id>/reject', methods=['POST'])
def reject_application(id):
    if 'customer_id' not in session:
        return redirect('/logout')
    Application.set_status(id, "REJECTED")
    return redirect('/customer/dashboard')

@app.route('/application/<int:id>/customer_reply', methods=['POST'])
def application_customer_reply(id):
    if 'customer_id' not in session:
        return redirect('/logout')
    Notification.save({
        'application_id': id,
        'message': request.form['message'],
        'is_from_customer': 1,
    })
    return redirect('/customer/dashboard/application/' + str(id))

@app.route('/application/<int:id>/housekeeper_reply', methods=['POST'])
def application_housekeeper_reply(id):
    if 'housekeeper_id' not in session:
        return redirect('/logout')
    Notification.save({
        'application_id': id,
        'message': request.form['message'],
        'is_from_customer': 0,
    })
    return redirect('/housekeeper/account/application/' + str(id))