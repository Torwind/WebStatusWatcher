"""
Configuration manager.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

import yaml


class ConfigManager:
    """
    Loads, creates and saves application configuration.
    """

    def __init__(self, config_dir: Path):
        self._config_dir = config_dir
        self._config_file = config_dir / "config.yaml"
        self._default_file = (
            Path(__file__).parent / "default_config.yaml"
        )

        self._config: dict[str, Any] = {}

        self._ensure_exists()
        self.load()

    def _ensure_exists(self) -> None:
        """
        Create config directory and config.yaml
        from default template.
        """

        self._config_dir.mkdir(parents=True, exist_ok=True)

        if not self._config_file.exists():
            shutil.copy2(self._default_file, self._config_file)

    def load(self) -> None:
        """
        Load YAML configuration.
        """

        with self._config_file.open(
            "r",
            encoding="utf-8",
        ) as file:

            self._config = yaml.safe_load(file) or {}

    def save(self) -> None:
        """
        Save configuration.
        """

        with self._config_file.open(
            "w",
            encoding="utf-8",
        ) as file:

            yaml.safe_dump(
                self._config,
                file,
                allow_unicode=True,
                sort_keys=False,
            )

    @property
    def data(self) -> dict[str, Any]:
        return self._config

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Read value using dotted notation.

        Example:
            watcher.interval
        """

        value = self._config

        for part in key.split("."):

            if not isinstance(value, dict):
                return default

            value = value.get(part)

            if value is None:
                return default

        return value

    def set(
        self,
        key: str,
        value: Any,
        autosave: bool = True,
    ) -> None:
        """
        Set configuration value.
        """

        parts = key.split(".")

        node = self._config

        for part in parts[:-1]:

            if part not in node:
                node[part] = {}

            node = node[part]

        node[parts[-1]] = value

        if autosave:
            self.save()

    def reload(self) -> None:
        """
        Reload configuration.
        """

        self.load()

    def __repr__(self) -> str:
        return (
            f"<ConfigManager file='{self._config_file}'>"
        )