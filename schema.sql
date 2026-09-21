CREATE TABLE IF NOT EXISTS drops (
    id UUID PRIMARY KEY,
    content TEXT NOT NULL,
    expires_at TIMESTAMPTZ,
    views_remaining INTEGER
);
