from typing import List, Optional

from .solution import Solution


class ImprovedEuler(Solution):
    name = "I_Euler"

    def get_next(self) -> Optional[float]:
        k1 = self.calculate(self.x, self.y)
        k2 = self.calculate(self.x + self.step, self.y + self.step * k1)

        self.y += self.step * (k1 + k2) / 2

        return self.y
