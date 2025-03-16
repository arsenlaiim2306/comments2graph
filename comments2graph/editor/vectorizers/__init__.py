import importlib

def get_vectorizer(name: str):
    try:
        module = importlib.import_module(f".{name}", package=__package__)
        return module.VectorBackend
        
    except ImportError as e:
        raise ValueError(f"Backend '{name}' not found.") from e
    except AttributeError as e:
        raise ValueError(f"Module '{name}' does not contain a 'VectorBackend' class.") from e