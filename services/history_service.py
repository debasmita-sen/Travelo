import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional
import uuid

from config import DATABASE_PATH


def init_history_store():
    """Ensure the chat_history table exists and migrate older schemas.

    Creates `chat_history` when missing. If the table exists but lacks
    `conversation_id`, the function adds the column and populates each row
    with a generated UUID so older rows are grouped under unique conversations.
    """
    with _connect() as connection:
        # Check if table exists
        table_exists = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='chat_history'"
        ).fetchone()

        if not table_exists:
            # Create new table with conversation_id
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_history (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  conversation_id TEXT NOT NULL,
                  type TEXT NOT NULL,
                  title TEXT NOT NULL,
                  message TEXT NOT NULL,
                  payload TEXT NOT NULL,
                  created_at TEXT NOT NULL
                )
                """
            )
        else:
            # Migrate existing table to add conversation_id if it doesn't exist
            columns = connection.execute("PRAGMA table_info(chat_history)").fetchall()
            column_names = [col[1] for col in columns]

            if "conversation_id" not in column_names:
                # Add conversation_id column and populate with UUIDs
                connection.execute("ALTER TABLE chat_history ADD COLUMN conversation_id TEXT")
                # Assign each row a unique conversation_id
                rows = connection.execute("SELECT id FROM chat_history").fetchall()
                for row in rows:
                    conv_id = str(uuid.uuid4())
                    connection.execute("UPDATE chat_history SET conversation_id = ? WHERE id = ?", (conv_id, row[0]))
                connection.commit()


def save_history_item(item_type: str, title: str, message: str, payload: Dict, conversation_id: Optional[str] = None) -> Dict:
    """Save a message or report into the history store and return its metadata."""
    init_history_store()
    if not conversation_id:
        conversation_id = str(uuid.uuid4())  # create a conversation id if not supplied
    created_at = datetime.now().isoformat(timespec="seconds")
    with _connect() as connection:
        cursor = connection.execute(
            """
            INSERT INTO chat_history (conversation_id, type, title, message, payload, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (conversation_id, item_type, title or "Chat", message or "", json.dumps(payload), created_at),
        )
        item_id = cursor.lastrowid
    return {
        "id": item_id,
        "conversation_id": conversation_id,
        "type": item_type,
        "destination": title or "Chat",
        "date": created_at,
        "message": message or "",
        **_payload_fields(item_type, payload),
    }


def list_history(limit: int = 30) -> List[Dict]:
    """Return a short list of recent conversation summaries (one row per convo)."""
    init_history_store()
    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT id, conversation_id, type, title, message, payload, created_at
            FROM chat_history
            WHERE id IN (
                SELECT MAX(id)
                FROM chat_history
                GROUP BY conversation_id
            )
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [_row_to_item(row) for row in rows]


def get_conversation(conversation_id: str) -> List[Dict]:
    """Get all messages in a conversation"""
    init_history_store()
    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT id, conversation_id, type, title, message, payload, created_at
            FROM chat_history
            WHERE conversation_id = ?
            ORDER BY id ASC
            """,
            (conversation_id,),
        ).fetchall()

    return [_row_to_item(row) for row in rows]


def delete_history_item(item_id: int) -> bool:
    """Delete a single history row by id."""
    init_history_store()
    with _connect() as connection:
        cursor = connection.execute("DELETE FROM chat_history WHERE id = ?", (item_id,))
        connection.commit()
    return cursor.rowcount > 0


def delete_conversation(conversation_id: str) -> bool:
    """Delete all rows for a given conversation_id."""
    init_history_store()
    with _connect() as connection:
        cursor = connection.execute("DELETE FROM chat_history WHERE conversation_id = ?", (conversation_id,))
        connection.commit()
    return cursor.rowcount > 0


def clear_history() -> None:
    """Clear all history from the database"""
    init_history_store()
    with _connect() as connection:
        connection.execute("DELETE FROM chat_history")
        connection.commit()


def _connect():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.isolation_level = None  # Auto-commit mode
    return connection


def _row_to_item(row) -> Dict:
    try:
        payload = json.loads(row["payload"])
    except (TypeError, ValueError):
        payload = {}
    return {
        "id": row["id"],
        "conversation_id": row["conversation_id"],
        "type": row["type"],
        "destination": row["title"],
        "date": row["created_at"],
        "message": row["message"],
        **_payload_fields(row["type"], payload),
    }


def _payload_fields(item_type: str, payload: Dict) -> Dict:
    if item_type == "chat":
        return {"answer": payload.get("answer", "")}
    return {"report": payload.get("report", payload)}
