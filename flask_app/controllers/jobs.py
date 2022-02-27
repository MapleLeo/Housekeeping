from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.job import Job
from flask_app.models.housekeeper import Housekeeper
from flask_app.models.customer import Customer
from flask_app.models.application import Application
import os
@app.route('/new/job')
def new_job():
    if'customer_id' not in session:
        return redirect('/logout')

    data = {
        'id':session['customer_id']
    }
    
    return render_template('new_job.html', customer=Customer.get_by_id(data))

@app.route('/create/job', methods=['POST'])
def add_job():
    if 'customer_id' not in session:
        return redirect('/logout')
    if not Job.validate_job(request.form):
        return redirect('/customer/dashboard')
    data = {
        'title': request.form['title'],
        'date': request.form['date'],
        'time': request.form['time'],
        'pay': request.form['pay'],
        'description': request.form['description'],
        'customer_id': session['customer_id']
    }
    id=Job.save(data)
    return redirect('/customer/dashboard')

@app.route('/apply/job/<int:id>', methods=['POST'])
def apply_job(id):
    if 'housekeeper_id' not in session:
        return redirect('/logout')
    if 'resume' not in request.files:
        flash("Please attach resume.", "application")
        return redirect('job/'+id)
    file = request.files['resume']
    file.save(os.path.join("flask_app/Static/", file.filename))
    data = {
        'job_id': id,
        'housekeeper_id': session['housekeeper_id'],
        'status': 'PENDING',
        'resume': file.filename,
    }
    Application.save(data)
    return redirect('/housekeeper/dashboard')

@app.route('/destroy/job/<int:id>')
def destroy_job(id):
    if 'customer_id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    Job.destroy(data)
    return redirect('/customer_dashboard')

@app.route('/job/<int:id>')
def show_job(id):
    if 'housekeeper_id' not in session:
        return redirect('/logout')
    return render_template('show_job.html',housekeeper=Housekeeper.get_by_id({'id': session['housekeeper_id']}), job=Job.get_one({'id': id}))
