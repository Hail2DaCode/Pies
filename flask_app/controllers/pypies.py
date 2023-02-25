from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import pypie
from flask_app.models import pyuser


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
    return render_template("pypie_derby.html", pies=pypie.Pie.get_all_pies_with_creator())
@app.route('/votes/<int:pie_id>', methods = ['POST'])
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
    return render_template('pypie_vote.html', pie = pypie.Pie.get_pie_with_creator(data))
@app.route('/yuck/pie/<int:pie_id>')
def show_yuck_pie(pie_id):
    if 'user_id' not in session:
        flash("Must login or register")
        return redirect('/')
    print(session['user_id'])
    data = {"id": pie_id}
    return render_template("pypie_vote_yuck.html", pie = pypie.Pie.get_pie_with_creator(data))

@app.route('/yuck/<int:pie_id>', methods=['POST'])
def remove_vote(pie_id):
    data = {'id': pie_id}
    data2 = {'user_id': session['user_id'], 'pie_id': pie_id}
    pypie.Pie.dec_votes(data)
    pypie.Pie.destroy_vote_status(data2)
    return redirect("/pies")
@app.route('/clear')
def clear_session():
    session.clear()
    return redirect('/')