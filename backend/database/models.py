"""
Database schema definitions for Enterprise Expert Knowledge Worker.
Supports both PostgreSQL and SQLite.
"""

SCHEMA_SQL = """
-- Employees Table
CREATE TABLE IF NOT EXISTS employees (
    employee_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    department TEXT NOT NULL,
    role TEXT NOT NULL,
    location TEXT NOT NULL,
    employment_type TEXT NOT NULL, -- Full-time, Contractor, Intern
    manager TEXT NOT NULL,
    status TEXT NOT NULL,          -- Active, On_Leave, Terminated
    tenure_months INTEGER NOT NULL,
    performance_rating REAL NOT NULL, -- e.g. 3.8, 4.2
    remote_eligible INTEGER NOT NULL,  -- 1 or 0
    clear_access_level TEXT NOT NULL  -- Public, Confidential, Secret, TopSecret
);

-- Products Table
CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    eligibility TEXT NOT NULL,
    price TEXT NOT NULL,
    requirements TEXT NOT NULL,
    underwriter TEXT NOT NULL,
    status TEXT NOT NULL
);

-- Policies Table
CREATE TABLE IF NOT EXISTS policies (
    policy_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    department TEXT NOT NULL,
    version TEXT NOT NULL,
    last_updated TEXT NOT NULL,
    file_path TEXT NOT NULL
);

-- Contracts Table
CREATE TABLE IF NOT EXISTS contracts (
    contract_id TEXT PRIMARY KEY,
    vendor_name TEXT NOT NULL,
    contract_type TEXT NOT NULL,
    effective_date TEXT NOT NULL,
    expiry_date TEXT NOT NULL,
    sla_uptime TEXT,
    governing_law TEXT NOT NULL,
    status TEXT NOT NULL
);

-- Access Requests Table (Managed via Human-in-the-Loop)
CREATE TABLE IF NOT EXISTS access_requests (
    request_id TEXT PRIMARY KEY,
    employee_id TEXT NOT NULL,
    employee_name TEXT NOT NULL,
    product_or_system TEXT NOT NULL,
    reason TEXT NOT NULL,
    risk_level TEXT NOT NULL,     -- Low, Medium, High, Critical
    status TEXT NOT NULL,         -- PENDING, APPROVED, REJECTED
    requested_operation TEXT NOT NULL,
    approved_by TEXT,
    request_timestamp TEXT NOT NULL,
    approval_timestamp TEXT
);

-- Audit Logs Table
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id TEXT PRIMARY KEY,
    query_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    user_id TEXT NOT NULL,
    action_type TEXT NOT NULL,
    agent_name TEXT NOT NULL,
    details TEXT NOT NULL,
    status TEXT NOT NULL,
    duration_ms INTEGER NOT NULL
);

-- Chat Sessions (every conversation is persisted)
CREATE TABLE IF NOT EXISTS chat_sessions (
    session_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    user_role TEXT NOT NULL,
    title TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- Chat Messages (user, assistant and system turns with full response metadata as JSON)
CREATE TABLE IF NOT EXISTS chat_messages (
    message_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    sender TEXT NOT NULL,          -- user, assistant, system
    content TEXT NOT NULL,
    metadata TEXT,                 -- JSON: citations, plan, trace, approval card, etc.
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_chat_messages_session ON chat_messages(session_id, created_at);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_role ON chat_sessions(user_role, updated_at);

-- Uploaded Documents (files added through the Upload UI)
CREATE TABLE IF NOT EXISTS uploaded_documents (
    doc_id TEXT PRIMARY KEY,
    original_filename TEXT NOT NULL,
    stored_path TEXT NOT NULL,
    title TEXT NOT NULL,
    doc_type TEXT NOT NULL,         -- policy, product, contract
    department TEXT NOT NULL,
    access_roles TEXT NOT NULL,     -- comma separated
    size_bytes INTEGER NOT NULL,
    uploaded_by_role TEXT NOT NULL,
    uploaded_at TEXT NOT NULL,
    chunk_count INTEGER NOT NULL DEFAULT 0
);

-- FAQ auto-update: how often each question is asked (all users and roles combined).
-- The question text is stored only once an entry is published; before that only a hash is kept.
CREATE TABLE IF NOT EXISTS faq_candidates (
    question_key TEXT PRIMARY KEY,      -- sha1 of the normalised question
    ask_count INTEGER NOT NULL DEFAULT 0,
    first_asked TEXT NOT NULL,
    last_asked TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'counting',   -- counting | published | skipped
    skip_reason TEXT,
    last_evaluated_count INTEGER NOT NULL DEFAULT 0,
    display_question TEXT,
    answer TEXT,
    sources TEXT,                       -- JSON list of {document_name, section, version}
    source_titles TEXT,                 -- JSON list of document titles the answer relies on
    published_at TEXT
);
"""
