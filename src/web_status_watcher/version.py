"""
Application version information.
"""

APP_NAME = "WebStatusWatcher"

VERSION_MAJOR = 0
VERSION_MINOR = 3
VERSION_PATCH = 2

VERSION = (
    f"{VERSION_MAJOR}."
    f"{VERSION_MINOR}."
    f"{VERSION_PATCH}"
)


def full_version() -> str:
    """
    Return application name with version.
    """

    return (
        f"{APP_NAME} "
        f"v{VERSION}"
    )