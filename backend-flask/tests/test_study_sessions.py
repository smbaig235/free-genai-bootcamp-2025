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