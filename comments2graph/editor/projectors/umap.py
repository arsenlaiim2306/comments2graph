from umap import UMAP

class ProjectorBackend():
	def __init__(self, config, logger=None):
		self.logger = logger

		conf = {
			"n_components": 2,
		}
		for key, val in config.items():
			conf[key] = val

		self.projector = UMAP(**conf)

	def __call__(self, vectors):
		return self.projector.fit_transform(vectors)