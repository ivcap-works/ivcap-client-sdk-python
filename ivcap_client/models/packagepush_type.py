from enum import Enum


class PackagepushType(str, Enum):
    CONFIG = "config"
    LAYER = "layer"
    MANIFEST = "manifest"

    def __str__(self) -> str:
        return str(self.value)
