from gspread import service_account_from_dict
from gspread.spreadsheet import Spreadsheet, Worksheet
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

def get_spreadsheet_client(config_file_path: str = ".streamlit/secrets.toml") -> Spreadsheet | None:
    """
    Get spreadsheet client using service account
    """
    try:
        secrets_config: list[dict[str, str]] = toml.loads(
            Path(config_file_path).read_text(encoding="utf-8")
        )
        if 'connections' in secrets_config and \
            'gsheets' in secrets_config['connections'] and \
            'type' in secrets_config['connections']['gsheets'] and \
            secrets_config['connections']['gsheets']['type'] == 'service_account':
            config = secrets_config['connections']['gsheets']
            client = service_account_from_dict(config)
            spreadsheet = client.open_by_url(config['spreadsheet'])
            return spreadsheet
        else:
            return None
    except (FileNotFoundError, toml.decoder.TomlDecodeError, KeyError):
        logging.info("No config file found")
    return None

def get_worksheet_client(config_file_path: str = ".streamlit/secrets.toml",
                         check_write_perms: bool = True) -> Worksheet | None:
    """
    Get worksheet client using service account
    """
    try:
        secrets_config: list[dict[str, str]] = toml.loads(
            Path(config_file_path).read_text(encoding="utf-8")
        )
        if 'connections' in secrets_config and \
            'gsheets' in secrets_config['connections']:
            config = secrets_config['connections']['gsheets']
            spreadsheet = get_spreadsheet_client()
            if spreadsheet:
                if check_write_perms:
                    permissions = [ p for p in spreadsheet.list_permissions() \
                                if p['emailAddress'] == config['client_email'] ]
                    if len(permissions) > 0:
                        for p in permissions:
                            if p['role'] != 'writer' and \
                                p['deleted'] != False and \
                                p['pendingOwner'] != False:
                                return None
                worksheet = spreadsheet.worksheet(config['worksheet'])
                return worksheet
    except (FileNotFoundError, toml.decoder.TomlDecodeError, KeyError):
        logging.info("No config file found")
    return None

def get_google_sheet_titles_and_url(
        config_file_path: str = ".streamlit/secrets.toml",
        default_title: str | None = "Google Sheet"
) -> tuple[str, str, str] | None:
    """
    Get spreadsheet & worsksheet titles and URL from secrets config file.
    """
    try:
        secrets_config: list[dict[str, str]] = toml.loads(
            Path(config_file_path).read_text(encoding="utf-8")
        )
        if 'connections' in secrets_config and \
            'gsheets' in secrets_config['connections'] and \
            'spreadsheet' in secrets_config['connections']['gsheets']:
            config = secrets_config['connections']['gsheets']
            url = config['spreadsheet']
            spreadsheet = get_spreadsheet_client()
            if spreadsheet:
                s_title = spreadsheet.title
                worksheet = spreadsheet.worksheet(config['worksheet'])
                w_title = worksheet.title
                return s_title, w_title, url
            elif default_title:
                return default_title, '', url
    except (FileNotFoundError, toml.decoder.TomlDecodeError, KeyError):
        logging.info("No config file found")
    return None