# Implementation Plan: POST /study_sessions Route

## 1. Route Setup
- [x] 1.1. Add the route decorator and function definition
```python
@app.route('/api/study-sessions', methods=['POST'])
@cross_origin()
def create_study_session():
```

## 2. Request Validation
- [x] 2.1. Parse JSON request body
- [x] 2.2. Validate required fields
- [x] 2.3. Add type validation for IDs

## 3. Database Operations
- [x] 3.1. Verify group exists
- [x] 3.2. Verify study activity exists
- [x] 3.3. Insert new study session
- [x] 3.4. Get the created session ID

## 4. Response Preparation
- [x] 4.1. Fetch created session details
- [x] 4.2. Format and return response
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

- [ ] 4.2. Format and return response
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

## 5. Error Handling
- [x] 5.1. Add try-catch block
- [x] 5.2. Add database commit

## Testing Code

### Unit Tests
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

### PowerShell Test Commands
```powershell
# Create new study session
$body = @{
    group_id = 1
    study_activity_id = 1
} | ConvertTo-Json

Invoke-RestMethod -Method POST -Uri "http://localhost:5000/api/study-sessions" `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body

# Test missing fields
Invoke-RestMethod -Method POST -Uri "http://localhost:5000/api/study-sessions" `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"group_id": 1}'

# Test invalid group
Invoke-RestMethod -Method POST -Uri "http://localhost:5000/api/study-sessions" `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"group_id": 999, "study_activity_id": 1}'
```

### Bash/Unix Test Commands (keep these for non-Windows users)
```bash
# Create new study session
curl -X POST http://localhost:5000/api/study-sessions \
  -H "Content-Type: application/json" \
  -d '{"group_id": 1, "study_activity_id": 1}'

# Test missing fields
curl -X POST http://localhost:5000/api/study-sessions \
  -H "Content-Type: application/json" \
  -d '{"group_id": 1}'

# Test invalid group
curl -X POST http://localhost:5000/api/study-sessions \
  -H "Content-Type: application/json" \
  -d '{"group_id": 999, "study_activity_id": 1}'
```
