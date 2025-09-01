# generator.py
from config import RECEIVER_DECODE_UI, RECEIVER_DECODE_FUNCTION, BASE_DB
import json
import base64
from typing import List, Dict, Any

__all__ = ["generate_actions_table"]

def fill_placeholders(obj, context):
    """Recursively replace {{...}} placeholders in obj using context dict."""
    if isinstance(obj, dict):
        return {k: fill_placeholders(v, context) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [fill_placeholders(i, context) for i in obj]
    elif isinstance(obj, str):
        # Replace all {{key}} or {{key.subkey}} with values from context
        import re
        def replacer(match):
            expr = match.group(1)
            parts = expr.split('.')
            val = context
            for part in parts:
                val = val.get(part, f"{{{{{expr}}}}}") if isinstance(val, dict) else f"{{{{{expr}}}}}"
            return str(val)
        return re.sub(r"\{\{([^}]+)\}\}", replacer, obj)
    else:
        return obj

def generate_actions_table(
    uuid: str,
    validators: str,
    default_settings: Dict[str, Any],
    options: List[Dict[str, Any]],
    context: Dict[str, Any],
    table_orientation: str = None,
) -> str:
    """
    Generates an HTML table with links for each option.
    Each link contains a base64-encoded payload with placeholders filled from params and merged settings.
    default_settings: dict of defaults applied to all options unless overridden in the option.
    """
    
    cells = []

    for option in options:
        #print(f"Processing option: {option}")
        # Merge shared_settings with option (option keys take precedence)
        option_settings = dict(default_settings)
        option_settings.update(option)
        #print(f"Merged settings: {option_settings}")
        #print(f"Context for placeholders: {dict(context)}")
        # Fill placeholders in the merged option
        option_settings_filled = fill_placeholders(option_settings, dict(context))
        #print(f"Filled option: {option_settings_filled}")
        # Build payload
        payload = {
            "uuid": uuid,
            "validators": validators,
            "key": option_settings_filled.get("key"),
            "value": option_settings_filled.get("value"),
            "context": context,
            "triggerOnSuccess": option_settings_filled.get("triggerOnSuccess", {}),
            "storage": option_settings_filled.get("storage"),
            "redirect": option_settings_filled.get("redirect"),
        }
        # Remove None values for cleaner payload
        payload = {k: v for k, v in payload.items() if v is not None}
        # Encode payload
        b64payload = base64.urlsafe_b64encode(
            json.dumps(payload).encode("utf-8")
        ).decode("utf-8")
        link = f'<a href="{RECEIVER_DECODE_UI}/{b64payload}">{option_settings_filled.get("value")}</a>'
        cells.append(f"<td>{link}</td>")

    # Use style from shared_settings unless overridden
    if table_orientation == "vertical":
        rows = "\n".join(f"<tr>{cell}</tr>" for cell in cells)
        table = f"<table>\n{rows}\n</table>"
    else:
        row = "".join(cells)
        table = f"<table>\n<tr>{row}</tr>\n</table>"
    
    print(table)
    return table