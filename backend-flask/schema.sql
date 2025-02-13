-- First drop tables if they exist to ensure clean state
DROP TABLE IF EXISTS word_review_items;
DROP TABLE IF EXISTS word_reviews;
DROP TABLE IF EXISTS word_groups;
DROP TABLE IF EXISTS study_sessions;
DROP TABLE IF EXISTS study_activities;
DROP TABLE IF EXISTS groups;
DROP TABLE IF EXISTS words;

-- Create tables
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    words_count INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS study_activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    preview_url TEXT
);

CREATE TABLE IF NOT EXISTS study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER NOT NULL,
    study_activity_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (study_activity_id) REFERENCES study_activities(id)
);

CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    french TEXT NOT NULL,
    english TEXT NOT NULL,
    parts TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS word_groups (
    word_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    FOREIGN KEY (word_id) REFERENCES words(id),
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

CREATE TABLE IF NOT EXISTS word_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL,
    correct_count INTEGER DEFAULT 0,
    wrong_count INTEGER DEFAULT 0,
    last_reviewed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (word_id) REFERENCES words(id)
);

CREATE TABLE IF NOT EXISTS word_review_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL,
    study_session_id INTEGER NOT NULL,
    correct BOOLEAN NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (word_id) REFERENCES words(id),
    FOREIGN KEY (study_session_id) REFERENCES study_sessions(id)
);

-- Delete any existing test data
DELETE FROM groups;
DELETE FROM study_activities;

-- Reset the autoincrement counters
DELETE FROM sqlite_sequence WHERE name='groups';
DELETE FROM sqlite_sequence WHERE name='study_activities';

-- Insert test data
INSERT INTO groups (id, name, words_count) VALUES (1, 'Test Group', 0);
INSERT INTO study_activities (id, name, url, preview_url) 
VALUES (1, 'Typing Tutor', 'http://localhost:8080', '/assets/study_activities/typing_tutor.png');

-- Verify the inserts worked
SELECT * FROM groups;
SELECT * FROM study_activities;