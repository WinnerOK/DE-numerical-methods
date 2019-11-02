from abc import ABC, abstractmethod
from typing import Optional, List, Callable


class Solution(ABC):
    def __init__(self, x_0: float, y_0: float, x: float, n: int, func: Callable[[float, Optional[float]], float]):
        self.x = x_0
        self.y = y_0
        self.x_final = x
        self.n = n
        self.step = (x - x_0) / n
        self.func = func

    def calculate(self, x: float, y: float) -> Optional[float]:
        try:
            return self.func(x, y)
        except:  # Catching Arithmetical and Domain errors
            return None

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_next(self) -> Optional[float]:
        raise NotImplementedError

    def get_data(self) -> List[Optional[float]]:
        data = [self.y]
        for i in range(self.n):
            try:
                data.append(self.get_next())
            except:  # if numerical method got itself into None values, it wouldn't be able to calculate further
                data.extend([None] * (self.n - i))
                break
            self.x += self.step
        return data
