"""
app.db
~~~~~~

This module contains the operations for creating the database and its tables.

1. We initialize connection pool using sqlmodel's `create_async_engine()`.
2. A function yields a connection/session from the pool.
"""
