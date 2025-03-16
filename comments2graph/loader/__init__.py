import os
import json
import gzip
import pickle
import hashlib

from .url_tool import URLTool
from .backends import get_backend


class DataLoader():
	def __init__(self, backend="ytdlp", conf_path="config.json", logger=None):
		self.logger = logger

		# Загрузка конфигов
		conf = self.load_confing(conf_path)

		self.cache_dir = conf.get("cache_dir", "cache")
		os.makedirs(self.cache_dir, exist_ok=True)

		self.backend = get_backend(backend)(conf.get(backend, {}), self.logger)
	
	def __call__(self, path, save_storage=None):
		#path - может содержать как url ссылку, так и файл txt

		result = {}

		if URLTool.is_url(path):
			result = self.url_loader(path)
			if save_storage is not None and result["state"] == "OK":
				save_storage.add_text_records(result["data"])
		else:
			result = self.path_loader(path)
			if save_storage is not None and result["state"] == "OK":
				all_data = [item["data"] for item in result["data"] if item.get("state") == "OK"]
				data = [text for sublist in all_data for text in sublist]
				save_storage.add_text_records(data)

		return result

	# Загрузчик конфига
	def load_confing(self, path):
		if os.path.exists(path):
			try:
				with open(path) as file:
					return json.loads(file.read())
			except (FileNotFoundError, json.JSONDecodeError) as e:
				raise RuntimeError(f"Config error: {e}")

		return {}

	# Загрузчики
	def path_loader(self, path):
		if os.path.exists(path):
			with open(path, "r") as f:
				urls = [l.strip() for l in f if l.strip() and URLTool.is_url(l.strip())]
				urls = list(set(urls))

				responses = []
				for url in urls:
					responses.append(self.url_loader(url))

				return self.return_ok(responses)
		return self.return_error("File reading error")


	def url_loader(self, url):
		cache_result = self.load_from_file(url)
		if cache_result["state"] == "OK":
			return cache_result

		try:
			data = self.backend(url)

			self.save_to_file(url, data)
			return self.return_ok(data)
		except Exception as e:
			# Логирование ошибки
			if self.logger is not None:
				self.logger.error(f"Error loading URL {url}: {e}")
			return self.return_error(str(e))


	# Кеширование
	def url2hash_path(self, url):
		url_hash = hashlib.sha256(url.encode()).hexdigest()
		return os.path.join(self.cache_dir, f"{url_hash}.pkl.gz")

	def save_to_file(self, url, data):
		cache_file = self.url2hash_path(url)
		with gzip.open(cache_file, 'wb') as f:
			pickle.dump(data, f)
	def load_from_file(self, url):
		cache_file = self.url2hash_path(url)

		try:
			if os.path.exists(cache_file):
				with gzip.open(cache_file, 'rb') as f:
					data = pickle.load(f)
					if data:
						return self.return_ok(data)
		except (EOFError, pickle.UnpicklingError) as e:
			if self.logger is not None:
				self.logger.error(f"Cache corrupted: {cache_file}")
			print(f"Cache corrupted: {cache_file}")

		return self.return_error("Cache loading error")


	# Типы результатов
	def return_ok(self, data):
		return {"state": "OK", "data": data}
	def return_error(self, msg):
		return {"state": "ERROR", "message": msg}
