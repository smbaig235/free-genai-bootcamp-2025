# Implementation Plan: POST /study_sessions/:id/review Route

## 1. Route Setup and Request Validation
- [ ] 1.1. Add the route decorator with proper HTTP method and CORS
- [ ] 1.2. Define the function with session_id parameter
- [ ] 1.3. Set up basic error handling structure (try/except)
- [ ] 1.4. Validate request body contains required fields:
  - word_id (integer)
  - correct (boolean)
- [ ] 1.5. Convert and validate data types of incoming parameters

```python
@app.route('/api/study-sessions/<id>/review', methods=['POST'])
@cross_origin()
def create_review_item(id):
    try:
        data = request.get_json()
        if not all(key in data for key in ['word_id', 'correct']):
            return jsonify({"error": "Missing required fields"}), 400
            
        try:
            word_id = int(data['word_id'])
            correct = bool(data['correct'])
        except ValueError:
            return jsonify({"error": "Invalid data format"}), 400
```

## 2. Database Validation
- [ ] 2.1. Check if study session exists
- [ ] 2.2. Verify word exists
- [ ] 2.3. Ensure word belongs to the same group as the study session

```python
        cursor = app.db.cursor()
        
        # Verify study session exists
        cursor.execute('''
            SELECT ss.id, ss.group_id 
            FROM study_sessions ss 
            WHERE ss.id = ?
        ''', (id,))
        session = cursor.fetchone()
        if not session:
            return jsonify({"error": "Study session not found"}), 404
            
        # Verify word exists and belongs to group
        cursor.execute('''
            SELECT w.id 
            FROM words w
            JOIN group_words gw ON gw.word_id = w.id
            WHERE w.id = ? AND gw.group_id = ?
        ''', (word_id, session['group_id']))
        if not cursor.fetchone():
            return jsonify({"error": "Word not found or not in group"}), 404
```

## 3. Database Operations
- [ ] 3.1. Insert review record into word_review_items table
- [ ] 3.2. Update word statistics if needed
- [ ] 3.3. Commit transaction

```python
        # Create review item
        cursor.execute('''
            INSERT INTO word_review_items (
                study_session_id,
                word_id,
                correct,
                created_at
            ) VALUES (?, ?, ?, datetime('now'))
        ''', (id, word_id, correct))
        
        review_id = cursor.lastrowid
        app.db.commit()
```

## 4. Response Preparation
- [ ] 4.1. Fetch created review item details
- [ ] 4.2. Format response JSON
- [ ] 4.3. Return success response with created item

```python
        # Fetch created review
        cursor.execute('''
            SELECT 
                wri.id,
                wri.word_id,
                w.french,
                w.english,
                wri.correct,
                wri.created_at
            FROM word_review_items wri
            JOIN words w ON w.id = wri.word_id
            WHERE wri.id = ?
        ''', (review_id,))
        
        review = cursor.fetchone()
        
        return jsonify({
            'id': review['id'],
            'word_id': review['word_id'],
            'french': review['french'],
            'english': review['english'],
            'correct': review['correct'],
            'created_at': review['created_at']
        }), 201
```

## 5. Error Handling
- [ ] 5.1. Add specific error handling for database errors
- [ ] 5.2. Handle potential concurrent modification issues
- [ ] 5.3. Implement proper rollback on error

```python
    except Exception as e:
        current_app.logger.error(f"Error in create_review_item: {str(e)}")
        if cursor:
            cursor.execute("ROLLBACK")
        return jsonify({"error": str(e)}), 500
```

## 6. Testing

### 6.1 Unit Tests
```python
def test_create_review_item_success():
    response = client.post(
        f'/api/study-sessions/{test_session_id}/review',
        json={
            'word_id': test_word_id,
            'correct': True
        }
    )
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['word_id'] == test_word_id
    assert data['correct'] is True

def test_create_review_item_invalid_session():
    response = client.post(
        '/api/study-sessions/999999/review',
        json={
            'word_id': test_word_id,
            'correct': True
        }
    )
    assert response.status_code == 404

def test_create_review_item_invalid_word():
    response = client.post(
        f'/api/study-sessions/{test_session_id}/review',
        json={
            'word_id': 999999,
            'correct': True
        }
    )
    assert response.status_code == 404

def test_create_review_item_missing_fields():
    response = client.post(
        f'/api/study-sessions/{test_session_id}/review',
        json={
            'word_id': test_word_id
        }
    )
    assert response.status_code == 400
```

### 6.2 Manual Testing Steps
- [ ] 6.2.1. Test successful review creation with valid data
- [ ] 6.2.2. Test with invalid session ID
- [ ] 6.2.3. Test with invalid word ID
- [ ] 6.2.4. Test with word not in session's group
- [ ] 6.2.5. Test with missing required fields
- [ ] 6.2.6. Test with invalid data types
- [ ] 6.2.7. Verify review count updates in study session
- [ ] 6.2.8. Test concurrent review submissions
