

import random  # define the random module
import string
from models import *
import os
from flask_sqlalchemy import SQLAlchemy
# from flask_restful import Resource, Api
import matplotlib.pyplot as plt
from flask import flash
from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from datetime import datetime as dt
import matplotlib
matplotlib.use('Agg')
# from pathlib import joinpath
# matplotlib.use('Agg')


@app.route('/')
def index():
    data = User.query.all()

    return render_template('Signin.html')


@app.route('/')
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        fname = request.form['f_name']
        email = request.form['email']
        password = request.form['pswd']

        members = User.query.filter_by(email_id=email).first()
        if members is None:
            user_details = User(
                username=fname, email_id=email, password=password)
            db.session.add(user_details)
            db.session.commit()

            mem = User.query.filter_by(
                email_id=email).first()
            u_id = mem.user_id

            flash("User is Successfully Sign Up , Now You can Sign In ")
            return render_template("Signin.html", user=u_id)
            flash("User is Successfully Sign Up , Now You can Sign In ")

        else:
            flash("user is already Present , Pls log in !")
            return redirect("/signin")

    else:
        return render_template("signup.html")


@app.route('/')
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['pswd']

        members = User.query.filter_by(
            email_id=email).first()

        if members:
            if (members.password == password):
                u_id = members.user_id
                flash(
                    "Succesfully Sign In !")
                return redirect(f"/{u_id}/dashboard")
            else:
                flash(
                    "Email and Password are not Matched, The password that you've entered is incorrect!")
                return redirect("/signin")
        else:
            flash("user is not registered , Pls Sign Up!")
            return redirect("/signup")

    else:
        return render_template("Signin.html")


@app.route("/<int:user_idd>/dashboard", methods=["GET", "POST"])
def dashboard(user_idd):
    user_details = User.query.filter(User.user_id == user_idd).first()
    # print(user_details)

    if request.method == 'GET':
        for_list_id = List.query.filter_by(user_id=user_idd).first()

        list_details = List.query.filter_by(user_id=user_idd).all()

        card_details = Card.query.filter_by(
            user_id=user_idd).all()

        return render_template('dashboard.html', tasks=list_details, user=user_details.username,  user_id=user_idd, cd=card_details)
    elif request.method == 'POST':
        list_name = request.form['task']
        desc = request.form['description']

        add_list = List(title=list_name, desc=desc,
                        user_id=user_idd)

        # list_details.append(add_list)
        # print(list_details)
        db.session.add(add_list)
        db.session.commit()
        return redirect(f"/{user_idd}/dashboard")


@app.route("/<int:user_idd>/summary", methods=["GET", "POST"])
def summary(user_idd):
    user = User.query.filter_by(user_id=user_idd).first()
    list_details = List.query.filter_by(user_id=user_idd).all()

    l_name = []
    l_id = []
    for i in list_details:
        l_id.append(i.list_id)
        l_name.append(i.title)
    st = []
    date_comp = []
    for j in l_id:
        status = []
        date = []
        card_details = Card.query.filter_by(list_id=j).all()
        for k in card_details:
            date.append(k.deadline)
            status.append(k.completed)

        st.append(status)
        date_comp.append(date)
    # print(date_comp) today.strftime("%b-%d-%Y")
    all = []
    d = dt.today()
    # da = d.strftime("%m-%d-%Y")

# [['2022-09-13', '2022-08-29'], ['2022-09-13', '2022-09-30', '2022-09-21'],
#  ['2022-09-13', '2022-09-13'], ['2022-09-12']]

# from datetime import datetime as dt
# a = dt.strptime("9/2/22", "%m/%d/%y")
# print(a)
# b = dt.strptime("10/15/13", "%m/%d/%y")
# d = dt.today()
# print(d)
# print(a > b) #12 oct 2023 > 15 oct 2013
# print(a < b) #12 oct 2023 < 15 oct 2013
# print(a <= d) #12 oct 2023 < 3 sept 2022

    for i in range(len(st)):
        mom = []
        T = 0
        F = 0
        d_passed = 0
        d_left = 0
        for elem in date_comp[i]:
            if dt.strptime(elem, "%Y-%m-%d") > d:
                d_left += 1
            else:
                d_passed += 1

        for elem in st[i]:
            if elem == 'Incomplete':
                F += 1
            else:
                T += 1
        mom.append(T)
        mom.append(F)
        # mom.append(d_left)
        mom.append(d_passed)
        all.append(mom)
    # print(all)
    images = []
    for i in range(len(all)):
        x = ["Complete", "Incomplete", "Deadline_passed"]
        y = all[i]
        plt.clf()
        plt.bar(x, y, color=['#641E16', 'blue', 'red'], width=0.3)

        plt.ylabel("Number of Task")
        plt.title("Summary of Task")

        plt.savefig(f'static/image/plot_{i}.png')

        images.append(f'/static/image/plot_{i}.png')

    print(images)
    # image_list = []
    # username = 'cars2'
    # basepath = "static/images"

    # dir = os.walk(basepath)
    # print(dir)
    # file_list = []

    # for path, subdirs, files in dir:
    #     for file in files:
    #         temp = os.path.join('/' + path + '/', file)
    #         file_list.append(temp)
    # print(file_list)
    return render_template('summary.html', data=all, user=user, images=images, list=l_name)


@app.route("/<int:user_idd>/<int:list_idd>/delete")
def deletelist(user_idd, list_idd):

    list = List.query.filter(List.list_id == list_idd).first()
    print(list)

    return render_template("list_confirmation.html", user_id=user_idd, list_id=list_idd, ld=list)

    # print(list)
    # print(list.list_id)
    # db.session.delete(list)
    # db.session.commit()
    # return redirect(f'/{user_idd}/dashboard')


@app.route("/<int:user_idd>/<int:list_idd>/delete/confirm")
def list_confirm(user_idd, list_idd):
    list = List.query.filter_by(list_id=list_idd).first()
    all_cards_have_same_lists = Card.query.filter_by(list_id=list_idd).all()
    print(all_cards_have_same_lists)
    for card in all_cards_have_same_lists:
        db.session.delete(card)
    db.session.delete(list)
    db.session.commit()
    return redirect(f'/{user_idd}/dashboard')


@app.route('/<int:user_idd>/<int:list_idd>/edit', methods=["GET", "POST"])
def editlist(user_idd, list_idd):
    if request.method == 'GET':
        userdata = User.query.filter(User.user_id == user_idd).first()
        # print(userdata)
        listdata = List.query.filter(List.list_id == list_idd).first()
        # print(listdata)

        return render_template('updateList.html', ud=userdata, ld=listdata)
    else:
        # listdata = List.query.filter(List.list_id == list_idd).first()
        new_title = request.form['task']
        new_desc = request.form['description']
        s = List.query.filter_by(list_id=list_idd).update(dict(
            title=new_title, desc=new_desc))
        db.session.commit()
        return redirect(f"/{user_idd}/dashboard")


@app.route("/<int:user_idd>/<int:list_idd>/addcard", methods=["GET", "POST"])
def addcard(user_idd, list_idd):
    if request.method == 'GET':
        # currtime = dt.now()
        # curr_time = currtime.strftime('%Y-%m-%d')
        user_details = User.query.filter_by(user_id=user_idd).first()
        # print(user_details)
        list_details = List.query.filter_by(list_id=list_idd).first()
        # print(list_details)
        card_details = Card.query.filter_by(
            list_id=list_idd, user_id=user_idd).first()
        # print(card_details)

        return render_template('addcards.html', ud=user_details, ld=list_details, user_id=user_idd, list_id=list_idd, cd=card_details)
    else:
        cname = request.form['cname']
        date = request.form['date']
        cdesc = request.form['cdesc']
        status = request.form.getlist('process')
        # print(date)

        # year = date[:4]
        # month = date[5: 7]
        # date1 = date[8: 10]

        # curr_time = datetime(int(year), int(month), int(
        #     date1))

        for st in status:

            if st == '1':
                cid = 'Incomplete'
            elif st == '2':
                cid = 'Complete'

        add_card = Card(card_title=cname, deadline=date, card_desc=cdesc,
                        completed=cid, user_id=user_idd, list_id=list_idd)
        print(add_card)
        db.session.add(add_card)
        db.session.commit()

        return redirect(f"/{user_idd}/dashboard")


@app.route("/<int:user_idd>/<int:list_idd>/<int:card_idd>/delete")
def deletecard(user_idd, list_idd, card_idd):
    card = Card.query.filter_by(card_id=card_idd).first()
    return render_template('card_confirmation.html', user_id=user_idd, list_id=list_idd, card_id=card_idd, cd=card)
    # return redirect(f"/{user_idd}/{list_idd}/{card_idd}/confirm")


@app.route("/<int:user_idd>/<int:list_idd>/<int:card_idd>/delete/confirm")
def confirm(user_idd, list_idd, card_idd):
    card = Card.query.filter_by(card_id=card_idd).first()

    db.session.delete(card)
    db.session.commit()
    return redirect(f'/{user_idd}/dashboard')


@app.route("/<int:user_idd>/<int:list_idd>/<int:card_idd>/edit", methods=["GET", "POST"])
def editcard(user_idd, list_idd, card_idd):
    if request.method == 'GET':
        userdata = User.query.filter(User.user_id == user_idd).first()
        # # print(userdata)
        listdata = List.query.filter_by(
            user_id=user_idd).all()
        # print(listdata)
        print(len(listdata))
        carddata = List.query.filter(Card.card_id == card_idd).first()
        print(carddata)
        card_details = Card.query.filter(Card.card_id == card_idd).first()
        print(card_details)

        return render_template('updatecards.html', crd=card_details, cd=carddata, ud=userdata, ld=listdata, user_id=user_idd, list_id=list_idd, card_id=card_idd)
    else:

        # listdata = List.query.filter(List.list_id == list_idd).first()

        # cname = request.form['cname']
        # date = request.form['date']
        # cdesc = request.form['cdesc']
        # status = request.form.getlist('process')

        new_list_name = request.form.getlist('lname')[0]
        new_card_title = request.form['cname']
        new_date = request.form['date']
        new_card_desc = request.form['cdesc']
        new_status = request.form.getlist('process')

        for st in new_status:

            if st == '1':
                cid = 'Incomplete'
            elif st == '2':
                cid = 'Complete'

        new_card = Card.query.filter_by(card_id=card_idd).update(dict(
            card_title=new_card_title, card_desc=new_card_desc,
            deadline=new_date, completed=cid, list_id=new_list_name))
        db.session.commit()
        return redirect(f"/{user_idd}/dashboard")


@app.route('/signout')
def signout():
    return redirect("/")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
