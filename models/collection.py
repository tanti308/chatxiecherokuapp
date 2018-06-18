from mongoengine import *

# design database


class User(Document):
        username = StringField()
        fullname = StringField()
        password = StringField()
        email = StringField()
        phonenumber = IntField()
        image = StringField()
        role = IntField()
        status = IntField()  # trạng thái cấm, ban,..
        message_status = IntField()


class Room(Document):
        userid = ObjectIdField()
        title = StringField()
        description = StringField()
        password = StringField()
        viewer = IntField()
        image = StringField()

class Message(Document):
        userid = StringField()
        clientid = StringField()
        message = StringField()
        datetime = StringField()

class Video(Document):
        roomid = ObjectIdField()
        upcomming = ListField()
        videoimage = StringField()
        link = StringField()
        video_type = StringField()
