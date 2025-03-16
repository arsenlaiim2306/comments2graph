import pytest
from unittest.mock import patch
import logging
from comments2graph.loader.loader import DataLoader

@patch("comments2graph.loader.url_tool.URLTool.is_youtube_url", side_effect=Exception("Test error"))
def test_url_loader_error_logging(mock_ytdlp):
    loader = DataLoader(is_logging=True)
    with patch.object(loader, "logger") as mock_logger:
        result = loader.url_loader("https://invalid.url")
        assert result["state"] == "ERROR"
        mock_logger.error.assert_called_with("Error loading URL https://invalid.url: Test error")