"""
Version information.
"""

APP_NAME = "WebStatusWatcher"

VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 0

VERSION = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"


def full_version() -> str:
    return f"{APP_NAME} v{VERSION}"