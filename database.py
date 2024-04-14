import sqlite3

class Database:
    def __init__(self, db_name='bot_database.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_database()

    def create_database(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tokens (
                                chat_id INTEGER PRIMARY KEY,
                                token_count INTEGER DEFAULT 500
                            )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS requests (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                chat_id INTEGER,
                                request_text TEXT,
                                request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY(chat_id) REFERENCES tokens(chat_id)
                            )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS voice_choices (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                chat_id INTEGER,
                                voice_choice TEXT,
                                choice_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY(chat_id) REFERENCES tokens(chat_id)
                            )''')
        self.conn.commit()

    def add_user(self, chat_id, token_count=500):
        self.cursor.execute("INSERT OR IGNORE INTO tokens (chat_id, token_count) VALUES (?, ?)", (chat_id, token_count))
        self.conn.commit()

    def get_token_count(self, chat_id):
        self.cursor.execute("SELECT token_count FROM tokens WHERE chat_id = ?", (chat_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]  # Возвращает количество символов для данного chat_id
        else:
            return None

    def update_token_count(self, chat_id, new_count):
        self.cursor.execute("UPDATE tokens SET token_count = ? WHERE chat_id = ?", (new_count, chat_id))
        self.conn.commit()

    def save_request(self, chat_id, request_text):
        self.cursor.execute("INSERT INTO requests (chat_id, request_text) VALUES (?, ?)", (chat_id, request_text))
        self.conn.commit()

    def save_voice_choice(self, chat_id, voice_choice):
        self.cursor.execute("INSERT INTO voice_choices (chat_id, voice_choice) VALUES (?, ?)", (chat_id, voice_choice))
        self.conn.commit()

    def close(self):
        self.conn.close()