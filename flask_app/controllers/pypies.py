from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import pypie
from flask_app.models import pyuser
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def show_login_reg():
    if 'user_id' in session:
        session.clear()
    return render_template("login_reg.html")
@app.route('/register/user', methods = ['POST'])
def create_user():
    print(request.form)
    users = pyuser.User.get_all()
    if not pyuser.User.validate_user(request.form, users):
        return redirect ('/') 
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "fname": request.form['first_name'],
        "lname": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    user_id = pyuser.User.save(data)
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    return redirect("/dashboard")
@app.route("/dashboard")
def show_dashboard():
    if 'user_id' not in session:
        flash("Must login or register")
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    print(session['user_id'])
    return render_template("dashboard.html", user = pyuser.User.get_user_with_pies(data))
@app.route("/login/user", methods = ["POST"])
def check_login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = pyuser.User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    # never render on a post!!!
    return redirect("/dashboard")
@app.route('/create/new/pie', methods = ['POST'])
def create_new_pie():
    print(request.form)
    if not pypie.Pie.validate_pie(request.form):
        return redirect('/dashboard')
    data = {
        "name": request.form['name'],
        "filling": request.form['filling'],
        "crust": request.form["crust"],
        "user_id": session['user_id']
    }
    pie_id = pypie.Pie.save(data)
    return redirect('/dashboard')
@app.route('/clear')
def clear_session():
    session.clear()
    return redirect('/')
@app.route('/pie/edit/<int:pie_id>')
def show_edit(pie_id):
    if 'user_id' not in session:
        flash("Must login or register")
        return redirect('/')
    data = {"id": pie_id}
    return render_template("edit_pypie.html", pie = pypie.Pie.get_one(data))
@app.route('/update/<int:pie_id>', methods=['POST'])
def update(pie_id):
    if not pypie.Pie.validate_pie(request.form):
        return redirect(f'/pie/edit/{pie_id}')
    data = {
        'id': pie_id,
        "name":request.form['name'],
        "filling": request.form['filling'],
        "crust": request.form['crust'],
    }
    pypie.Pie.update(data)
    return redirect("/dashboard")
@app.route('/delete/<int:pie_id>')
def delete(pie_id):
    data = {
        'id': pie_id
    }
    pypie.Pie.destroy(data)
    return redirect('/dashboard')
@app.route('/pies')
def show_pies():
    if 'user_id' not in session:
        flash("Must login or register")
        return redirect('/')
    print(session['user_id'])
    return render_template("pypie_derby.html", users = pyuser.User.get_all(), pies=pypie.Pie.get_all())
@app.route('/votes/<int:pie_id>')
def inc_votes(pie_id):
    data = {"id": pie_id}
    data2 = {'user_id': session['user_id'], "pie_id": pie_id}
    pypie.Pie.update_votes(data)
    pypie.Pie.add_vote_status(data2)
    return redirect ('/pies')
@app.route('/pie/<int:pie_id>')
def show_pie(pie_id):
    if 'user_id' not in session:
        flash("Must login or register")
        return redirect('/')
    data = {"pie_id": pie_id, 'user_id': session['user_id']}
    #check vote status: Have you already voted for that pie?
    if not pypie.Pie.check_vote_status(data):
        return redirect(f'/yuck/pie/{pie_id}')
    data = {"id": pie_id}
    return render_template('pypie_vote.html', pie = pypie.Pie.get_one(data), users = pyuser.User.get_all())
@app.route('/yuck/pie/<int:pie_id>')
def show_yuck_pie(pie_id):
    if 'user_id' not in session:
        flash("Must login or register")
        return redirect('/')
    print(session['user_id'])
    data = {"id": pie_id}
    return render_template("pypie_vote_yuck.html", users = pyuser.User.get_all(), pie = pypie.Pie.get_one(data))

@app.route('/yuck/<int:pie_id>')
def remove_vote(pie_id):
    data = {'id': pie_id}
    data2 = {'user_id': session['user_id'], 'pie_id': pie_id}
    pypie.Pie.dec_votes(data)
    pypie.Pie.destroy_vote_status(data2)
    return redirect("/pies")