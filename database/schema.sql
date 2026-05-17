-- database/schema.sql

CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    provider_id TEXT NOT NULL UNIQUE,
    provider TEXT NOT NULL,
    email TEXT UNIQUE,
    username TEXT,
    display_name TEXT,
    profile_pic TEXT,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);