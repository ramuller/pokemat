from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass
from pathlib import Path

ALLOWED_KINDS = {
    'point',
    'icon',
    'but-g',
    'but-r',
    'but-bw',
}

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
                CHECK (kind IN ('but-r', 'but-g', 'but-b', 'but-bw', 'but-wb', 'icon', 'point')),
            x          INTEGER,
            y          INTEGER,
            xe         INTEGER,
            ye         INTEGER,
            color_r    INTEGER CHECK (color_r BETWEEN 0 AND 255),
            color_g    INTEGER CHECK (color_g BETWEEN 0 AND 255),
            color_b    INTEGER CHECK (color_b BETWEEN 0 AND 255),
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

    def add_widget(
        self,
        *,
        name: str,
        screen: str,
        kind: str,
        x: int | None = None,
        y: int | None = None,
        xe: int | None = None,
        ye: int | None = None,
        color_r: int | None = None,
        color_g: int | None = None,
        color_b: int | None = None,
        text: str | None = None,
        tolerance: int | None = None,
        movement: str | None = None,
        icon: str | None = None,
    ) -> int:
        """
        Insert a widget record.
        Returns the new widget id.
        """

        allowed_kinds = {'but-r', 'but-g', 'but-b', 'but-bw', 'but-wb', 'icon', 'point'}
        if kind not in allowed_kinds:
            raise ValueError(f"Invalid kind: {kind!r}")

        # Optional sanity checks (cheap and helpful)
        if x is not None and xe is not None and xe < x:
            raise ValueError("xe must be >= x")

        if y is not None and ye is not None and ye < y:
            raise ValueError("ye must be >= y")

        cur = self.conn.execute(
            """
            INSERT INTO widgets (
                name,
                screen,
                kind,
                x, y, xe, ye,
                color_r, color_g, color_b,
                text, tolerance, movement, icon
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                screen,
                kind,
                x, y, xe, ye,
                color_r, color_g, color_b,
                text, tolerance, movement, icon,
            ),
        )

        self.conn.commit()
        return cur.lastrowid

