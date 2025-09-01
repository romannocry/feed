"""
Generator function's goal is to take a json payload and generate a html table widget that will be embedded in emails:
hardcoded:
receiver's web page: https://loop.email/receiver
receiver's function: https://lambdda/receiver

Payload:
{
    "redirect": "", // default blank
    "input": [] // list of input strings
    "style": "horizontal|vertical", // default horizontal
    "triggerOnSuccess":{
        "api":"https://api/triggerWorkflow", // default url
        "method":"GET|POST", // default POST
        "params":{
        } // key value pairs to be sent as query params or form data
    },
    "storage": "https://storage.url" // default null

}

Example payload:
{
    "redirect": "https//www.google.com", 
    "input": ["yes","no"] // list of input strings
    "style": "horizontal", // default horizontal
    "triggerOnSuccess":{
        "api":"https://api/triggerWorkflow", // default url
        "method":"POST", // default POST
        "params":{
            "userId":"123",
            "ledgerId":"456"
            "answer":"{{input}}" // input will be replaced by the actual input value
        } // key value pairs to be sent as query params or form data
    },
    "storage": "https://lambda/db/123" // default null
}

Example output
<table>
<tr>
<td><a href="https://loop.email/receiver/{b64payload}"></td> //yes
<td><a href="https://loop.email/receiver/{b64payload}"></td> //no
</tr>
</table>

What happens when user clicks on yes:
1. user is redirected to https://loop.email/receiver/{b64payload}
2. receiver function decodes b64payload
3. receiver function stores the input in the storage url if provided
4. receiver function redirects user to redirect url if provided
5. receiver function triggers the api with the params if provided
6. user lands on the redirect url
"""

import json
import base64
from typing import List, Dict, Any

__all__ = ["generate_actions_table"]
receiver_url = "https://loop.email/receiver"

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
        print(f"Processing option: {option}")
        # Merge shared_settings with option (option keys take precedence)
        option_settings = dict(default_settings)
        option_settings.update(option)
        print(f"Merged settings: {option_settings}")
        print(f"Context for placeholders: {dict(context)}")
        # Fill placeholders in the merged option
        option_settings_filled = fill_placeholders(option_settings, dict(context))
        print(f"Filled option: {option_settings_filled}")
        # Build payload
        payload = {
            "uuid": uuid,
            "validators": validators,
            "label": option_settings_filled.get("label"),
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
        link = f'<a href="{receiver_url}/{b64payload}">{option_settings_filled.get("label")}</a>'
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