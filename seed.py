from app import app
from models import connect_db, db, User, Feedback

db.drop_all()
db.create_all()
