from app import db

def init_db():
    with app.app_context():
        db.create_all()