import sqlite3
from typing import List, Optional, Tuple

class DataStorage:
	def __init__(self, db_path: str = 'data.db', make_new=False):
		self.db_path = db_path

		self._init_db()
		if make_new:
			self.clear_table()

	def _init_db(self):
		"""Создает таблицу, если она не существует."""
		with sqlite3.connect(self.db_path) as conn:
			cursor = conn.cursor()
			cursor.execute('''
				CREATE TABLE IF NOT EXISTS data (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					text TEXT NOT NULL UNIQUE,
					vector BLOB
				)
			''')
			conn.commit()


	# Запись
	def add_text_records(self, texts: List[str]):
		if texts:
			old_texts = self.get_all_texts()
			new_texts = list(set(texts) - set(old_texts))

			with sqlite3.connect(self.db_path) as conn:
				cursor = conn.cursor()

				# Вставляем тексты, пропуская дубликаты
				cursor.executemany('''
					INSERT INTO data (text, vector) VALUES (?, ?)
				''', [(text, None) for text in new_texts])
				conn.commit()

	def update_vector_by_id(self, record_id: int, vector: bytes):
		with sqlite3.connect(self.db_path) as conn:
			cursor = conn.cursor()
			# Проверяем существование id
			cursor.execute('SELECT id FROM data WHERE id = ?', (record_id,))

			if cursor.fetchone():
				# Вставляем выектор по индексу
				cursor.execute('''
					UPDATE data SET vector = ? WHERE id = ?
				''', (vector, record_id))
				conn.commit()

	# Чтение
	def get_all_texts(self) -> List[str]:
		with sqlite3.connect(self.db_path) as conn:
			cursor = conn.cursor()
			cursor.execute('SELECT text FROM data')
			return [row[0] for row in cursor.fetchall()]

	def get_all_vectors(self) -> List[bytes]:
		with sqlite3.connect(self.db_path) as conn:
			cursor = conn.cursor()
			cursor.execute('SELECT vector FROM data')
			return [row[0] for row in cursor.fetchall() if row[0] is not None]

	# Очистка
	def clear_table(self):
		with sqlite3.connect(self.db_path) as conn:
			cursor = conn.cursor()
			cursor.execute('DELETE FROM data')
			cursor.execute('DELETE FROM sqlite_sequence WHERE name="data"')
			conn.commit()