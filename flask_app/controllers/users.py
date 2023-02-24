from flask_app import app
from flask import render_template,redirect,request,session, flash
from flask_app.models.user import User

@app.route('/')
def index():
    # all_users = User.get_all()
    # print(all_users)
    return render_template('index.html', all_users = User.get_all())

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/new_user', methods = ['POST'])
def new_user():
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email']
    }
    if not User.validate_user(request.form):
        return redirect('/create')
    User.save(data)
    return redirect('/')

@app.route('/show_user/<int:user_id>')
def show_user(user_id):
    return render_template('user.html', user = User.get_one({'id':user_id}))

@app.route('/edit/<int:user_id>')
def edit(user_id):
    return render_template('edit.html', user = User.get_one({'id':user_id}))

@app.route('/edit_user/<int:user_id>', methods = ['POST'])
def edit_user(user_id):
    data = {
        'id': user_id,
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email']
    }
    User.update(data)
    return redirect('/')

@app.route('/delete/<int:user_id>')
def delete(user_id):
    User.delete({'id': user_id})
    return redirect('/')