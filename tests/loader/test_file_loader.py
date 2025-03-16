import pytest
from unittest.mock import patch, MagicMock, mock_open
from comments2graph.loader.loader import DataLoader

@patch("comments2graph.loader.loader.DataLoader.url_loader", return_value={"status": "OK", "data": "test"})
@patch("os.path.exists", return_value=True)
def test_file_loader(mock_url_loader, mock_file):
    loader = DataLoader()
    with patch("builtins.open", mock_open(read_data='https://youtube.com/watch?v=cl2CPRjUnAQ\nxts.txt\nhttps://youtube.com/watch?v=cl2CPRjUnAQ\nhttps://youtube.com/watch?v=cl2CPRjU')):
        result = loader.path_loader("dummy.txt")
        assert result["state"] == "OK"
        assert len(result["data"]) == 2