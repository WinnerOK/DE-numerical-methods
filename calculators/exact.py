from typing import List, Optional

from .solution import Solution


class Exact(Solution):
    name = "Exact"

    def get_data(self) -> List[Optional[float]]:
        data = []
        for _ in range(self.n):
            try:
                data.append(self.func(self.x))
            except:
                data.append(None)
            self.x += self.step
        return data
