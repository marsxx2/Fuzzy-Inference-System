from fuzzy.datatype import grade
import math
from enum import Enum


class MemberFunc:
    def __str__(self):
        return f'{self.__class__.__name__}()'
    
    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def __call__(self, value: float) -> grade:
        return grade(0.0)

    @property
    def crossover_point(self) -> float | tuple[float, float]:
        return 0.0, 0.0

    @property
    def centroid(self) -> float:
        return 0.0


class Triangular(MemberFunc):
    def __init__(self, lbase: float, center: float, rbase: float):
        self._lbase: float = lbase
        self._center: float = center
        self._rbase: float = rbase

    def __str__(self):
        return f'{self.__class__.__name__}({self._lbase}, {self._center}, {self._rbase})'
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self._lbase}, {self._center}, {self._rbase})'

    def __call__(self, value: float) -> grade:
        return grade(
            max(
                min(
                    (value - self._lbase) / (self._center - self._lbase),
                    (self._rbase - value) / (self._rbase - self._center)
                ),
                0.0
            )
        )

    @property
    def crossover_point(self) -> tuple[float, float]:
        return (self._center + self._lbase) / 2, (self._center + self._rbase) / 2

    @property
    def centroid(self) -> float:
        return (self._lbase + self._center + self._rbase) / 3


class Trapezoidal(MemberFunc):
    class _Shape(Enum):
        OpenLeft = -1
        close = 0
        OpenRight = 1

    def __init__(self, lbase = None, lhead = None, rhead = None, rbase = None):
        if lbase != None and lhead != None and rhead != None and rbase != None:
            self._shape = self._Shape.close
        elif lbase != None and lhead != None and rhead == None and rbase == None:
            self._shape = self._Shape.OpenRight
        elif lbase == None and lhead == None and rhead != None and rbase != None:
            self._shape = self._Shape.OpenLeft
        else:
            raise ValueError("Please set all arguments or 'lbase' and 'lhead' together or 'rhead' and 'rbase' together")
        
        self._lbase: float = lbase
        self._lhead: float = lhead
        self._rhead: float = rhead
        self._rbase: float = rbase

    def __str__(self):
        if self._shape == self._Shape.close:
            return f'{self.__class__.__name__}({self._lbase}, {self._lhead}, {self._rhead}, {self._rbase})'
        elif self._shape == self._Shape.OpenLeft:
            return f'{self.__class__.__name__}(rhead = {self._rhead}, rbase = {self._rbase})'
        else:
            return f'{self.__class__.__name__}(lbase = {self._lbase}, lhead = {self._lhead})'
    
    def __repr__(self):
        if self._shape == self._Shape.close:
            return f'{self.__class__.__name__}({self._lbase}, {self._lhead}, {self._rhead}, {self._rbase})'
        elif self._shape == self._Shape.OpenLeft:
            return f'{self.__class__.__name__}(rhead = {self._rhead}, rbase = {self._rbase})'
        else:
            return f'{self.__class__.__name__}(lbase = {self._lbase}, lhead = {self._lhead})'

    def __call__(self, value: float) -> grade:
        if self._shape == self._Shape.close:
            return grade(
                max(
                    min(
                        (value - self._lbase) / (self._lhead - self._lbase),
                        1.0,
                        (self._rbase - value) / (self._rbase - self._rhead)
                    ),
                    0.0
                )
            )
        elif self._shape == self._Shape.OpenLeft:
            return grade(
                max(
                    min(
                        1.0,
                        (self._rbase - value) / (self._rbase - self._rhead)
                    ),
                    0.0
                )
            )
        else:
            return grade(
                max(
                    min(
                        (value - self._lbase) / (self._lhead - self._lbase),
                        1.0
                    ),
                    0.0
                )
            )

    @property
    def crossover_point(self) -> float | tuple[float, float]:
        if self._shape == self._Shape.close:
            return (self._lhead + self._lbase) / 2, (self._rhead + self._rbase) / 2
        elif self._shape == self._Shape.OpenLeft:
            return (self._rhead + self._rbase) / 2
        else:
            return (self._lhead + self._lbase) / 2

    @property
    def centroid(self) -> float:
        if self._shape == self._Shape.close:
            return (self._lbase + 2 * self._lhead + 2 * self._rhead + self._rbase) / 6
        elif self._shape == self._Shape.OpenLeft:
            return self._rhead
        else:
            return self._lhead
    

class Gaussian(MemberFunc):
    def __init__(self, center: float, sigma: float):
        self._center: float = center
        self._sigma: float = sigma

    def __str__(self):
        return f'{self.__class__.__name__}({self._center}, {self._sigma})'
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self._center}, {self._sigma})'

    def __call__(self, value: float) -> grade:
        return grade(math.exp(-(value - self._center) ** 2 / (2 * self._sigma ** 2)))

    @property
    def crossover_point(self) -> tuple[float, float]:
        return self._center - 1.17741, self._center + 1.17741

    @property
    def centroid(self) -> float:
        return self._center


class Bell(MemberFunc):
    def __init__(self, center: float, width: float, slope: float):
        self._center: float = center
        self._a: float = width / 2
        self._b: float = 2 * slope * self._a

    def __str__(self):
        return f'{self.__class__.__name__}({self._center}, {self._a * 2}, {self._b / (2 * self._a)})'
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self._center}, {self._a * 2}, {self._b / (2 * self._a)})'

    def __call__(self, value: float) -> grade:
        return grade(1 / (1 + abs((value - self._center) / self._a) ** (2 * self._b)))

    @property
    def center(self):
        return self._center
    
    @center.setter
    def center(self, value):
        self._center = value

    @property
    def width(self):
        return self._a * 2
    
    @width.setter
    def width(self, value):
        self._a = value / 2

    @property
    def slope(self):
        return self._b / (2 * self._a)
    
    @slope.setter
    def slope(self, value):
        self._b = 2 * value * self._a
    
    @property
    def crossover_point(self) -> tuple[float, float]:
        return self._center - self._a, self._center + self._a

    @property
    def centroid(self) -> float:
        return self._center


class Sigmoidal(MemberFunc):
    def __init__(self, a: float, c: float):
        self._a: float = a
        self._c: float = c

    def __call__(self, value: float) -> grade:
        return 1 / (1 + math.exp(-self._a * (value - self._c)))

    @property
    def crossover_point(self) -> float:
        return self._c

    @property
    def centroid(self) -> float:
        return self._c * (1 + self._a) / self._a
