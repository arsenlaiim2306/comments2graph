from os import remove
from os.path import exists
from csv import reader as csv_reader, writer as csv_writer
import numpy as np
import fasttext
import fasttext_pybind
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

class DataEditor():
	def __init__(self, file_path):
		self.file_path = file_path

		lines = []
		with open(file_path, "r") as csv_file:
			reader = csv_reader(csv_file)
			next(reader)

			for row in reader:
				lines.append(row[1])
			
			csv_file.close()

		with open("train.txt", "w") as train_file:
			text = " ".join(lines)
			train_file.write(text)
			train_file.close()

		self.text2vec_model = fasttext.train_unsupervised(input='train.txt', model='skipgram', dim=100, epoch=1000, lr=0.03)
		if exists("train.txt"):
			remove("train.txt")

	def get_texts(self):
		lines = []
		with open(self.file_path, "r") as csv_file:
			reader = csv_reader(csv_file)
			next(reader)

			for row in reader:
				lines.append(row[0])
			
			csv_file.close()

		return lines

	def get_vectors(self):
		lines = []
		with open(self.file_path, "r") as csv_file:
			reader = csv_reader(csv_file)
			next(reader)

			for row in reader:
				lines.append(row[1])
			
			csv_file.close()

		for i, line in enumerate(lines):
			lines[i] = self.text2vec_model[line]

		return lines

	def vec2d(self, vectors):
		vec_dim_model = TSNE(verbose=2, n_components=2, n_iter=1200)

		vectors = np.array(vectors)
		return vec_dim_model.fit_transform(vectors)

	def clasterize(self, vectors):
		clasterizer = KMeans(verbose=1, n_clusters=int(np.ceil(len(vectors)*0.1)))

		clast = clasterizer.fit(vectors)
		return clast.labels_