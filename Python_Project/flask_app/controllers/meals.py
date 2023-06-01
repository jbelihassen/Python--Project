from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.meal import Meal
# from flask_app.models.user import User




# **** Display Feed back *****

@app.route('/meals/new')
def new_meal():
    if 'admin_id' not in session:
        return redirect('/admin')
    return render_template("add_meals.html")




@app.route('/meals/create' , methods=['post'])
def add_meal():
    if not Meal.validate_meal(request.form):
        return redirect('/admin')
    data = {
        **request.form,
        'admin_id':session['admin_id']
    }
    Meal.create_meal(data)
    return redirect('/admin')



@app.route('/meals/delete/<int:meal_id>')
def delete_m(meal_id):
     if 'admin_id' not in session:
        return redirect('/')
     Meal.delete_meal({'id':meal_id})
     return redirect('/admin')