from flask import render_template,request,redirect,session,flash
from flask_app import app
from flask_app.models.reservation import  Reservation 
from flask_app.models.user import User
from flask_app.models.room import Room
from flask_app.models.meal import Meal
from flask_app.models.reservation import Reservation
from datetime import datetime

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/reservation/confirm/<int:reservation_id>')
def confirm_reservation(reservation_id):
    Reservation.confirm_reservation(reservation_id)
    return redirect('/admin')

@app.route('/reservation')
def reservation():
    all_rooms = Room.get_rooms()
    all_meals=Meal.get_meals()
   
    return render_template('reservation.html', all_rooms=all_rooms, all_meals=all_meals )


@app.route('/reservation/create' , methods=['post'])
def add_reservation():
    if not 'user_id' in session:
        if  User.validate_user2(request.form):
            user_data = {
                **request.form, 
                'password':bcrypt.generate_password_hash(request.form['phone_number'])
            }
            user_id = User.create_user(user_data)
            data = {** request.form,
                    'user_id':user_id}
    else:
        data = {
            **request.form,'user_id':session['user_id']
        }
    confirmed_reservation = Reservation.get_confirmed_reservation({'room_id':request.form['room_id']})
    # if confirmed_reservation:
    if confirmed_reservation:
        for reservation in confirmed_reservation:
            if datetime.strptime(request.form['check_in'],"%Y-%m-%d").date() >= reservation.check_in and datetime.strptime(request.form['check_in'],"%Y-%m-%d").date()  <= reservation.check_out:
                # print( "="*20,"Room already reserved In", "="*20,datetime.strptime(request.form['check_in'],"%Y-%m-%d").date() , reservation.check_in,reservation.check_out )
                flash("room not available already booked!!","reservation")
                all_rooms = Room.get_rooms()
                all_meals=Meal.get_meals()
                return render_template('reservation.html', all_rooms=all_rooms, all_meals=all_meals )
            if datetime.strptime(request.form['check_out'],"%Y-%m-%d").date()  >= reservation.check_in and datetime.strptime(request.form['check_out'],"%Y-%m-%d").date()  <= reservation.check_out:
                # print( "*"*20,"Room already reserved Out", "*"*20)
                flash("room not available already booked!!","reservation")
                all_rooms = Room.get_rooms()
                all_meals=Meal.get_meals()
                return render_template('reservation.html', all_rooms=all_rooms, all_meals=all_meals )
    if Reservation.validate_reservation(data):
        Reservation.create_reservation(data)
        return redirect('/rooms')
    return render_template("reservation.html")
# @app.route('/reservation/create' , methods=['post'])
# def add_reservation():
#     confirmed_reservation = Reservation.get_confirmed_reservation({'room_id':request.form['room_id']})
#     for reservation in confirmed_reservation:
#         print("="*25,datetime.strptime(request.form['check_in'],"%Y-%m-%d"),reservation.check_in,"="*25)
#     return redirect("/reservation")








