from typing import List, Optional

from .solution import Solution


class Exact(Solution):
    name = "Exact"

    def get_next(self) -> Optional[float]:
        return self.func(self.x + self.step)
