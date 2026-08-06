from dataclasses import dataclass


@dataclass(slots=True)
class Site:

    id: int

    name: str

    url: str

    enabled: bool

    interval_seconds: int