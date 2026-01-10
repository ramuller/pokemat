from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass
from pathlib import Path


def _sanitize_phone_name(phone: str) -> str:
    """
    Keep filenames safe-ish. Adjust rules as you like.
    """
    phone = phone.strip()
    if not phone:
        raise ValueError("phone model name must not be empty")

    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-")
    cleaned = "".join(c for c in phone if c in allowed)

    if not cleaned:
        raise ValueError(f"phone model name {phone!r} becomes empty after sanitizing")

    return cleaned


def phone_db_path(phone: str, base_dir: Path | None = None) -> Path:
    """
    Returns ~/.config/pokemat/<phone>.db (or custom base_dir).
    """
    phone = _sanitize_phone_name(phone)

    if base_dir is None:
        # Respect XDG_CONFIG_HOME when present; fallback to ~/.config
        xdg = os.environ.get("XDG_CONFIG_HOME")
        base_dir = Path(xdg).expanduser() if xdg else Path.home() / ".config"

    return base_dir / "pokemat" / f"{phone}.db"


def init_schema(conn: sqlite3.Connection) -> None:
    """
    Create tables needed by your app. Example schema.
    """
    conn.executescript(
        """
        PRAGMA journal_mode = WAL;
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS meta (
            key   TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS widgets (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT NOT NULL,
            screen     TEXT NOT NULL,
            kind       TEXT NOT NULL
                CHECK (kind IN ('but-g', '', 'but-r', 'but-bw', 'icon')),
            x          INTEGER NOT NULL,
            y          INTEGER NOT NULL,
            color_r    INTEGER,
            color_g    INTEGER,
            color_b    INTEGER,
            text       TEXT,
            tolerance  INTEGER,
            movement   TEXT,
            icon       TEXT
        );
        """
    )
    conn.commit()


@dataclass
class PhoneDB:
    phone: str
    conn: sqlite3.Connection
    learning_mode: bool
    path: Path

    @classmethod
    def open_for_phone(cls, phone: str) -> "PhoneDB":
        path = phone_db_path(phone)
        path.parent.mkdir(parents=True, exist_ok=True)

        learning_mode = not path.exists()

        # Connect (creates the file if it doesn't exist)
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row

        # Initialize schema (safe to do always)
        init_schema(conn)

        return cls(phone=phone, conn=conn, learning_mode=learning_mode, path=path)

    def close(self) -> None:
        self.conn.close()
