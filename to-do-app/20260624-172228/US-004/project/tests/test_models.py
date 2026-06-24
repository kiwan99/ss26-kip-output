import pytest
from datetime import datetime
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import db, Todo
from app import app

@pytest.fixture
def test_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

def test_todo_model(test_app):
    with test_app.app_context():
        item = Todo(content='Test Item')
        db.session.add(item)
        db.session.commit()
        assert item.id is not None
        assert item.done is False
        assert item.completion_time is None

        item.done = True
        db.session.commit()
        assert item.done is True
        assert item.completion_time is not None