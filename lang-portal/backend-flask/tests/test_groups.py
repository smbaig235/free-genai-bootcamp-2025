import pytest
from flask import g
import sqlite3

def test_get_group_words_raw_success(client, app):
    """Test successful retrieval of raw words for a group"""
    with app.app_context():
        cursor = app.db.cursor()
        # First clear any existing data
        cursor.execute('DELETE FROM word_groups')
        cursor.execute('DELETE FROM words')
        cursor.execute('DELETE FROM groups')
        
        # Now insert our test data
        cursor.execute('INSERT INTO groups (name) VALUES (?)', ('Test Group',))
        group_id = cursor.lastrowid
        
        cursor.execute('''
            INSERT INTO words (french, english, parts) 
            VALUES (?, ?, ?)
        ''', ('bonjour', 'hello', 'noun'))
        word_id = cursor.lastrowid
        
        cursor.execute('INSERT INTO word_groups (group_id, word_id) VALUES (?, ?)', 
                      (group_id, word_id))
        app.db.commit()

        # Test the endpoint
        response = client.get(f'/groups/{group_id}/words/raw')
        assert response.status_code == 200
        data = response.get_json()
        assert 'words' in data
        assert isinstance(data['words'], list)
        assert len(data['words']) == 1
        
        word = data['words'][0]
        assert word['french'] == 'bonjour'
        assert word['english'] == 'hello'
        assert 'correct_count' in word
        assert 'wrong_count' in word

def test_get_group_words_raw_not_found(client):
    """Test response when group is not found"""
    response = client.get('/groups/999999/words/raw')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Group not found'

def test_get_group_words_raw_error(client, app, mocker):
    """Test error handling when database error occurs"""
    with app.app_context():
        # Mock the cursor creation to return a cursor that raises an error
        mock_cursor = mocker.MagicMock()
        mock_cursor.execute.side_effect = Exception('Database error')
        mock_cursor.fetchone.return_value = None
        
        # Mock the database connection
        mock_db = mocker.MagicMock()
        mock_db.cursor.return_value = mock_cursor
        
        # Replace app.db with our mock
        mocker.patch.object(app, 'db', mock_db)
        
        response = client.get('/groups/1/words/raw')
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'Database error' in str(data['error']) 