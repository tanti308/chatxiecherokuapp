from flask import *
from datetime import datetime
from flask_socketio import *
from jinja2 import *
import mlab
from models.collection import *
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)


mlab.connect()

app.secret_key = 'this key is secret'

app.config['SECRET_KEY'] = '123@#@45690@#'
socketio = SocketIO(app)

UPLOAD_FOLDER = 'static\image\\upload_image'
ALLOWED_EXTENSIONS = set(['jpg','png'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    check_1 = "." in filename
    check_2 = filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS
    # if check_1 and check_2:
    #     return True
    # else:
    #     return False
    return check_1 and check_2


# Xử lý gửi tin nhắn private cho 1 user được chỉ định
# Bước 1: Xử lý đăng ký user vào Dictionary
users = {}

@socketio.on('private-message-send-username', namespace='/private-mesage')
def receive_username(username):
    users[username] = request.sid
    print(users)

# Bước 2: Xử lý gửi tin nhắn tới user được chỉ định


@socketio.on('private-message-from-client', namespace='/private-mesage')
def receive_private_message(tinnhan):
    receipient_session_id = users[tinnhan['username']]
    message = tinnhan['message']
    print(message)

    emit('private-message-from-server-receipient',
         message, room=receipient_session_id)
    emit('private-message-from-server-sender', message, room=request.sid)

# Kết thúc xử lý tin nhắn private cho user được chỉ định



@app.route('/')
def index():
    room_data = Room.objects()
    if 'loggedin' in session:
        username = session['loggedin']
        user_data = User.objects(username = username)
        for user in user_data:
            name = user['username']
            image = user['image']
            print(image)
    else:
        username = ""
        image = "profile_img.png"
    return render_template('index.html', room_data = room_data, image = image)


@app.route('/register', methods=['GET', 'POST'])  # methods la ten bat buoc
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        form = request.form
        fullname = form['fullname']
        username = form['username']
        password = form['password']
        email = form['email']
        phonenumber = form['phonenumber']
        new_user = User(fullname=fullname, username=username, password=password,
                        email=email, phonenumber=phonenumber, role=0, image="profile_img.png", status=1, message_status=1)
        session['loggedin'] = username
        # print(new_user.fullname)
        new_user.save()
        return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        form = request.form
        username = form['username']
        password = form['password']
        print(username)
        print(password)
        # dùng để check thông tin thay cho vòng for vì vòng for bị ngắt khi gặp return
        # xuất ra list chứa dictionary có key username = username
        user_data = User.objects(username=username)

        if len(user_data) == 0:  # check khi người dùng nhập sai
            flash("Khong ton tai username")
            return redirect(url_for("index"))
        else:
            for user in user_data:  # dùng vòng for lấy dữ liệu khỏi list
                if user.password == password:
                    room_data = Room.objects()
                    session['loggedin'] = username
                    user_list = User.objects()
                    for user in user_list:
                        image = user['image']
                    return render_template('index.html',user_list = user_list,room_data = room_data, image = image)
                    # return ('',204)


@app.route('/logout')
def logout():
    # return "{0}".format(session['loggedin']) # username truyen dc qua session
    del session['loggedin']
    return render_template('index.html')


@app.route('/update', methods=['GET', 'POST'])
def update():
    username = session['loggedin']
    user_data = User.objects(username=username)
    if request.method == "GET":
        for user in user_data:
            fullname = user['fullname']
            email = user['email']
            phonenumber = user['phonenumber']
            image = user['image']
        return render_template("update.html", fullname=fullname, email=email, phonenumber=phonenumber, image=image)
    elif request.method == "POST":
        form = request.form
        fullname = form['fullname']
        email = form['email']
        phonenumber = form['phonenumber']
        file = request.files['image']
        image_name = file.filename
        if file and allowed_file(image_name):
             image_name = secure_filename(image_name)
             print(image_name)
             # file.save(image_name)
             file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))

        user_data.update(set__fullname=fullname, set__email=email,
                         set__phonenumber=phonenumber, set__image=image_name)
        return redirect(url_for('update'))


@app.route('/roomcreate', methods=['GET', 'POST'])
def roomcreate():
    if request.method == "GET":
        user_data = User.objects(username = session['loggedin'])
        for user in user_data:
            image = user['image']
        return render_template("roomcreate.html",image = image)
    elif request.method == "POST":
        form = request.form
        title = form['title']
        description = form['description']
        password = form['password']
        link = form['link']
        file = request.files['image']
        image_name = file.filename
        if file and allowed_file(image_name):
             image_name = secure_filename(image_name)
             print(image_name)
             # file.save(image_name)
             file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))

        user_data = User.objects(username = session['loggedin'])
        for user in user_data:
            userid = user['id']
        new_room = Room(userid=userid, title=title,
                        description=description, password=password, viewer=0, image=image_name)
        new_room.save()
        return redirect(url_for('index'))


@app.route('/roomhost/<roomid>')
def roomhost(roomid):
    user_data = User.objects(username = session['loggedin'])
    for user in user_data:
        image = user['image']
    return render_template('roomhost.html',roomid = roomid,image= image)


@app.route('/room-detail/<roomid>')
def room_detail(roomid):
    user_data = User.objects(username = session['loggedin'])
    for user in user_data:
        image = user['image']
    return render_template('room-detail.html',roomid = roomid, image = image)


@app.route('/roomlist')
def roomlist():
    user_data = User.objects(username = session['loggedin'])
    for user in user_data:
        user_id = user['id']
        image = user['image']
    room_list = Room.objects(userid = user_id)
    return render_template('roomlist.html', room_list = room_list,image =image)

@app.route('/exception')
def exception():
    return render_template('exception.html')

@app.route('/fbi_warning')
def fbi_warning():
    return render_template('fbi-warning.html')

# Send play and pause


@socketio.on('client-send-play-pause', namespace='/player')
def play_pause(data):
    emit('server-send-play-pause', data, broadcast=True)
    print(data)

a = 0
@socketio.on('connect', namespace='/message')
def test_connect():
    global a
    a +=1
    emit('my response', {'data': 'Connected'})
    print('Connected! ', a)
    emit('server_sent_count', a, namespace = "/message", broadcast = True)

@socketio.on('disconnect', namespace = '/message')
def test_disconnect():
    global a
    a -=1
    print('Disconnected', a)
    emit('server_sent_count', a, namespace = "/message", broadcast = True)
        


@socketio.on('client-sent-message', namespace = "/message")
def client_sent_message(data):
    username = session['loggedin']
    # Luu message vao csdl
    user = User.objects(username = username).first()
    new_message = Message(
        userid = str(user.id),
        clientid = data['userid'],
        message = data['message'],
        datetime = data['date']
    )
    new_message.save()

# Lay message trong csdll
    message_send = Message.objects().with_id(new_message.id)
    data_to_send = {
        'clientid' : message_send.clientid,
        'username': username,
        'message' : message_send.message
    }

    emit('server_sent_message', data_to_send, namespace = "/message", broadcast = True)

@app.route('/player')
def player():
    return render_template('player.html')


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=3000, debug=False)
