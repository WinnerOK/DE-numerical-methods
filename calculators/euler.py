from typing import Optional

from .solution import Solution


class Euler(Solution):
    name = "Euler"

    def get_next(self) -> Optional[float]:
        self.y += self.step * self.calculate(self.x, self.y)
        return self.y
