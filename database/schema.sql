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


CREATE TABLE IF NOT EXISTS refresh_tokens (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    token TEXT NOT NULL UNIQUE,
    expires_at TIMESTAMP NOT NULL,
    revoked INTEGER DEFAULT 0,

    FOREIGN KEY(user_id) REFERENCES users(id)
);