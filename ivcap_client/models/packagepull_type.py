from enum import Enum


class PackagepullType(str, Enum):
    CONFIG = "config"
    LAYER = "layer"
    MANIFEST = "manifest"

    def __str__(self) -> str:
        return str(self.value)
