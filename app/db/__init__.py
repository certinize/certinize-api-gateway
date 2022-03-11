"""
app.db
~~~~~~

This module contains the operations for creating the database and its tables.

We use SQLModel to create the database and its tables.

Connecting to a database using a connection pool:
1. We initialize connection pool using sqlmodel's `create_async_engine()`.
2. A function yields a connection/session from the pool.
3. Services use the function as a dependency (DI).
"""
