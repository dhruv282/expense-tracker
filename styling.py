import logging
from pathlib import Path
import toml

def get_owner_color_map(
        config_file_path: str = ".streamlit/expense_tracker_config.toml"
    ) -> (dict[str, str] | None):
    try:
        owner_config: list[dict[str, str]] = toml.loads(
            Path(config_file_path).read_text(encoding="utf-8")
        )['owners']
        if len(owner_config) > 0:
            owner_color_map: dict[str, str] = {}
            for owner in owner_config:
                owner_color_map[owner['name']] = owner['color']
            return owner_color_map
        else:
            return None
    except (FileNotFoundError, toml.decoder.TomlDecodeError, KeyError):
        logging.info("No config file found, continuing without owner color map")
    return None

category_color_map = {
    "Income": "#7cfc00",
    "Savings": "#7cfc00",
    "Investments": "#008000",
    "Personal Care": "#7fffd4",
    "Housing": "#00ced1",
    "Internet": "#00bfff",
    "Travel": "#4169e1",
    "Car": "#9932cc",
    "Health & Fitness": "#da70d6",
    "Grocery": "#ff69b4",
    "Shopping": "#c71585",
    "Phone": "#dc143c",
    "Taxes": "#ff4500",
    "Utility": "#ffa500",
    "Entertainment": "#ffff00",
    "Dining": "#ffe4e1",
    "Petrol": "#b8860b",
    "Other": "#ffffff",
}

payment_method_color_map = {
    "Credit": "#bfe1f6",
    "Check": "#ffe5a0",
    "Cash": "#d4edbc",
}

payment_method_label_prefix = {
    "Credit": "💳",
    "Check": "✉️",
    "Cash": "💵",
}
