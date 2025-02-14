
## Backend API Implementation for French Language Learning Portal

### AI Coding Assistant: Cursor (Free)
### LLM Model: Claude 3.5 Sonnet

### Core Technologies:

- Flask (Python) as the backend framework
- SQLite3 as the database
- Flask-CORS for handling Cross-Origin Resource Sharing

### 3 API Endpoints Implemented:

1. An enpoint to create a new study sessions (POST /api/study-sessions)
2. An enpoint to submit reviews for a study sessions (POST /study_sessions/:id/review)
3. An endpoint to get a raw word data for a group (GET /groups/:id/words/raw)

#### Step 1:

1. We have created few simple rules for Flask and SQlite3 to follow during implementation for generated code through AI coding assistant.

#### Step 2:

1. Next,we created plans for the missing API endpoints to implement the step by step guide which helps during implementation and testing.

#### Step 3:
 
### API Endpoint Implementations:  

## 1. Study Sessions Endpoint: (POST /study_sessions Route)

These are the implementation steps for the POST /study_sessions route:

* Route Setup
* Request Validation
* Database Operations
* Response Preparation
* Error Handling
* Testing 

#### Route Setup

 In this step we added the route decorator and function definition

```python
@app.route('/api/study-sessions', methods=['POST'])
@cross_origin()
def create_study_session():
```

#### Request Validation

      * Parse JSON request body

      * Validate required fields

      * Add type validation for IDs

#### Database Operations

     * Verify group exists

     * Verify study activity exists

     * Insert new study session

     * Get the created session ID

#### Response Preparation

     * Fetch created session details

     * Format and return response

```python
cursor.execute('''
    SELECT 
        ss.id,
        ss.group_id,
        g.name as group_name,
        sa.id as activity_id,
        sa.name as activity_name,
        ss.created_at
    FROM study_sessions ss
    JOIN groups g ON g.id = ss.group_id
    JOIN study_activities sa ON sa.id = ss.study_activity_id
    WHERE ss.id = ?
''', (session_id,))
```

#### Format and return response

```python
session = cursor.fetchone()
return jsonify({
    'id': session['id'],
    'group_id': session['group_id'],
    'group_name': session['group_name'],
    'activity_id': session['activity_id'],
    'activity_name': session['activity_name'],
    'start_time': session['created_at'],
    'end_time': session['created_at'],
    'review_items_count': 0
}), 201
```

#### Error Handling

     * Add try-catch block

     * Add database commit

#### Testing Code

#### Unit Tests

```python
def test_create_study_session(client):
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
    
    # Test missing required fields
    response = client.post('/api/study-sessions', json={
        'group_id': 1
    })
    assert response.status_code == 400
    
    # Test invalid group_id
    response = client.post('/api/study-sessions', json={
        'group_id': 999,
        'study_activity_id': 1
    })
    assert response.status_code == 404
    
    # Test invalid study_activity_id
    response = client.post('/api/study-sessions', json={
        'group_id': 1,
        'study_activity_id': 999
    })
    assert response.status_code == 404
    
    # Test invalid ID format
    response = client.post('/api/study-sessions', json={
        'group_id': "invalid",
        'study_activity_id': 1
    })
    assert response.status_code == 400
```
This test file implements these test cases 

- Missing required fields error
- Invalid group ID error
- Invalid study activity ID error
- Invalid ID format error
- Each test verifies both the status code and the error message in the response.

After creating test file,run this test file using pytest:

```bash
pytest tests/test_study_sessions.py -v
```

Next step,initialize the databse:

```bash
python init_db.py
```

and then check the database contents:

```bash
python check_db.py 
```

finally, we make sure the flask is installed

```bash
pip install flask flask-cors
```

then start the flask server:

```bash
python -m flask run
```

Now,we are ready to run the curl commands

### Bash/Unix Test Commands 

#### Create new study session

'''
   curl -X POST http://localhost:5000/api/study-sessions \
     -H "Content-Type: application/json" \
     -d '{"group_id": 1, "study_activity_id": 1}'
'''

  ![New study Session.](images/New-Study-Sessions.png=50x50)

#### Test missing fields
'''
   curl -X POST http://localhost:5000/api/study-sessions \
      -H "Content-Type: application/json" \
      -d '{"group_id": 1}'
'''
   ![Test Missing Field.](images/Test-Missingfields.png=50x50)

#### Test invalid group

'''
   curl -X POST http://localhost:5000/api/study-sessions \
     -H "Content-Type: application/json" \
     -d '{"group_id": 999, "study_activity_id": 1}'
'''

  ![Test Invalid group.](images/Test-Invalid-group.png=50x50)


## 2. Submit reviews for a study sessions (POST /study_sessions/:id/review Route)


 These are the implementation steps for POST /study_sessions/:id/review Route

* Route Setup and Request Validation
* Database Validation
* Database Operations
* Response Preparation
* Error Handling
* Testing 


#### Route Setup and Request Validation

  - Add the route decorator with proper HTTP method and CORS
  - Define the function with session_id parameter
  - Set up basic error handling structure (try/except)
  - Validate request body contains required fields:
     - word_id (integer)
     - correct (boolean)
1.5. Convert and validate data types of incoming parameters

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

#### Database Validation

-  Check if study session exists
-  Verify word exists
-  Ensure word belongs to the same group as the study session

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

#### Database Operations

-  Insert review record into word_review_items table
-  Update word statistics if needed
-  Commit transaction

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

#### Response Preparation

-  Fetch created review item details
-  Format response JSON
-  Return success response with created item

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

#### Error Handling

-  Add specific error handling for database errors
-  Handle potential concurrent modification issues
-  Implement proper rollback on error

```python
    except Exception as e:
        current_app.logger.error(f"Error in create_review_item: {str(e)}")
        if cursor:
            cursor.execute("ROLLBACK")
        return jsonify({"error": str(e)}), 500
```

#### Testing

##### Unit Tests

- Test successful review creation
- Test invalid session ID case
- Test invalid word ID case
- Test missing fields case
- Test invalid data types case

#### Manual Testing Steps

1. Test successful review creation with valid data:
   - Create a study session
   - Add a word to the session's group
   - Submit a review with correct=true
   - Verify the response contains all expected fields
   - Verify the data is stored in the database

2. Test with invalid session ID:
   - Try to submit a review to a non-existent session ID
   - Verify you get a 404 error

3. Test with invalid word ID:
   - Try to submit a review with a non-existent word ID
   - Verify you get a 404 error

4. Test with word not in session's group:
   - Create a word that's not in the session's group
   - Try to submit a review for that word
   - Verify you get a 404 error

5. Test with missing required fields:
   - Submit without word_id
   - Submit without correct field
   - Verify you get a 400 error in both cases

6. Test with invalid data types:
   - Submit with string for word_id
   - Submit with string for correct
   - Verify you get a 400 error

7. Verify review count updates:
   - Create multiple reviews
   - Check study session details
   - Verify review_items_count increases correctly

8. Test concurrent submissions:
   - Open multiple browser tabs
   - Submit reviews simultaneously
   - Verify all reviews are recorded correctly
   - Check for any race conditions

## 3. Get a raw word data for a group (GET /groups/:id/words/raw Route)

These are the implementation steps for GET /groups/:id/words/raw Route

  * Route Setup
  * Database Query Implementation
  * Response Formatting
  * Error Handling
  * Testing
  * Documentation
  
#### Route Setup

-  Add the new route decorator using the existing pattern
-  Add cross-origin decorator to match other endpoints
-  Define the function `get_group_words_raw(id)`

#### Database Query Implementation

- Set up error handling with try-except block
- Create database cursor
- Verify group exists (return 404 if not found)
- Write SQL query to fetch all words for the group
  - Should join `words`, `word_groups`, and `word_reviews` tables
  - No pagination needed (raw endpoint)
  - Include word ID, French word, English word, and review counts

#### Response Formatting

-  Create response dictionary structure
-  Format each word entry
-  Return JSON response

#### Error Handling

- Add specific error messages for common failures
- Ensure 500 error returns for unexpected exceptions
- Add proper error response format matching other endpoints

#### Implementation

 In this implementation we are performing these tasks:

     * Sets up error handling with try-except block
     * Creates a database cursor
     * Verifies the group exists (returns 404 if not found)
     * Writes and executes the SQL query to fetch all words for the group
     * Joins the necessary tables (words, word_groups, word_reviews)
     * Includes all required fields (ID, French, English, review counts)
     * Orders by French word alphabetically
     * Formats and returns the response

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

#### Testing

- Write test cases using pytest
- Test successful response
- Test group not found scenario
- Test error handling

#### Test Implementation

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

 ![Test groups.](images/group-test.png=50x50)

#### Documentation

-  Add route documentation with request/response examples
-  Document any specific error cases
-  Add API documentation to the project's docs
path: backend-flask/docs/api-documentation.md


