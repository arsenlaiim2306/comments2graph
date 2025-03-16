from .backends import get_backend

class DataVisualizer:
	def __init__(self, backend="plotly", logger=None):
		self.logger = logger
		self.backend = get_backend(backend)

		self.visualizer = None

	def __call__(self, texts, vectors, clusters, dark_theme=True):
		self.visualizer = self.backend(texts, vectors, clusters, dark_theme=dark_theme, logger=self.logger)
		self.visualizer()

	def save(type="html", filename="visualization.html"):
		"""
		type: Тип сохранения 'file' или 'html'
		filename: Путь сохранения
		"""
		
		if type == "html":
			self.visualizer.save_html(filename)
		elif type == "image":
			self.visualizer.save_image(filename)


