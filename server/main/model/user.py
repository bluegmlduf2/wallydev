from . import *

class User(db.Model):
    """ 유저정보 취득 """
    __tablename__ = "user"

    uid = db.Column(db.String(255), primary_key=True)
    country = db.Column(db.String(2), nullable=True)
    entryDate = db.Column(db.Date, nullable=True)
    isShowMessage = db.Column(db.Boolean, default=True)
    stayStatus = db.Column(db.String(1), nullable=True)

    def __repr__(self):
        return "<User '{}'>".format(self.uid)
