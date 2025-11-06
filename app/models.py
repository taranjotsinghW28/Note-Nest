from app import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(20), unique=True, nullable=False)
    Email = db.Column(db.String(40), unique=True, nullable=False)
    password_hash = db.Column(db.String(1200))

    tasks = db.relationship("Note", backref="author", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


note_tag = db.Table(
    "note_tag",
    db.Column("note_id", db.Integer, db.ForeignKey("note.note_id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.tag_id"))
)

class Note(db.Model):
    note_id = db.Column(db.Integer, primary_key=True)
    note_title = db.Column(db.String(200), nullable=False)
    note_content = db.Column(db.Text, nullable=True)
    note_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    # one note → many tags
    tags = db.relationship("Tag", secondary=note_tag, backref="notes")


class Tag(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(50), nullable=False)
