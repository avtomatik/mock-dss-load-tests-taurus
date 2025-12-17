# =============================================================================
# Pre-defined SQL Queries
# =============================================================================
SQL_SELECT_COUNT = """
SELECT count(*)
FROM signatures
WHERE DATE(signed_at) = %s;
"""

SQL_INSERT_DOCUMENT = """
INSERT INTO documents (document_id, content, created_at)
VALUES (%s, %s, NOW());
"""
