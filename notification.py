from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import datetime
import json

@dataclass
class notification:
    uuid: str
    campaignName: Optional[str] = None
    creator: Optional[str] = None
    to: Optional[str] = None
    from_: Optional[str] = None  # 'from' is a reserved keyword
    creation_date: Optional[int] = None
    user_email: Optional[str] = None
    key: Optional[str] = None
    value: Optional[str] = None
    context: Optional[Dict[str, Any]] = field(default_factory=dict)
    modified_date: Optional[int] = None

    def to_csv_row(self) -> str:
        # Convert to CSV row, handling commas and missing values
        values = [
            self.uuid,
            self.campaignName or "",
            self.creator or "",
            self.to or "",
            self.from_ or "",
            str(self.creation_date or ""),
            self.user_email or "",
            self.key or "",
            self.value or "",
            json.dumps(self.context) if self.context else "",
            str(self.modified_date or "")
        ]
        import csv, io
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(values)
        return output.getvalue().strip()