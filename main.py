from os import remove
from os.path import exists
from DataLoader import DataLoader
from DataEditor import DataEditor
import plotly.express as px
import textwrap
import sys

YT_API_KEY = ""
comments_path = "comments.csv"

def load():
	if len(sys.argv) >= 2:
		if exists(comments_path):
			remove(comments_path)
				
		loader = DataLoader(YT_API_KEY)
		match len(sys.argv):
			case 2: loader.extract_youtube(comments_path, sys.argv[1])
			case 3: loader.extract_youtube(comments_path, sys.argv[1], int(sys.argv[2]))

def process():
	editor = DataEditor(comments_path)

	texts = ["<br>".join(textwrap.wrap(t, width=70)) for t in editor.get_texts()]

	vectors = editor.get_vectors()
	vectors2d = editor.vec2d(vectors)
	clasterized = editor.clasterize(vectors)

	return (texts, vectors2d, clasterized)

if __name__ == "__main__":
	load()
	texts, vectors2d, clasterized = process()

	data = {
		"x": [],
		"y": [],
		"labels": texts,
		"colors": clasterized
	}
	for vec in vectors2d:
		data["x"].append(vec[0])
		data["y"].append(vec[1])

	fig = px.scatter(data, x='x', y='y', hover_name='labels', color='colors')
	fig.update_layout(title='Комментарии', xaxis_title='Ось X', yaxis_title='Ось Y')
	fig.show()