import pytest
from os import rmdir
import json
from tempfile import NamedTemporaryFile
from comments2graph.loader.loader import DataLoader

def test_load_config_valid():
    with NamedTemporaryFile(mode="w+", delete=False) as f:
        json.dump({"cache_dir": "test_cache", "youtube_api_key": "test_key"}, f)
        f.seek(0)
        loader = DataLoader(conf_path=f.name)
        assert loader.cache_dir == "test_cache"
        assert loader.youtube_api_key == "test_key"

        rmdir("test_cache")