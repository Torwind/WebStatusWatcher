"""
Configuration schema validation.
"""

from __future__ import annotations


REQUIRED_SECTIONS = (
    "application",
    "watcher",
    "database",
    "logging",
    "notifications",
    "ui",
)


def validate(config: dict) -> None:
    """
    Validate required top-level sections.
    Raises ValueError if configuration is invalid.
    """

    for section in REQUIRED_SECTIONS:
        if section not in config:
            raise ValueError(
                f"Missing configuration section: {section}"
            )