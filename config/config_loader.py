import os
import json
from pathlib import Path

def load_config():
    """
    Load configuration from multiple possible locations with fallback support.
    Supports JSON format for better structure and environment variable overrides.
    """
    # Configuration search paths (in order of precedence)
    config_locations = [
        Path("config/settings.json"),
        Path("config/_config.json"),
        Path("config/_config"),
        Path("_config.json"),
        Path("_config")
    ]
    # Environment variable that can override config location
    env_config_path = os.environ.get("CONFIG_PATH")
    if env_config_path:
        config_locations.insert(0, Path(env_config_path))
    
    # Find first available config
    config_data = {}
    config_path = None
    
    for location in config_locations:
        if location.exists():
            config_path = location
            break
    
    if not config_path:
        raise FileNotFoundError(
            "Configuration file not found. Searched: " + 
            ", ".join(str(p) for p in config_locations)
        )
    
    # Load configuration based on file type
    if config_path.suffix == '.json':
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
            # Set environment variables from JSON
            for key, value in config_data.items():
                if isinstance(value, str):
                    os.environ[key] = value
                else:
                    os.environ[key] = json.dumps(value)
    else:
        # Legacy format (key=value)
        with open(config_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    try:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
                    except ValueError:
                        print(f"Warning: Ignoring invalid config line: {line}")
    
    return {
        "config_path": str(config_path),
        "config_format": "json" if config_path.suffix == '.json' else "legacy",
        "loaded_keys": list(config_data.keys()) if config_data else None
    }