from typing import List, Optional

from .solution import Solution


class RungeKutta(Solution):
    name = "Ru-Kh"

    def get_data(self) -> List[Optional[float]]:
        data = []
        for i in range(self.n + 1):
            data.append(self.y)
            try:
                k1 = self.step * self.calculate(self.x, self.y)
                k2 = self.step * self.calculate(
                    self.x + self.step / 2,
                    self.y + k1 / 2
                )
                k3 = self.step * self.calculate(
                    self.x + self.step / 2,
                    self.y + k2 / 2
                )
                k4 = self.step * self.calculate(self.x + self.step, self.y + k3)
                self.y += (k1 + 2 * k2 + 2 * k3 + k4) / 6
                self.x += self.step
            except:
                data.extend([None] * (self.n - i))
                break
        return data
