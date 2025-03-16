from sklearn.cluster import KMeans

class ClusteringBackend():
    def __init__(self, config, logger=None):
        self.logger = logger

        # Конфигурация по умолчанию
        conf = {
            "n_clusters": 8,
            "init": "k-means++",
            "n_init": 10,
            "max_iter": 300,
        }

        for key, val in config.items():
            conf[key] = val

        self.kmeans = KMeans(**conf)

    def __call__(self, vectors):
        return self.kmeans.fit_predict(vectors)