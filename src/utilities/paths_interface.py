from pathlib import Path


class PathsInterface:
    @property
    def project(self) -> Path:
        raise NotImplementedError

    @property
    def assets(self) -> Path:
        raise NotImplementedError
