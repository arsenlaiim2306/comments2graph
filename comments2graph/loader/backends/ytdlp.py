from yt_dlp import YoutubeDL
from ..url_tool import URLTool

class LoaderBackend:
	def __init__(self, config, logger=None):
		self.logger = logger

		self.ydl_opts = {
			'extract_flat': False,				# Не извлекать информацию о видео
			'extract_comments': True,			# Извлекать комментарии
			'getcomments': True,				# Получить комментарии
			'no_warnings': True,				# Игнорировать предупреждения
		}
		
		for key, val in config.items():
			self.ydl_opts[key] = val

	def __call__(self, url):
		if URLTool.is_youtube_url(url):
			with YoutubeDL(self.ydl_opts) as ydl:
				# Извлекаем информацию о видео, включая комментарии
				info_dict = ydl.extract_info(url, download=False)
				
				# Получаем комментарии
				comments = info_dict.get('comments', [])
				comments = [comm["text"] for comm in comments]
				
				return comments
		else:
			raise ValueError(f"Unsupported url")