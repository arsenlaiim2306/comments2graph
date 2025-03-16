from sklearn.cluster import DBSCAN

class ClusteringBackend():
	def __init__(self, config, logger=None):
		self.logger = logger

		conf = {
			"eps": 0.38,
			"min_samples": 2,
			"n_jobs": -1
		}
		for key, val in config.items():
			conf[key] = val

		self.dbscan = DBSCAN(**conf)

	def __call__(self, vectors):
		return self.dbscan.fit_predict(vectors)