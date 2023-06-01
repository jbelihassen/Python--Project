from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.feed_back import Feed_back
# from flask_app.models.user import User




# **** Display Feed back *****

@app.route('/feed_backs/new')
def new_feed_backs():
    
    all_feedbacks = Feed_back.get_feed_backs()
    return render_template("feed_back.html" , all_feedbacks = all_feedbacks)




@app.route('/feed_backs/create' , methods=['post'])
def add_feed_backs():
    if not Feed_back.validate_feed_back(request.form):
        return redirect('/feed_backs/new')
    data = {
        **request.form,
        'user_id':session['user_id']
    }
    Feed_back.create_feed_back(data)
    return redirect('/feed_backs/new')





@app.route('/feed_backs/delete/<int:feed_back_id>')
def delete_feed(feed_back_id):
     if 'user_id' not in session:
        return redirect('/')
     Feed_back.delete_feed_back({'id':feed_back_id})
     return redirect('/feed_backs/new')