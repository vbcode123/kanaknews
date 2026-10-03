import sqlite3
from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        try:
            from django.conf import settings
            from django.utils import timezone
            db_path = settings.DATABASES['default']['NAME']
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(app_news)")
            columns = [col[1] for col in cursor.fetchall()]
            altered = False
            if 'is_script_edited_by_copy_editor' not in columns:
                cursor.execute("ALTER TABLE app_news ADD COLUMN is_script_edited_by_copy_editor bool NOT NULL DEFAULT 0")
                altered = True
            if 'sent_to_visual_editor_at' not in columns:
                cursor.execute("ALTER TABLE app_news ADD COLUMN sent_to_visual_editor_at datetime NULL")
                altered = True
            if 'is_graphics_completed' not in columns:
                cursor.execute("ALTER TABLE app_news ADD COLUMN is_graphics_completed bool NOT NULL DEFAULT 0")
                altered = True
            if 'graphics_sent_to_visual_editor_at' not in columns:
                cursor.execute("ALTER TABLE app_news ADD COLUMN graphics_sent_to_visual_editor_at datetime NULL")
                altered = True

            cursor.execute("SELECT name FROM django_migrations WHERE app='app' AND name='0016_news_copy_editor_status'")
            if not cursor.fetchone():
                now_str = timezone.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                cursor.execute(
                    "INSERT INTO django_migrations (app, name, applied) VALUES (?, ?, ?)",
                    ('app', '0016_news_copy_editor_status', now_str)
                )
                altered = True

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS app_deskvisualchatmessage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    desk_id INTEGER NOT NULL REFERENCES app_desk(id) ON DELETE CASCADE,
                    visual_editor_id INTEGER NOT NULL REFERENCES app_visualeditor(id) ON DELETE CASCADE,
                    sender_type VARCHAR(20) NOT NULL,
                    sender_user_id INTEGER NULL REFERENCES auth_user(id) ON DELETE SET NULL,
                    message TEXT NOT NULL,
                    attachment VARCHAR(100) NULL,
                    is_read BOOLEAN NOT NULL DEFAULT 0,
                    read_at DATETIME NULL,
                    created_at DATETIME NOT NULL,
                    updated_at DATETIME NOT NULL
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS app_deskvisualchat_desk_idx ON app_deskvisualchatmessage(desk_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS app_deskvisualchat_ve_idx ON app_deskvisualchatmessage(visual_editor_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS app_deskvisualchat_created_idx ON app_deskvisualchatmessage(created_at)")

            cursor.execute("SELECT name FROM django_migrations WHERE app='app' AND name='0017_desk_visual_editor_chat'")
            if not cursor.fetchone():
                now_str = timezone.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                cursor.execute(
                    "INSERT INTO django_migrations (app, name, applied) VALUES (?, ?, ?)",
                    ('app', '0017_desk_visual_editor_chat', now_str)
                )
                altered = True

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS app_deskcopychatmessage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    desk_id INTEGER NOT NULL REFERENCES app_desk(id) ON DELETE CASCADE,
                    copy_editor_id INTEGER NOT NULL REFERENCES app_copyeditor(id) ON DELETE CASCADE,
                    sender_type VARCHAR(20) NOT NULL,
                    sender_user_id INTEGER NULL REFERENCES auth_user(id) ON DELETE SET NULL,
                    message TEXT NOT NULL,
                    attachment VARCHAR(100) NULL,
                    is_read BOOLEAN NOT NULL DEFAULT 0,
                    read_at DATETIME NULL,
                    created_at DATETIME NOT NULL,
                    updated_at DATETIME NOT NULL
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS app_deskcopychat_desk_idx ON app_deskcopychatmessage(desk_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS app_deskcopychat_ce_idx ON app_deskcopychatmessage(copy_editor_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS app_deskcopychat_created_idx ON app_deskcopychatmessage(created_at)")

            cursor.execute("SELECT name FROM django_migrations WHERE app='app' AND name='0018_desk_copy_editor_chat'")
            if not cursor.fetchone():
                now_str = timezone.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                cursor.execute(
                    "INSERT INTO django_migrations (app, name, applied) VALUES (?, ?, ?)",
                    ('app', '0018_desk_copy_editor_chat', now_str)
                )
                altered = True

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS app_deskvoiceoverchatmessage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    desk_id INTEGER NOT NULL REFERENCES app_desk(id) ON DELETE CASCADE,
                    voice_over_id INTEGER NOT NULL REFERENCES app_voiceoveruser(id) ON DELETE CASCADE,
                    sender_type VARCHAR(20) NOT NULL,
                    sender_user_id INTEGER NULL REFERENCES auth_user(id) ON DELETE SET NULL,
                    message TEXT NOT NULL,
                    attachment VARCHAR(100) NULL,
                    is_read BOOLEAN NOT NULL DEFAULT 0,
                    read_at DATETIME NULL,
                    created_at DATETIME NOT NULL,
                    updated_at DATETIME NOT NULL
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS app_deskvochat_desk_idx ON app_deskvoiceoverchatmessage(desk_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS app_deskvochat_vo_idx ON app_deskvoiceoverchatmessage(voice_over_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS app_deskvochat_created_idx ON app_deskvoiceoverchatmessage(created_at)")

            cursor.execute("SELECT name FROM django_migrations WHERE app='app' AND name='0019_desk_voice_over_chat'")
            if not cursor.fetchone():
                now_str = timezone.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                cursor.execute(
                    "INSERT INTO django_migrations (app, name, applied) VALUES (?, ?, ?)",
                    ('app', '0019_desk_voice_over_chat', now_str)
                )
                altered = True

            # Ensure last_seen column on staff tables
            for tbl in ['app_desk', 'app_voiceoveruser', 'app_copyeditor', 'app_visualeditor', 'app_socialmedia', 'app_reporter']:
                cursor.execute(f"PRAGMA table_info({tbl})")
                tbl_cols = [c[1] for c in cursor.fetchall()]
                if 'last_seen' not in tbl_cols:
                    cursor.execute(f"ALTER TABLE {tbl} ADD COLUMN last_seen datetime NULL")
                    altered = True

            cursor.execute("SELECT name FROM django_migrations WHERE app='app' AND name='0020_add_last_seen_to_staff'")
            if not cursor.fetchone():
                now_str = timezone.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                cursor.execute(
                    "INSERT INTO django_migrations (app, name, applied) VALUES (?, ?, ?)",
                    ('app', '0020_add_last_seen_to_staff', now_str)
                )
                altered = True

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS app_desksocialchatmessage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    desk_id INTEGER NOT NULL REFERENCES app_desk(id) ON DELETE CASCADE,
                    social_media_id INTEGER NOT NULL REFERENCES app_socialmedia(id) ON DELETE CASCADE,
                    sender_type VARCHAR(20) NOT NULL,
                    sender_user_id INTEGER NULL REFERENCES auth_user(id) ON DELETE SET NULL,
                    message TEXT NOT NULL,
                    attachment VARCHAR(100) NULL,
                    is_read BOOLEAN NOT NULL DEFAULT 0,
                    read_at DATETIME NULL,
                    created_at DATETIME NOT NULL,
                    updated_at DATETIME NOT NULL
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS app_desksmchat_desk_idx ON app_desksocialchatmessage(desk_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS app_desksmchat_sm_idx ON app_desksocialchatmessage(social_media_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS app_desksmchat_created_idx ON app_desksocialchatmessage(created_at)")

            cursor.execute("SELECT name FROM django_migrations WHERE app='app' AND name='0021_desk_social_media_chat'")
            if not cursor.fetchone():
                now_str = timezone.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                cursor.execute(
                    "INSERT INTO django_migrations (app, name, applied) VALUES (?, ?, ?)",
                    ('app', '0021_desk_social_media_chat', now_str)
                )
                altered = True

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS app_deskreporterchatmessage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    desk_id INTEGER NOT NULL REFERENCES app_desk(id) ON DELETE CASCADE,
                    reporter_id INTEGER NOT NULL REFERENCES app_reporter(id) ON DELETE CASCADE,
                    sender_type VARCHAR(20) NOT NULL,
                    sender_user_id INTEGER NULL REFERENCES auth_user(id) ON DELETE SET NULL,
                    message TEXT NOT NULL,
                    attachment VARCHAR(100) NULL,
                    is_read BOOLEAN NOT NULL DEFAULT 0,
                    read_at DATETIME NULL,
                    created_at DATETIME NOT NULL,
                    updated_at DATETIME NOT NULL
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS app_deskreporterchat_desk_idx ON app_deskreporterchatmessage(desk_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS app_deskreporterchat_rep_idx ON app_deskreporterchatmessage(reporter_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS app_deskreporterchat_created_idx ON app_deskreporterchatmessage(created_at)")

            cursor.execute("SELECT name FROM django_migrations WHERE app='app' AND name='0022_desk_reporter_chat'")
            if not cursor.fetchone():
                now_str = timezone.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                cursor.execute(
                    "INSERT INTO django_migrations (app, name, applied) VALUES (?, ?, ?)",
                    ('app', '0022_desk_reporter_chat', now_str)
                )
                altered = True

            if altered:
                conn.commit()
            conn.close()
        except Exception:
            pass
