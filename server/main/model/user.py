from . import *

class User(db.Model):
    """ 유저정보 취득 """
    __tablename__ = "user"

    uid = db.Column(db.String(255), primary_key=True)

    def __repr__(self):
        return "<User '{}'>".format(self.uid)
