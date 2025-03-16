import re


class URLTool():
	def is_url(path):
		url_pattern = re.compile(r'^https?://\S+$')
		return bool(url_pattern.match(path))

	def is_youtube_url(url):
		youtube_pattern = re.compile(
			r'(https?://)?(www\.)?'
			r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
			r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
		)
		return bool(youtube_pattern.match(url))

	def extract_video_id(url):
		# Регулярное выражение для извлечения VIDEO_ID
		patterns = [
			r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]+)',
			r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)',
			r'(?:https?:\/\/)?(?:www\.)?youtube-nocookie\.com\/embed\/([a-zA-Z0-9_-]+)'
		]
		
		for pattern in patterns:
			match = re.search(pattern, url)
			if match:
				return match.group(1)
		
		raise ValueError("Неверный URL видео. Невозможно извлечь VIDEO_ID.")