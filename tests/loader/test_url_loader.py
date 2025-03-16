import pytest
import json
from tempfile import NamedTemporaryFile
from unittest.mock import patch, MagicMock, mock_open
from comments2graph.loader.loader import DataLoader

@patch("comments2graph.loader.loader.youtube_backend", return_value=["comment1", "comment2"])
@patch("comments2graph.loader.loader.DataLoader.load_from_file", return_value={"state": "ERROR", "massage": "test"})
def test_url_loader_youtube_api(mock_youtube, mock_cache):
    with NamedTemporaryFile(mode="w+", delete=False) as f:
        json.dump({"youtube_api_key": "test_key"}, f)
        f.seek(0)
        loader = DataLoader(conf_path=f.name)

        with patch("comments2graph.loader.url_tool.URLTool.is_youtube_url", return_value=True):
            result = loader.url_loader("https://youtube.com/watch?v=cl2CPRjUnAQ")
            assert result["state"] == "OK"
            assert len(result["data"]) == 2

@patch("comments2graph.loader.loader.ytdlp_backend", return_value=["comment3"])
@patch("comments2graph.loader.loader.DataLoader.load_from_file", return_value={"state": "ERROR", "massage": "test"})
def test_url_loader_ytdlp(mock_ytdlp, mock_cache):
    with NamedTemporaryFile(mode="w+", delete=False) as f:
        json.dump({"youtube_api_key": ""}, f)
        f.seek(0)
        loader = DataLoader(conf_path=f.name)

        with patch("comments2graph.loader.url_tool.URLTool.is_youtube_url", return_value=True):
            result = loader.url_loader("https://youtube.com/watch?v=cl2CPRjUnAQ")
            assert result["state"] == "OK"
            assert result["data"] == ["comment3"]