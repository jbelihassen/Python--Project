from flask import render_template,request,redirect,session,flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.feed_back import Feed_back
from flask_app.models.meal import Meal
from flask_app.models.room import Room
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('acceil.html')




@app.route('/log/user')
def log():
    return render_template('login_user.html')


@app.route('/services')
def ser():
    return render_template('our_services.html')




@app.route('/prices')
def pri():
    meals =Meal.get_meals()
    rooms =Room.get_rooms()
    return render_template('our-prices.html',  meals=meals , rooms=rooms)


@app.route('/user/profil')
def us_profil():
    if 'user_id' not in session:#if he has not an id redirect to the register page
        return redirect('/acceil')
    users= User.get_by_id_user({'id':session['user_id']})


    return render_template('dashboard_user.html',user=users)



# @app.route('/reservation')
# def res():
#     return render_template('reservation.html')





@app.route('/feedback')
def dashboard():
    if 'user_id' not in session:#if he has not an id redirect to the register page
        return redirect('/')
    log_user=User.get_by_id_user({'id':session['user_id']})
    all_feedback = Feed_back.get_feed_backs()

    return render_template('feed_back.html',log= log_user, all_feedback = all_feedback)


@app.route('/users/login',methods=['POST'])
def login_user():
    user_db = User.get_by_email_user(request.form)
    if not user_db:
        flash('Invalid email or password',"login_user")
        return redirect('/log/user')
    if not user_db.is_valid:
        flash('you are not active wait it will take few days',"login_user")
        return redirect('/log/user')
    if not bcrypt.check_password_hash(user_db.password, request.form['password']):
        flash('Invalid email or password',"login_user")
        return redirect('/log/user')
    session['user_id']=user_db.id
    return redirect('/')




    
