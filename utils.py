import logging
from pathlib import Path
import toml

def get_worksheet(
        config_file_path: str = ".streamlit/secrets.toml"
) -> str | None:
    """
    Gets worksheet value from secrets config file.
    This is needed to specify a worksheet for service accounts.
    """
    try:
        secrets_config: list[dict[str, str]] = toml.loads(
            Path(config_file_path).read_text(encoding="utf-8")
        )
        if 'connections' in secrets_config and \
            'gsheets' in secrets_config['connections'] and \
            'worksheet' in secrets_config['connections']['gsheets'] and \
            'type' in secrets_config['connections']['gsheets'] and \
            secrets_config['connections']['gsheets']['type'] == 'service_account':
            return secrets_config['connections']['gsheets']['worksheet']
        else:
            return None
    except (FileNotFoundError, toml.decoder.TomlDecodeError, KeyError):
        logging.info("No config file found, continuing without owner color map")
    return None
