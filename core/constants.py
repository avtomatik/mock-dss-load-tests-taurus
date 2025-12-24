SIGN_RESPONSE_MODEL_FIELDS = [
    "signature_id",
    "document_id",
    "signed_at",
    "signature_value",
]


_API = "http://localhost:8000"


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
