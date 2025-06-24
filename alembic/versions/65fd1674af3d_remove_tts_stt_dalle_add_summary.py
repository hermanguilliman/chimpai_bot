"""remove tts stt dalle, add summary

Revision ID: 65fd1674af3d
Revises: c925261f9bc1
Create Date: 2025-06-23 18:10:46.669767
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "65fd1674af3d"
down_revision: Union[str, None] = "c925261f9bc1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Создание таблицы chat_settings
    op.create_table(
        "chat_settings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("settings_id", sa.Integer(), nullable=False),
        sa.Column("api_key", sa.String(length=51), nullable=True),
        sa.Column(
            "base_url",
            sa.String(length=255),
            nullable=False,
            server_default="https://api.openai.com/v1",
        ),
        sa.Column(
            "personality_name",
            sa.Text(),
            nullable=True,
            server_default="🤵 Ассистент",
        ),
        sa.Column(
            "personality_text",
            sa.Text(),
            nullable=True,
            server_default="Действуй как личный ассистент пользователя",
        ),
        sa.Column(
            "export_format",
            sa.String(length=10),
            nullable=False,
            server_default="markdown",
        ),
        sa.Column(
            "model", sa.Text(), nullable=True, server_default="gpt-4o-mini"
        ),
        sa.Column(
            "max_tokens", sa.Integer(), nullable=True, server_default="1000"
        ),
        sa.Column(
            "temperature", sa.Text(), nullable=True, server_default="0.7"
        ),
        sa.ForeignKeyConstraint(
            ["settings_id"],
            ["settings.id"],
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )

    # Создание таблицы summary_settings
    op.create_table(
        "summary_settings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("settings_id", sa.Integer(), nullable=False),
        sa.Column("api_key", sa.String(), nullable=True),
        sa.Column(
            "base_url",
            sa.String(length=255),
            nullable=False,
            server_default="https://300.ya.ru/api",
        ),
        sa.Column(
            "export_format",
            sa.String(length=10),
            nullable=False,
            server_default="markdown",
        ),
        sa.ForeignKeyConstraint(
            ["settings_id"],
            ["settings.id"],
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )

    # Перенос данных из settings в chat_settings
    op.execute("""
        INSERT INTO chat_settings (settings_id, api_key, base_url, personality_name, personality_text, export_format, model, max_tokens, temperature)
        SELECT id, api_key, base_url, personality_name, personality_text, export_format, model, max_tokens, temperature
        FROM settings
    """)

    # Создание записей в summary_settings с значениями по умолчанию
    op.execute("""
        INSERT INTO summary_settings (settings_id, api_key, base_url, export_format)
        SELECT id, NULL, 'https://300.ya.ru/api', 'markdown'
        FROM settings
    """)

    # Удаление ненужных столбцов из settings
    op.drop_column("settings", "api_key")
    op.drop_column("settings", "base_url")
    op.drop_column("settings", "personality_name")
    op.drop_column("settings", "personality_text")
    op.drop_column("settings", "export_format")
    op.drop_column("settings", "max_tokens")
    op.drop_column("settings", "model")
    op.drop_column("settings", "temperature")
    op.drop_column("settings", "tts_model")
    op.drop_column("settings", "tts_speed")
    op.drop_column("settings", "tts_voice")


def downgrade() -> None:
    """Downgrade schema."""
    # Добавление удаленных столбцов обратно в settings
    op.add_column(
        "settings", sa.Column("api_key", sa.String(length=51), nullable=True)
    )
    op.add_column(
        "settings",
        sa.Column(
            "base_url",
            sa.String(length=255),
            nullable=False,
            server_default="https://api.openai.com/v1",
        ),
    )
    op.add_column(
        "settings",
        sa.Column(
            "personality_name",
            sa.Text(),
            nullable=True,
            server_default="🤵 Ассистент",
        ),
    )
    op.add_column(
        "settings",
        sa.Column(
            "personality_text",
            sa.Text(),
            nullable=True,
            server_default="Действуй как личный ассистент пользователя",
        ),
    )
    op.add_column(
        "settings",
        sa.Column(
            "export_format",
            sa.String(length=10),
            nullable=False,
            server_default="markdown",
        ),
    )
    op.add_column(
        "settings",
        sa.Column(
            "max_tokens", sa.Integer(), nullable=True, server_default="1000"
        ),
    )
    op.add_column(
        "settings",
        sa.Column(
            "model", sa.Text(), nullable=True, server_default="gpt-4o-mini"
        ),
    )
    op.add_column(
        "settings",
        sa.Column(
            "temperature", sa.Text(), nullable=True, server_default="0.7"
        ),
    )
    op.add_column(
        "settings",
        sa.Column(
            "tts_model", sa.String(), nullable=True, server_default="tts-1-hd"
        ),
    )
    op.add_column(
        "settings",
        sa.Column(
            "tts_speed", sa.String(), nullable=True, server_default="1.0"
        ),
    )
    op.add_column(
        "settings",
        sa.Column(
            "tts_voice", sa.String(), nullable=True, server_default="alloy"
        ),
    )

    # Перенос данных из chat_settings обратно в settings
    op.execute("""
        UPDATE settings
        SET
            api_key = chat_settings.api_key,
            base_url = chat_settings.base_url,
            personality_name = chat_settings.personality_name,
            personality_text = chat_settings.personality_text,
            export_format = chat_settings.export_format,
            model = chat_settings.model,
            max_tokens = chat_settings.max_tokens,
            temperature = chat_settings.temperature
        FROM chat_settings
        WHERE chat_settings.settings_id = settings.id
    """)

    # Установка значений по умолчанию для tts-полей
    op.execute("""
        UPDATE settings
        SET
            tts_model = 'tts-1-hd',
            tts_speed = '1.0',
            tts_voice = 'alloy'
    """)

    # Удаление таблиц chat_settings и summary_settings
    op.drop_table("summary_settings")
    op.drop_table("chat_settings")
