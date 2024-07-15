from flask_app import app
from flask import render_template , request , redirect , session

from flask_app.models.Job import Job
from flask_app.models.User import User

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    
    user_data = {'id': session['user_id']}
    logged_user = User.get_by_id(user_data)
    all_jobs = Job.get_all()
    user_jobs = Job.get_user_jobs(user_data)

    
    return render_template("dashboard.html", jobs=all_jobs, user_jobs=user_jobs, logged_user=logged_user)


@app.route('/addJob')
def add_job_page():
    logged_user = User.get_by_id({'id': session['user_id']})
    return render_template("add_job.html" , logged_user  = logged_user)

@app.route('/job/create', methods=['POST'])
def add_job():
    data = request.form
    if Job.validate_form(data):
        Job.create(data)
        return redirect('/dashboard')
    return redirect('/addJob')


@app.route('/jobs/cancel/<int:id>')
def cancel_job(id):
    data = {'id': id}
    Job.delete(data)
    return redirect('/dashboard')


@app.route('/edit/<int:id>')
def edit_job_page(id):
    data = {'id': id}
    job = Job.get_by_id(data)
    return render_template("edit_job.html" , job = job)

@app.route("/job/update" , methods=['POST'])
def update_job():
    data = request.form
    Job.update(data)
    return redirect('/dashboard')


@app.route('/view/<int:id>')
def job_view_page(id):
    job = Job.get_by_id({'id': id})
    return render_template("view_job.html" , job = job)

@app.route('/jobs/add_to_my_jobs/<int:job_id>')
def add_to_my_jobs(job_id):
    user_id = session['user_id']
    data = {'users_id': user_id, 'jobs_id': job_id}
    Job.add_to_user_jobs(data)
    return redirect('/dashboard')
    

@app.route('/jobs/done/<int:job_id>')
def mark_job_done(job_id):
    user_id = session['user_id']
    data = {'users_id': user_id, 'jobs_id': job_id}
    Job.remove_from_user_jobs(data)
    return redirect('/dashboard')