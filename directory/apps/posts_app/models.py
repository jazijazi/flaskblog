from datetime import datetime as dt
from sqlalchemy import Column , Integer , String , Text , DateTime , ForeignKey
from directory import db

class Post(db.Model):
    __tablename__ = 'posts'
    id = Column(Integer , primary_key=True)
    title = Column(String(128) , nullable=False , unique=True)
    date_posted = Column(DateTime , nullable=False , default=dt.utcnow)
    content = Column(Text , nullable=False , unique=False)
    user_id = Column(Integer , ForeignKey('users.id') , nullable=False)

    def __repr__(self):
        return f"Post '{self.title}' , '{self.date_posted}'"