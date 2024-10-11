# comments2graph
Analysis of YouTube comments based on the proximity of meanings.

First, you need to enter your youtube api key in the YT_API_KEY variable in the main.py file.
To use the script, after main.py you need to enter the id of the video or playlist or channel or the path to the file with this data.

### Example
python main.py Jesv24I9bXM 1000 - this will download <=1000 video comments and display the result of their analysis.
The same goes for playlists and channels.

python main.py file.list 1000
In the file file.list lines of a similar format:
Jesv24I9bXM 1000
