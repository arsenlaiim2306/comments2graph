import logging
from logging.handlers import RotatingFileHandler
import argparse

from .storage import DataStorage
from .loader import DataLoader
from .editor import DataEditor
from .visualizer import DataVisualizer


def get_logger(name, path, level, max_size=10485760):
	logger = logging.getLogger()
	logger.setLevel(level)

	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

	file_handler = RotatingFileHandler(path, maxBytes=max_size, backupCount=1)
	file_handler.setLevel(level)
	file_handler.setFormatter(formatter)

	logger.addHandler(file_handler)


def main(args):
	logger = get_logger(__name__, args.log, logging.ERROR)
	data_storage = DataStorage(args.db_path, args.db_new)

	data_loader = DataLoader(args.loader, args.config, logger=logger)
	data_loader(args.data, data_storage)

	data_editor = DataEditor(args.vectorizer, args.clusterizer, args.projectors, args.config, logger=logger)
	texts, vectors, clasters = data_editor(data_storage, args.new_vectors)

	data_visualizer = DataVisualizer(args.visualizer, logger)
	data_visualizer(texts, vectors, clasters, args.dark_theme)

	if args.save_type:
		data_visualizer.save(args.save_type, args.save_path)
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="comments2graph")
	parser.add_argument("data", help="url or file path")
	parser.add_argument("--config", default="config.json", help="config path")
	parser.add_argument("--log", default="main.log", help="log file path")
	parser.add_argument("--db_path", default="data.db", help="database file path")
	parser.add_argument("--db_new", default=False, action="store_true", help="rewrite database")

	parser.add_argument("-l", "--loader", default="ytdlp", help="'ytdlp' or 'youtube_api'")

	parser.add_argument("-v", "--vectorizer", default="sentence", help="only 'sentence'")
	parser.add_argument("-c", "--clusterizer", default="dbscan", help="'dbscan' or 'kmeans'")
	parser.add_argument("-p", "--projectors", default="umap", help="only 'umap'")
	parser.add_argument("--new_vectors", default=False, action="store_true", help="rewrite database vectors")

	parser.add_argument("-g", "--visualizer", default="plotly", help="only 'plotly'")
	parser.add_argument("--dark_theme", action="store_true", help="dark theme")

	parser.add_argument("--save_type", default="", help="'' or 'html' or 'image'")
	parser.add_argument("--save_path", default="visualize.html", help="save path")


	args = parser.parse_args()

	main(args)