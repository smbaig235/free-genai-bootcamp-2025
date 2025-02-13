import os
import sys
import tempfile
import pytest

# Add the parent directory to Python path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

@pytest.fixture
def app():
    # Create a temporary file to isolate the database for tests
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    # Other setup can go here
    with app.app_context():
        # Initialize the test database
        pass

    yield app

    # Cleanup - close database connection before removing file
    if hasattr(app, 'db'):
        app.db.close()
    
    # Close the file descriptor
    os.close(db_fd)
    
    # Try to remove the file, with a small delay if needed
    try:
        os.unlink(db_path)
    except PermissionError:
        import time
        time.sleep(1)  # Give Windows time to release the file
        os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()