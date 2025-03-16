from googleapiclient.discovery import build
from ..url_tool import URLTool

class LoaderBackend:
	def __init__(self, config, logger=None):
		self.logger = logger
		
		self.conf = {
			"serviceName": "youtube",
			"version": "v3"
		}
		for key, val in config.items():
			conf[key] = val

		if "developerKey" in self.conf:
			self.api_key = self.conf["developerKey"]
		else:
			raise ValueError(f"developerKey not found")

	def __call__(video_id):
		if URLTool.is_youtube_url(url):
			# Создаем сервис для работы с YouTube API
			youtube = build(**self.conf)
			
			# Функция для получения комментариев
			def get_video_comments(video_id):
				comments = []
				next_page_token = None

				while True:
					# Запрос к API для получения комментариев
					request = youtube.commentThreads().list(
						part='snippet',
						videoId=video_id,
						pageToken=next_page_token,
						textFormat='plainText',
						maxResults=100  # Максимальное количество комментариев за один запрос
					)
					response = request.execute()

					# Извлекаем комментарии из ответа
					for item in response['items']:
						comment = item['snippet']['topLevelComment']['snippet']
						comments.append({
							'author': comment['authorDisplayName'],
							'text': comment['textDisplay'],
							'published_at': comment['publishedAt']
						})

					# Проверяем, есть ли следующая страница
					next_page_token = response.get('nextPageToken')
					if not next_page_token:
						break

				return comments

			# Получаем комментарии
			comments = get_video_comments(video_id)
			comments = [comm["text"] for comm in comments]
			return comments
		else:
			raise ValueError(f"Unsupported url")