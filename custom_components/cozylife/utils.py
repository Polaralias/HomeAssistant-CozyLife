import json
import time
import logging
from pathlib import Path
from typing import Optional

_LOGGER = logging.getLogger(__name__)

def get_sn() -> str:
    """
    message sn
    :return: str
    """
    return str(int(round(time.time() * 1000)))

# cache get_pid_list result for many calls
_CACHE_PID = []
_CACHE_PID_PATH: Optional[Path] = None


def get_pid_list(model_path: Path, lang='en') -> list:
    """
    http://doc.doit/project-12/doc-95/
    :param lang:
    :return:
    """
    global _CACHE_PID, _CACHE_PID_PATH
    if len(_CACHE_PID) != 0 and _CACHE_PID_PATH == model_path:
        return _CACHE_PID

    try:
        raw = model_path.read_text(encoding='utf-8')
    except FileNotFoundError:
        _LOGGER.error('Local device model cache not found: %s', model_path)
        return []
    except OSError as err:
        _LOGGER.error('Unable to read local device model cache %s: %s', model_path, err)
        return []

    try:
        pid_list = json.loads(raw)
    except json.JSONDecodeError as err:
        _LOGGER.error('Error decoding local device model cache %s: %s', model_path, err)
        return []

    if isinstance(pid_list, dict):
        info = pid_list.get('info')
        if isinstance(info, dict):
            pid_list = info.get('list')

    if not isinstance(pid_list, list):
        _LOGGER.info('Local device model cache structure is not as expected')
        return []

    _CACHE_PID = pid_list
    _CACHE_PID_PATH = model_path
    return _CACHE_PID
