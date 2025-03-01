from flask import request, jsonify, g, current_app
from flask_cors import cross_origin
from datetime import datetime
import math
import sqlite3

def load(app):
  @app.route('/api/study-sessions', methods=['POST'])
  @cross_origin()
  def create_study_session():
    cursor = None
    try:
      # Parse request body
      data = request.get_json()
      current_app.logger.info(f"Received request data: {data}")
      
      # Validate required fields
      if not all(key in data for key in ['group_id', 'study_activity_id']):
          current_app.logger.error("Missing required fields")
          return jsonify({"error": "Missing required fields"}), 400
          
      # Validate ID types
      try:
          group_id = int(data['group_id'])
          study_activity_id = int(data['study_activity_id'])
      except ValueError:
          current_app.logger.error("Invalid ID format")
          return jsonify({"error": "Invalid ID format"}), 400
      
      cursor = app.db.cursor()
      
      # Debug: Check if group exists
      cursor.execute('SELECT id, name FROM groups WHERE id = ?', (group_id,))
      group = cursor.fetchone()
      current_app.logger.info(f"Found group: {group}")
      if not group:
          current_app.logger.error(f"Group not found with ID: {group_id}")
          return jsonify({"error": "Group not found"}), 404
      
      # Verify study activity exists
      cursor.execute('SELECT id FROM study_activities WHERE id = ?', (study_activity_id,))
      if not cursor.fetchone():
          return jsonify({"error": "Study activity not found"}), 404
          
      # Insert new study session
      cursor.execute('''
          INSERT INTO study_sessions (group_id, study_activity_id, created_at)
          VALUES (?, ?, datetime('now'))
      ''', (group_id, study_activity_id))
      
      # Get the created session ID
      session_id = cursor.lastrowid
      
      # Fetch created session details
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
      
      session = cursor.fetchone()
      
      # Commit the transaction
      app.db.commit()
      
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
      
    except Exception as e:
      current_app.logger.error(f"Error in create_study_session: {str(e)}")
      if cursor:
          cursor.execute("ROLLBACK")
      return jsonify({"error": str(e)}), 500

  @app.route('/api/study-sessions', methods=['GET'])
  @cross_origin()
  def get_study_sessions():
    try:
      cursor = app.db.cursor()
      
      # Get pagination parameters
      page = request.args.get('page', 1, type=int)
      per_page = request.args.get('per_page', 10, type=int)
      offset = (page - 1) * per_page

      # Get total count
      cursor.execute('''
        SELECT COUNT(*) as count 
        FROM study_sessions ss
        JOIN groups g ON g.id = ss.group_id
        JOIN study_activities sa ON sa.id = ss.study_activity_id
      ''')
      total_count = cursor.fetchone()['count']

      # Get paginated sessions
      cursor.execute('''
        SELECT 
          ss.id,
          ss.group_id,
          g.name as group_name,
          sa.id as activity_id,
          sa.name as activity_name,
          ss.created_at,
          COUNT(wri.id) as review_items_count
        FROM study_sessions ss
        JOIN groups g ON g.id = ss.group_id
        JOIN study_activities sa ON sa.id = ss.study_activity_id
        LEFT JOIN word_review_items wri ON wri.study_session_id = ss.id
        GROUP BY ss.id
        ORDER BY ss.created_at DESC
        LIMIT ? OFFSET ?
      ''', (per_page, offset))
      sessions = cursor.fetchall()

      return jsonify({
        'items': [{
          'id': session['id'],
          'group_id': session['group_id'],
          'group_name': session['group_name'],
          'activity_id': session['activity_id'],
          'activity_name': session['activity_name'],
          'start_time': session['created_at'],
          'end_time': session['created_at'],  # For now, just use the same time since we don't track end time
          'review_items_count': session['review_items_count']
        } for session in sessions],
        'total': total_count,
        'page': page,
        'per_page': per_page,
        'total_pages': math.ceil(total_count / per_page)
      })
    except Exception as e:
      return jsonify({"error": str(e)}), 500

  @app.route('/api/study-sessions/<id>', methods=['GET'])
  @cross_origin()
  def get_study_session(id):
    try:
      cursor = app.db.cursor()
      
      # Get session details
      cursor.execute('''
        SELECT 
          ss.id,
          ss.group_id,
          g.name as group_name,
          sa.id as activity_id,
          sa.name as activity_name,
          ss.created_at,
          COUNT(wri.id) as review_items_count
        FROM study_sessions ss
        JOIN groups g ON g.id = ss.group_id
        JOIN study_activities sa ON sa.id = ss.study_activity_id
        LEFT JOIN word_review_items wri ON wri.study_session_id = ss.id
        WHERE ss.id = ?
        GROUP BY ss.id
      ''', (id,))
      
      session = cursor.fetchone()
      if not session:
        return jsonify({"error": "Study session not found"}), 404

      # Get pagination parameters
      page = request.args.get('page', 1, type=int)
      per_page = request.args.get('per_page', 10, type=int)
      offset = (page - 1) * per_page

      # Get the words reviewed in this session with their review status
      cursor.execute('''
        SELECT 
          w.*,
          COALESCE(SUM(CASE WHEN wri.correct = 1 THEN 1 ELSE 0 END), 0) as session_correct_count,
          COALESCE(SUM(CASE WHEN wri.correct = 0 THEN 1 ELSE 0 END), 0) as session_wrong_count
        FROM words w
        JOIN word_review_items wri ON wri.word_id = w.id
        WHERE wri.study_session_id = ?
        GROUP BY w.id
        ORDER BY w.french
        LIMIT ? OFFSET ?
      ''', (id, per_page, offset))
      
      words = cursor.fetchall()

      # Get total count of words
      cursor.execute('''
        SELECT COUNT(DISTINCT w.id) as count
        FROM words w
        JOIN word_review_items wri ON wri.word_id = w.id
        WHERE wri.study_session_id = ?
      ''', (id,))
      
      total_count = cursor.fetchone()['count']

      return jsonify({
        'session': {
          'id': session['id'],
          'group_id': session['group_id'],
          'group_name': session['group_name'],
          'activity_id': session['activity_id'],
          'activity_name': session['activity_name'],
          'start_time': session['created_at'],
          'end_time': session['created_at'],  # For now, just use the same time
          'review_items_count': session['review_items_count']
        },
        'words': [{
          'id': word['id'],
          'french': word['french'],
          'english': word['english'],
          'correct_count': word['session_correct_count'],
          'wrong_count': word['session_wrong_count']
        } for word in words],
        'total': total_count,
        'page': page,
        'per_page': per_page,
        'total_pages': math.ceil(total_count / per_page)
      })
    except Exception as e:
      return jsonify({"error": str(e)}), 500

  @app.route('/api/study-sessions/<id>/review', methods=['POST'])
  @cross_origin()
  def create_review_item(id):
    cursor = None
    try:
      # Parse and validate request body
      data = request.get_json()
      if not all(key in data for key in ['word_id', 'correct']):
        return jsonify({"error": "Missing required fields"}), 400
        
      # Validate and convert data types
      try:
        word_id = int(data['word_id'])
        correct = bool(data['correct'])
      except ValueError:
        return jsonify({"error": "Invalid data format"}), 400

      cursor = app.db.cursor()
      
      # Verify study session exists and get group_id
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
      
      # Commit the transaction
      app.db.commit()

      # Fetch created review details
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
      
    except ValueError as e:
      current_app.logger.error(f"Validation error in create_review_item: {str(e)}")
      return jsonify({"error": "Invalid input format"}), 400
      
    except sqlite3.IntegrityError as e:
      current_app.logger.error(f"Database integrity error in create_review_item: {str(e)}")
      if cursor:
        cursor.execute("ROLLBACK")
      return jsonify({"error": "Database constraint violation"}), 409
      
    except sqlite3.Error as e:
      current_app.logger.error(f"Database error in create_review_item: {str(e)}")
      if cursor:
        cursor.execute("ROLLBACK")
      return jsonify({"error": "Database error occurred"}), 500
      
    except Exception as e:
      current_app.logger.error(f"Unexpected error in create_review_item: {str(e)}")
      if cursor:
        cursor.execute("ROLLBACK")
      return jsonify({"error": "An unexpected error occurred"}), 500

  @app.route('/api/study-sessions/reset', methods=['POST'])
  @cross_origin()
  def reset_study_sessions():
    try:
      cursor = app.db.cursor()
      
      # First delete all word review items since they have foreign key constraints
      cursor.execute('DELETE FROM word_review_items')
      
      # Then delete all study sessions
      cursor.execute('DELETE FROM study_sessions')
      
      app.db.commit()
      
      return jsonify({"message": "Study history cleared successfully"}), 200
    except Exception as e:
      return jsonify({"error": str(e)}), 500