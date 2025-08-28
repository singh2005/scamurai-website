from datetime import datetime, timezone
import dateutil.parser

def parse_pubdate(pubdate: str) -> datetime:
    """
    Parse pubDate strings from FTC or IC3 feeds and return ISO 8601 UTC.
    
    Examples:
      - FTC: "August 22, 2025 | 1:17PM"
      - IC3: "Wed, 23 Jul 2025 12:00:00 -04:00"
    """
    pubdate = pubdate.strip()

    try:
        if "|" in pubdate:  
            # FTC format: "August 22, 2025 | 1:17PM"
            dt = datetime.strptime(pubdate, "%B %d, %Y | %I:%M%p")
            # Assume FTC times are in US Eastern Time (they usually are)
            # If no timezone, treat as Eastern and convert to UTC
            from zoneinfo import ZoneInfo
            dt = dt.replace(tzinfo=ZoneInfo("America/New_York"))
        else:
            # IC3 format: "Wed, 23 Jul 2025 12:00:00 -04:00"
            dt = dateutil.parser.parse(pubdate)

        # Convert everything to UTC and return ISO 8601
        return dt.astimezone(timezone.utc)

    except Exception as e:
        raise ValueError(f"Unrecognized pubDate format: {pubdate}") from e
