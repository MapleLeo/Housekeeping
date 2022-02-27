from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.customer import Customer
from flask_app.models.job import Job
from flask_app.models.application import Application
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/customer')
def customer_index():
    return render_template('customer_index.html')

@app.route('/customer/register',methods=['POST'])
def customer_register():
    if not Customer.validate_register(request.form):
        return redirect('/customer')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = Customer.save(data)
    session['customer_id'] = id
    return redirect('/customer/dashboard')

@app.route('/customer/login',methods=['POST'])
def customer_login():
    customer = Customer.get_by_email(request.form)

    if not customer:
        flash("Invalid Email","login")
        return redirect('/customer')
    if not bcrypt.check_password_hash(shelter.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/customer')
    session['customer_id'] = shelter.id
    return redirect('/customer/dashboard')

@app.route('/customer/dashboard')
def customer_dashboard():
    if 'customer_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['customer_id']
    }
    job_data = {
        'customer_id': session['customer_id']
    }
    jobs = Job.get_by_customer(job_data)
    applications = Application.get_by_customer_with_job_and_housekeeper(session['customer_id'])
    return render_template('customer_dashboard.html',customer=Customer.get_by_id(data),jobs=jobs, applications=applications)


@app.route('/logout')
def customer_logout():
    session.clear()
    return redirect('/')    