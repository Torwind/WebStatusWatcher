SCHEMA = """
CREATE TABLE IF NOT EXISTS settings
(
    id INTEGER PRIMARY KEY,

    key TEXT UNIQUE NOT NULL,

    value TEXT
);

CREATE TABLE IF NOT EXISTS sites
(
    id INTEGER PRIMARY KEY,

    name TEXT NOT NULL,

    url TEXT NOT NULL,

    enabled INTEGER NOT NULL DEFAULT 1,

    interval_seconds INTEGER NOT NULL DEFAULT 30,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS history
(
    id INTEGER PRIMARY KEY,

    site_id INTEGER NOT NULL,

    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    status_code INTEGER,

    response_time REAL,

    changed INTEGER DEFAULT 0,

    FOREIGN KEY(site_id)
        REFERENCES sites(id)
);

CREATE TABLE IF NOT EXISTS events
(
    id INTEGER PRIMARY KEY,

    site_id INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    level TEXT,

    message TEXT,

    FOREIGN KEY(site_id)
        REFERENCES sites(id)
);
"""