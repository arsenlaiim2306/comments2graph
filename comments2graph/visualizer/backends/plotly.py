import plotly.express as px
import pandas as pd

class VisualizerBackend:
	def __init__(self, texts, vectors, clusters, color_palette=px.colors.qualitative.Alphabet, dark_theme=True, logger=None):
		"""
		texts: Список текстовых подписей
		vectors: Массив векторов формы (N, 2) или (N, 3)
		clusters: Массив меток кластеров формы (N,)
		"""

		self._validate_inputs(texts, vectors, clusters)
		self.logger = logger

		self.dark_theme = dark_theme
		
		self.texts = texts

		self.vectors = vectors
		self.dim = vectors.shape[1]

		self.clusters = clusters.astype(str)

		self.color_palette = color_palette
		self.fig = None
		
		self.df = self._prepare_dataframe()

	def __call__(self, title="Visualization", marker_size=5, opacity=0.7, show=True):
		"""
		title: Заголовок графика
		marker_size: Размер маркеров
		opacity: Прозрачность маркеров (0-1)
		"""

		if self.dim == 3:
			self._plot_3d(title)
		else:
			self._plot_2d(title)

		self._configure_layout(marker_size, opacity)
		
		if show:
			self.fig.show()

	def save_html(self, filename="visualization.html"):
		"""Сохранение графика в HTML файл"""
		if self.fig is None:
			if self.logger is not None:
				self.logger.error("Plot not created yet. Call __call__() first")
			raise RuntimeError("Plot not created yet. Call __call__() first")
		
		self.fig.write_html(filename)

	def save_image(self,filename="visualization.png"):
		"""Сохранение графика в файл изображения"""
		if self.dim == 3:
			if self.logger is not None:
				self.logger.error("3D images export not supported")
			raise NotImplementedError("3D images export not supported")
		if self.fig is None:
			if self.logger is not None:
				self.logger.error("Plot not created yet. Call __call__() first")
			raise RuntimeError("Plot not created yet. Call __call__() first")
		
		self.fig.write_image(filename, width=1200, height=800)


	def _validate_inputs(self, texts, vectors, clusters):
		"""Проверка согласованности входных данных"""
		if len(texts) != vectors.shape[0]:
			if self.logger is not None:
				self.logger.error("Texts and vectors must have the same length")
			raise ValueError("Texts and vectors must have the same length")

		if clusters.shape[0] != vectors.shape[0]:
			if self.logger is not None:
				self.logger.error("Clusters and vectors must have the same length")
			raise ValueError("Clusters and vectors must have the same length")

		if vectors.shape[1] not in (2, 3):
			if self.logger is not None:
				self.logger.error("Vectors must be 2D or 3D")
			raise ValueError("Vectors must be 2D or 3D")

	def _prepare_dataframe(self) -> pd.DataFrame:
		"""Создание структурированного DataFrame из входных данных"""
		data = {
			'text': self.texts,
			'cluster': self.clusters
		}
		
		coord_names = ['x', 'y', 'z'][:self.dim]
		for i, name in enumerate(coord_names):
			data[name] = self.vectors[:, i]
			
		return pd.DataFrame(data)

	def _plot_3d(self, title):
		"""Построение 3D визуализации"""
		self.fig = px.scatter_3d(
			self.df,
			x='x',
			y='y',
			z='z',
			color='cluster',
			hover_name='text',
			title=title,
			color_discrete_sequence=self.color_palette
		)

	def _plot_2d(self, title):
		"""Построение 2D визуализации"""
		self.fig = px.scatter(
			self.df,
			x='x',
			y='y',
			color='cluster',
			hover_name='text',
			title=title,
			color_discrete_sequence=self.color_palette
		)

	def _configure_layout(self, marker_size, opacity):
		"""Настройка отображения с учетом темы"""
		# Настройки для темной темы
		if self.dark_theme:
			layout = dict(
				plot_bgcolor="rgb(30, 30, 30)",  # Темный фон графика
				paper_bgcolor="rgb(30, 30, 30)",  # Темный фон области
				font=dict(color="white"),  # Белый текст
				hoverlabel=dict(
					bgcolor="rgb(50, 50, 50)",  # Темный фон подсказки
					font=dict(color="white")  # Белый текст подсказки
				)
			)
			marker_line_color = "white"  # Цвет обводки маркеров
		else:
			layout = dict(
				plot_bgcolor="white",
				paper_bgcolor="white",
				font=dict(color="black"),
				hoverlabel=dict(
					bgcolor="white",
					font=dict(color="black")
				)
			)
			marker_line_color = "DarkSlateGrey"

		# Общие настройки маркеров
		self.fig.update_traces(
			marker=dict(
				size=marker_size,
				opacity=opacity,
				line=dict(width=0.5, color=marker_line_color)
			)
		)

		# Применение настроек темы и других параметров
		self.fig.update_layout(
			**layout,  # Применяем настройки темы
			legend=dict(
				title_text='Clusters',
				itemsizing='constant',
				traceorder='normal'
			)
		)