# Implementation Plan: GET /groups/:id/words/raw

## 1. Route Setup
- [ ] 1.1. Add the new route decorator using the existing pattern
- [ ] 1.2. Add cross-origin decorator to match other endpoints
- [ ] 1.3. Define the function `get_group_words_raw(id)`

## 2. Database Query Implementation
- [ ] 2.1. Set up error handling with try-except block
- [ ] 2.2. Create database cursor
- [ ] 2.3. Verify group exists (return 404 if not found)
- [ ] 2.4. Write SQL query to fetch all words for the group
  - Should join `words`, `word_groups`, and `word_reviews` tables
  - No pagination needed (raw endpoint)
  - Include word ID, French word, English word, and review counts

## 3. Response Formatting
- [ ] 3.1. Create response dictionary structure
- [ ] 3.2. Format each word entry
- [ ] 3.3. Return JSON response

## 4. Error Handling
- [ ] 4.1. Add specific error messages for common failures
- [ ] 4.2. Ensure 500 error returns for unexpected exceptions
- [ ] 4.3. Add proper error response format matching other endpoints

## Implementation Example

```python
@app.route('/groups/<int:id>/words/raw', methods=['GET'])
@cross_origin()
def get_group_words_raw(id):
    try:
        cursor = app.db.cursor()
        
        # Check if group exists
        cursor.execute('SELECT name FROM groups WHERE id = ?', (id,))
        group = cursor.fetchone()
        if not group:
            return jsonify({"error": "Group not found"}), 404

        # Fetch all words for the group
        cursor.execute('''
            SELECT 
                w.id,
                w.french,
                w.english,
                COALESCE(wr.correct_count, 0) as correct_count,
                COALESCE(wr.wrong_count, 0) as wrong_count
            FROM words w
            JOIN word_groups wg ON w.id = wg.word_id
            LEFT JOIN word_reviews wr ON w.id = wr.word_id
            WHERE wg.group_id = ?
            ORDER BY w.french ASC
        ''', (id,))
        
        words = cursor.fetchall()
        
        # Format response
        words_data = [{
            "id": word["id"],
            "french": word["french"],
            "english": word["english"],
            "correct_count": word["correct_count"],
            "wrong_count": word["wrong_count"]
        } for word in words]

        return jsonify({
            'words': words_data
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

## 5. Testing
- [ ] 5.1. Write test cases using pytest
- [ ] 5.2. Test successful response
- [ ] 5.3. Test group not found scenario
- [ ] 5.4. Test error handling

### Test Implementation Example

```python
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
```

## 6. Documentation
- [ ] 6.1. Add route documentation with request/response examples
- [ ] 6.2. Document any specific error cases
- [ ] 6.3. Add API documentation to the project's docs

## 7. Final Verification
- [ ] 7.1. Test endpoint with Postman or similar tool
- [ ] 7.2. Verify response format matches other endpoints
- [ ] 7.3. Check error handling works as expected
- [ ] 7.4. Verify all tests pass
