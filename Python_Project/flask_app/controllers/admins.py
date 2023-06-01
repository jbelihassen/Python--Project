from flask import render_template,request,redirect,session,flash
from flask_app import app
from flask_app.models.admin import Admin
from flask_app.models.user import User
from flask_app.models.feed_back import Feed_back
from flask_app.models.room import Room
from flask_app.models.meal import Meal
from flask_app.models.reservation import Reservation


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/admin')
def dash():
    users  = User.get_users()
    rooms  = Room.get_rooms()
    meals  = Meal.get_meals()
    all_reservations = Reservation.get_all_reservations()
    
    return render_template('admin.html', users = users, rooms=rooms ,meals=meals, all_reservations=all_reservations )



@app.route('/login/min')
def logg():
    return render_template('login_admin.html')






@app.route('/admins/login',methods=['POST'])
def login_admin():
    admin_db = Admin.get_email_admin(request.form)
    if not admin_db:
        flash('Invalid email or password',"login_admin")
        return redirect('/login/min')
    if not admin_db.password == request.form['password']:
        flash('Invalid email or password',"login_admin")
        return redirect('/login/min')
    session['admin_id']=admin_db.id
    return redirect('/admin')




@app.route('/users/edit/<int:user_id>')
def edit(user_id):
   
    users = User.get_by_id_user({'id':user_id})
    return render_template('edit_user.html',user=users)




@app.route('/users/update',methods=['POST'])
def update1():
    if not User.validate_user2(request.form):
        return redirect(f"/users/edit/{request.form['id']}")
    
    User.update_user(request.form)
    return redirect('/admin')






@app.route('/users/delete/<int:user_id>')
def delete1(user_id):
    if 'admin_id' not in session:
        return redirect('/admin')
    User.delete_user({'id':user_id})
    return redirect('/admin')



@app.route('/users/registration')
def new_user():
    if 'admin_id' not in session:
        return redirect('/admin')
    return render_template('registration.html')


@app.route('/users/create',methods=['POST'])
def add_user():
    if not User.validate_user(request.form):
        return redirect('/users/registration')
    data={
        **request.form,
        'password':bcrypt.generate_password_hash(request.form['password'])
    }
     
    User.create_user(data)
    return redirect('/admin')

@app.route('/users/confirm/<int:user_id>')
def confirm_user(user_id):
    User.confirm_user(user_id)
    return redirect('/admin')



    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')