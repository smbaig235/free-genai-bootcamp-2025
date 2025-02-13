import os
import sys
import tempfile
import pytest

# Add the parent directory to Python path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from lib.db import init_db, get_db

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        db = get_db()
        app.db = db
        yield app
        
        # Cleanup
        db.close()
    
    os.close(db_fd)
    try:
        os.unlink(db_path)
    except PermissionError:
        pass  # Ignore permission errors on cleanup

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()