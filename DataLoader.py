import math
import requests
import json
from csv import writer as csv_writer
import re
from tqdm import tqdm

youtube_video_api = "https://www.googleapis.com/youtube/v3/commentThreads?key={}&textFormat=plainText&part=snippet&videoId={}&maxResults={}"
youtube_playlist_api = "https://www.googleapis.com/youtube/v3/playlistItems?key={}&part=contentDetails&playlistId={}&maxResults={}"
youtube_channel_api = "https://www.googleapis.com/youtube/v3/channels?key={}&part=contentDetails&id={}"

class DataLoader():
	def __init__(self, youtube_api_key=""):
		self.youtube_api_key = youtube_api_key
	
	def extract_youtube(self, save_file, Id, maxResults=100000):
		if Id[-5:] == ".list":
			self.extract_file(save_file, Id)
		else:
			match len(Id):
				case 11: self.extract_video(save_file, Id, maxResults)
				case 34: self.extract_playlist(save_file, Id, maxResults)
				case 24: self.extract_channel(save_file, Id, maxResults)


	def extract_video(self, save_file, videoId, maxResults):
		get_url = youtube_video_api.format(self.youtube_api_key, videoId, maxResults)

		page_token = ""
		for _ in range(math.ceil(maxResults/100)):
			requests_result = requests.get(get_url+f"&pageToken={page_token}")
			data_json = json.loads(requests_result.text)
			data = [c["snippet"]["topLevelComment"]["snippet"]["textOriginal"] for c in data_json["items"]]

			with open(save_file, "a") as csv_file:
				writer = csv_writer(csv_file)
				if page_token == "":
					writer.writerow(["original", "clear"])

				for d in data:
					res_text = d.replace("\n", " ").split()
					res_text = " ".join(res_text)
					# res_text = " ".join([re.sub(r"^http\S+", "", r) for r in res_text])
					# res_text = re.sub(r"[^A-zА-я0-9 ]", "", res_text)
					res_text = re.sub(r"\s+", " ", res_text)
					res_text = res_text.strip().lower()
					
					writer.writerow([d, res_text])

			if not "nextPageToken" in data_json:
				break
			page_token = data_json["nextPageToken"]

	def extract_playlist(self, save_file, playlistId, maxResults):
		get_url = youtube_playlist_api.format(self.youtube_api_key, playlistId, maxResults)

		pbar = tqdm(total=1, desc=playlistId)

		page_token = ""
		for _ in range(math.ceil(maxResults/50)):
			requests_result = requests.get(get_url+f"&pageToken={page_token}")
			data_json = json.loads(requests_result.text)
			data = [c["contentDetails"]["videoId"] for c in data_json["items"]]

			if page_token == "":
				pbar.reset(total=min(int(data_json["pageInfo"]["totalResults"]), maxResults))

			for d in data:
				self.extract_video(save_file, d, 100000)
				pbar.update()

			if not "nextPageToken" in data_json:
				break
			page_token = data_json["nextPageToken"]

	def extract_channel(self, save_file, Id, maxResults):
		get_url = youtube_channel_api.format(self.youtube_api_key, Id)

		requests_result = requests.get(get_url)
		data_json = json.loads(requests_result.text)

		channel_playlist = data_json["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

		self.extract_playlist(save_file, channel_playlist, maxResults)

	def extract_file(self, save_file, path):
		with open(path, "r") as file:
			lines = file.readlines()
			file.close()

			for line in lines:
				data = line.strip().split()
				chanelId = data[0]

				maxResults = 100000
				if len(data) > 1:
					maxResults = int(data[1])

				self.extract_youtube(save_file, chanelId, maxResults)