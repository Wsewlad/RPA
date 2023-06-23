# importt RPA modules
from RPA.HTTP import HTTP
# import system modules
import re
import os
from urllib.parse import urlparse

from common.Decorators import step_logger_decorator


def contains_money(title, description) -> bool:
    """Check is `title` or `description` contains any money amounts."""
    pattern = r'\$[\d,.]+|\d+\s?(dollars|USD)'
    text = title
    if description:
        text += ' ' + description
    matches = re.findall(pattern, text)
    if matches:
        return True
    else:
        return False


def get_file_name_from_url(url):
    """Get file name from URL."""
    parsed_url = urlparse(url)
    file_name = os.path.basename(parsed_url.path)
    return file_name


def download_picture(url: str, path: str):
    """Join `path` with file name and download file from given `url`."""
    http = HTTP()
    http.download(
        url=url,
        target_file=os.path.join(path, get_file_name_from_url(url)),
        overwrite=True
    )


def count_query_occurrences(query, title, description) -> int:
    text = title
    if description:
        text += ' ' + description
    return text.count(query)