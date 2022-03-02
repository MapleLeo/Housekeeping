from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.housekeeper import Housekeeper
from flask_app.models.job import Job
from flask_app.models.application import Application
from flask_app.models.notification import Notification
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/housekeeper')
def housekeeper_index():
    return render_template('housekeeper_index.html')

@app.route('/housekeeper/register',methods=['POST'])
def housekeeper_register():
    if not Housekeeper.validate_register(request.form):
        return redirect('/housekeeper')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = Housekeeper.save(data)
    session['housekeeper_id'] = id
    return redirect('/housekeeper/dashboard')

@app.route('/housekeeper/login',methods=['POST'])
def housekeeper_login():
    housekeeper = Housekeeper.get_by_email(request.form)

    if not housekeeper:
        flash("Invalid Email","housekeeper_login")
        return redirect('/housekeeper')
    if not bcrypt.check_password_hash(housekeeper.password, request.form['password']):
        flash("Invalid Password","housekeeper_login")
        return redirect('/housekeeper')
    session['housekeeper_id'] = housekeeper.id
    return redirect('/housekeeper/dashboard')

@app.route('/housekeeper/dashboard')
def housekeeper_dashboard():
    if 'housekeeper_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['housekeeper_id']
    }
    jobs = Job.get_all_available_with_customer()
    return render_template('housekeeper_dashboard.html',housekeeper=Housekeeper.get_by_id(data), jobs=jobs)

@app.route('/housekeeper/account')
def housekeeper_account():
    if 'housekeeper_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['housekeeper_id']
    }
    applications = Application.get_for_housekeeper_account(session['housekeeper_id'])
    housekeeper = Housekeeper.get_by_id({'id': session['housekeeper_id']})
    return render_template('housekeeper_account.html',housekeeper=Housekeeper.get_by_id(data), applications=applications)

@app.route('/housekeeper/account/application/<int:id>')
def housekeeper_account_notification(id):
    if 'housekeeper_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['housekeeper_id']
    }
    applications = Application.get_for_housekeeper_account(session['housekeeper_id'])
    housekeeper = Housekeeper.get_by_id({'id': session['housekeeper_id']})
    notifications = Notification.get_by_application({
        'application_id': id,
        'is_from_customer': 1
    })
    return render_template('housekeeper_account_notification.html',housekeeper=Housekeeper.get_by_id(data), applications=applications, notifications=notifications, application_id=id)

@app.route('/logout')
def housekeeper_logout():
    session.clear()
    return redirect('/')    

@app.route('/read_notification/<int:id>' ,methods=['POST'])
def read_notification(id):
    if 'housekeeper_id' not in session:
        return redirect('/logout')
    Application.mark_read(id)
    return redirect('/housekeeper/account')