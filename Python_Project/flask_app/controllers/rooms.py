from flask import render_template,request,redirect,session,flash
from flask_app import app
from flask_app.models.room import Room
from flask_app.models.admin import Admin
from flask_app.models.user import User


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/rooms')
def rom():
   
    rooms=Room.get_rooms()
    # liked= Room.all_user_likes({'user_id': session['user_id']})
    
    return render_template('page1.html', rooms=rooms)

@app.route('/rooms/add')
def roo():
    return render_template('form_room.html')

@app.route('/rooms/edit/<int:room_id>')
def edit_r(room_id):
    if 'admin_id' not in session:
        return redirect('/')
    room = Room.get_room({'id':room_id})
    return render_template('edit_room.html', room=room)


@app.route('/rooms/update',methods=['POST'])
def update_ro():
    if not Room.validate_room(request.form):
        return redirect(f"/rooms/edit/<int:room_id>")
    
    Room.update_room(request.form)
    return redirect('/admin')






@app.route('/rooms/delete/<int:room_id>')
def delete_rom(room_id):
    if 'admin_id' not in session:#to secure
        return redirect('/')
    Room.delete_room({'id':room_id})
    return redirect('/admin')


@app.route('/rooms/create',methods=['POST'])
def add_room():
    print(request.form)
    print(request.files['images'].filename)
    if not Room.validate_room(request.form):
        return redirect('/rooms/add')
    data= {
        **request.form,
        'images':request.files['images'].filename
    }
    Room.create_room(data)
    return redirect('/rooms')

@app.route('/likes/<int:room_id>/<int:user_id>', methods=['POST'])
def likes(room_id, user_id):
    data={
        'user_id': user_id,
        'room_id': room_id
    }
    room =Room.one_like(data)
    if (room == False):
        Room.likes_rooms(data)
    else:
        print("---- remove the like from the room ----")
        Room.unlikes_room(data)

    return redirect('/rooms')








