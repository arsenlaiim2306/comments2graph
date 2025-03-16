import pytest
from comments2graph.loader.url_tool import URLTool

def test_is_url():
    assert URLTool.is_url("http://example.com") is True
    assert URLTool.is_url("https://youtube.com/watch?v=cl2CPRjUnAQ") is True
    assert URLTool.is_url("/local/path") is False

def test_is_youtube_url():
    valid_urls = [
        "https://youtube.com/watch?v=cl2CPRjUnAQ",
        "http://youtu.be/cl2CPRjUnAQ",
        "https://www.youtube-nocookie.com/embed/cl2CPRjUnAQ"
    ]
    for url in valid_urls:
        print(url, URLTool.is_youtube_url(url))
        assert URLTool.is_youtube_url(url) is True

    assert URLTool.is_youtube_url("http://notyoutube.com/cl2CPRjUnAQ") is False

def test_extract_video_id():
    assert URLTool.extract_video_id("https://youtube.com/watch?v=cl2CPRjUnAQ") == "cl2CPRjUnAQ"
    assert URLTool.extract_video_id("http://youtu.be/cl2CPRjUnAQ") == "cl2CPRjUnAQ"
    with pytest.raises(ValueError):
        URLTool.extract_video_id("invalid_url")