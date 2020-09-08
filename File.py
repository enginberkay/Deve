from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class File:
    name: str
    path: Path
    spoolPath: str = field(init=False)
    file_url: Path = None

    def __post_init__(self):
        self.spoolPath = self.path.with_suffix('.log')
