from VDP import db


class User(db.Model):   # flask-sglalchemy z class spravi tabulku s tymto menom
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    words = db.relationship('Word', backref='user', lazy=True)


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unknown = db.Column(db.String(100), unique=True, nullable=False)
    known = db.Column(db.String(100), unique=True, nullable=False)
    level = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return self.unknown, self.known
