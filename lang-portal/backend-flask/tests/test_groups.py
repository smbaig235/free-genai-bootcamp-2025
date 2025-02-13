from unittest.mock import patch

def test_get_group_words_raw_success(client):
    """Test successful retrieval of raw words for a group"""
    response = client.get('/groups/1/words/raw')
    assert response.status_code == 200
    data = response.get_json()
    assert 'words' in data
    assert isinstance(data['words'], list)
    if len(data['words']) > 0:
        word = data['words'][0]
        assert 'id' in word
        assert 'french' in word
        assert 'english' in word
        assert 'correct_count' in word
        assert 'wrong_count' in word

def test_get_group_words_raw_not_found(client):
    """Test response when group is not found"""
    response = client.get('/groups/999999/words/raw')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Group not found'

def test_get_group_words_raw_error(client, mocker):
    """Test error handling when database error occurs"""
    # Mock the database cursor to raise an exception
    mocker.patch('app.db.cursor', side_effect=Exception('Database error'))
    response = client.get('/groups/1/words/raw')
    assert response.status_code == 500
    data = response.get_json()
    assert 'error' in data 