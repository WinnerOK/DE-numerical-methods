from typing import List, Optional

from .solution import Solution


class Euler(Solution):
    name = "Euler"

    def get_data(self) -> List[Optional[float]]:
        data = []
        for i in range(self.n + 1):
            data.append(self.y)
            self.x += self.step
            try:
                self.y += self.step * self.calculate(self.x, self.y)
            except:
                data.extend([None] * (self.n - i))
                break
                # return data
        return data
