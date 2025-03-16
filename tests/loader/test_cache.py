import pytest
import os
import hashlib
from unittest.mock import patch, mock_open
from comments2graph.loader.loader import DataLoader

def test_url2hash_path():
    loader = DataLoader()
    url = "https://youtube.com/watch?v=cl2CPRjUnAQ"
    expected_hash = hashlib.sha256(url.encode()).hexdigest() + ".pkl.gz"
    assert loader.url2hash_path(url).endswith(expected_hash)

@patch("gzip.open", mock_open())
@patch("os.path.exists", return_value=True)
def test_load_from_file_success(mock_exists):
    loader = DataLoader()
    with patch("pickle.load", return_value={"data": "test"}):
        result = loader.load_from_file("https://test.com")
        assert result["state"] == "OK"

@patch("os.path.exists", return_value=False)
def test_load_from_file_missing(mock_exists):
    loader = DataLoader()
    result = loader.load_from_file("https://test.com")
    assert result["state"] == "ERROR"