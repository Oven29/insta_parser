from typing import Tuple
import os
from abc import ABC, abstractmethod
from .. import settings
from .. import utils


class WriterBase(ABC):
    extension: str

    def __init__(self, path: str) -> None:
        self.path = path

    @abstractmethod
    def write(self, *values: Tuple[str]) -> None: ...


class TxtWriter(WriterBase):
    extension = 'txt'

    def write(self, *values: Tuple[str]) -> None:
        with open(self.path, 'a', encoding='utf-8') as f:
            f.write(' '.join(values) + '\n')
