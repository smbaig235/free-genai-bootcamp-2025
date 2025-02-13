# API Documentation

## Groups Endpoints

### GET /groups/:id/words/raw

Returns all words in a group without pagination.

#### Request
- Method: GET
- URL Parameters:
  - `id`: Group ID (integer, required)
- Headers:
  - None required

#### Response
**Success (200 OK)**
```json
{
  "words": [
    {
      "id": 1,
      "french": "bonjour",
      "english": "hello",
      "correct_count": 5,
      "wrong_count": 2
    },
    {
      "id": 2,
      "french": "au revoir",
      "english": "goodbye",
      "correct_count": 3,
      "wrong_count": 1
    }
  ]
}
```

**Error Responses**
- 404 Not Found
```json
{
  "error": "Group not found"
}
```

- 500 Internal Server Error
```json
{
  "error": "Database error"
}
```

#### Notes
- Returns all words in the group ordered alphabetically by French word
- Review counts default to 0 if no reviews exist
- No pagination is applied to this endpoint 