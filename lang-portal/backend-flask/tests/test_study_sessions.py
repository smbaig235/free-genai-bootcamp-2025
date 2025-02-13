import pytest
from datetime import datetime

def test_create_study_session(client, app):
    # Test successful creation
    response = client.post('/api/study-sessions', json={
        'group_id': 1,
        'study_activity_id': 1
    })
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['group_id'] == 1
    assert data['activity_id'] == 1
    assert 'group_name' in data
    assert 'activity_name' in data
    assert 'start_time' in data
    assert 'end_time' in data
    assert data['review_items_count'] == 0
    
    # Test missing required fields
    response = client.post('/api/study-sessions', json={
        'group_id': 1
    })
    assert response.status_code == 400
    assert 'error' in response.get_json()
    assert response.get_json()['error'] == 'Missing required fields'
    
    # Test invalid group_id
    response = client.post('/api/study-sessions', json={
        'group_id': 999,
        'study_activity_id': 1
    })
    assert response.status_code == 404
    assert 'error' in response.get_json()
    assert response.get_json()['error'] == 'Group not found'
    
    # Test invalid study_activity_id
    response = client.post('/api/study-sessions', json={
        'group_id': 1,
        'study_activity_id': 999
    })
    assert response.status_code == 404
    assert 'error' in response.get_json()
    assert response.get_json()['error'] == 'Study activity not found'
    
    # Test invalid ID format
    response = client.post('/api/study-sessions', json={
        'group_id': "invalid",
        'study_activity_id': 1
    })
    assert response.status_code == 400
    assert 'error' in response.get_json()
    assert response.get_json()['error'] == 'Invalid ID format'

def test_create_review_item_success(client, app):
    # Setup test data
    with app.db.cursor() as cursor:
        # Create test group
        cursor.execute('''
            INSERT INTO groups (name) VALUES (?)
        ''', ('Test Group',))
        group_id = cursor.lastrowid
        
        # Create test word
        cursor.execute('''
            INSERT INTO words (french, english) VALUES (?, ?)
        ''', ('bonjour', 'hello'))
        word_id = cursor.lastrowid
        
        # Add word to group
        cursor.execute('''
            INSERT INTO group_words (group_id, word_id) VALUES (?, ?)
        ''', (group_id, word_id))
        
        # Create test study activity
        cursor.execute('''
            INSERT INTO study_activities (name) VALUES (?)
        ''', ('Test Activity',))
        activity_id = cursor.lastrowid
        
        # Create test study session
        cursor.execute('''
            INSERT INTO study_sessions (group_id, study_activity_id, created_at)
            VALUES (?, ?, datetime('now'))
        ''', (group_id, activity_id))
        session_id = cursor.lastrowid
        
        app.db.commit()
    
    # Test the endpoint
    response = client.post(
        f'/api/study-sessions/{session_id}/review',
        json={
            'word_id': word_id,
            'correct': True
        }
    )
    
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['word_id'] == word_id
    assert data['french'] == 'bonjour'
    assert data['english'] == 'hello'
    assert data['correct'] is True
    assert 'created_at' in data

def test_create_review_item_invalid_session(client):
    response = client.post(
        '/api/study-sessions/999999/review',
        json={
            'word_id': 1,
            'correct': True
        }
    )
    assert response.status_code == 404
    assert 'error' in response.get_json()

def test_create_review_item_invalid_word(client, app):
    # Setup test session
    with app.db.cursor() as cursor:
        cursor.execute('''
            INSERT INTO study_sessions (group_id, study_activity_id, created_at)
            VALUES (1, 1, datetime('now'))
        ''')
        session_id = cursor.lastrowid
        app.db.commit()
    
    response = client.post(
        f'/api/study-sessions/{session_id}/review',
        json={
            'word_id': 999999,
            'correct': True
        }
    )
    assert response.status_code == 404
    assert 'error' in response.get_json()

def test_create_review_item_missing_fields(client):
    response = client.post(
        '/api/study-sessions/1/review',
        json={
            'word_id': 1
            # missing 'correct' field
        }
    )
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_create_review_item_invalid_data_types(client):
    response = client.post(
        '/api/study-sessions/1/review',
        json={
            'word_id': 'not_an_integer',
            'correct': 'not_a_boolean'
        }
    )
    assert response.status_code == 400
    assert 'error' in response.get_json() 