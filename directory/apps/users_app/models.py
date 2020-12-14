from sqlalchemy import Column , Integer , String , Boolean 
from directory import app, db , login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model , UserMixin):
    __tablename__ = 'users'
    id = Column(Integer , primary_key=True)
    username = Column(String(20) , unique=True , nullable=False)
    email = Column(String(128) , unique=True , nullable=False)
    image_file = Column(String(128) , nullable=False , default='default.jpg')
    password = Column(String(128) , nullable=False)
    role = Column(Integer , nullable=False , default=0)
    active = Column(Boolean , nullable=False , unique=False , default=False)
    posts = db.relationship('Post' , backref='author' , lazy=True)

    def __repr__(self):
        return f"User '{self.username}' , '{self.email}' , {self.image_file}"

    #role 0 ==> User / role 1 ==> Admin
    def is_admin(self):
        return self.role == 1

    #FOR RESET PASS GENERATE A TOKEN
    def get_reset_token(self , expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'] , expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod #becuse in this method not use 'self' as arg so its a static method
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def get_confirm_token(self , expires_sec=14400):
        s = Serializer(app.config['SECRET_KEY'] , expires_sec)
        return s.dumps({'user_email':self.email}).decode('utf-8')
    @staticmethod
    def verify_confirm_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_email = s.loads(token)['user_email']
        except:
            return None
        return User.query.filter_by(email=user_email).first()