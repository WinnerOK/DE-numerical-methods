from typing import List, Optional

from .solution import Solution


class ImprovedEuler(Solution):
    name = "I_Euler"

    def get_data(self) -> List[Optional[float]]:
        data = []
        for i in range(self.n + 1):
            data.append(self.y)
            try:
                k1 = self.calculate(self.x, self.y)
                k2 = self.calculate(self.x + self.step, self.y + self.step * k1)

                self.y += self.step * (k1 + k2) / 2
                self.x += self.step
            except:
                data.extend([None] * (self.n - i))
                break

        return data
