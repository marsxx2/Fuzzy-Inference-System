from fuzzy.datatype import grade


class Consequent:
    def __call__(self, *args) -> int | float:
        pass


class Mamdani(Consequent):
    def __init__(self, consequent = -1):
        self._consequences: list[tuple[int, float]] = []
        self._consequent: int = consequent

    def __str__(self):
        return f'y is SET({self._consequent})'
    
    def __repr__(self):
        if self._consequent != -1:
            return f'{self.__class__.__name__}({self._consequent})'
        return f'{self.__class__.__name__}()'
    
    def __len__(self):
        return len(self._consequences)

    def __getitem__(self, index):
        return self._consequences[index]
    
    def __setitem__(self, index, value):
        self._consequences[index] = value

    def __eq__(self, other):
        if isinstance(other, Mamdani):
            return self.consequent == other.consequent
        elif isinstance(other, int):
            return self.consequent == other
        else:
            raise TypeError("Only can compare with Mamdani class or int")
        
    def __ne__(self, other):
        return not self.__eq__(other)

    def __call__(self, *args):
        return self._consequent

    @property
    def max_degree(self) -> int:
        if self._consequences:
            return max(self._consequences, key=lambda x: x[1])[0]
        return -1
    
    @property
    def consequent(self) -> int:
        return self._consequent
    
    @consequent.setter
    def consequent(self, value: int):
        self._consequent = value
    
    def append(self, consequent: int, degree: float):
        self._consequences.append((consequent, degree))


class Sugeno(Consequent):
    def __init__(self, *args):
        argslen=len(args)
        if argslen == 0:
            raise ValueError("You must pass function coefficients to consequent")
        elif argslen == 1:
            if isinstance(args[0], int) or isinstance(args[0], float):
                self._coefficients = [args[0]]
                self._repr_str= f'{self.__class__.__name__}({args[0]})'
            elif isinstance(args[0], list):
                if not all(isinstance(num, int) or isinstance(num, float) for num in args[0]):
                    raise TypeError("All elements in list must be integer or float")
                self._coefficients = args[0]
                self._repr_str= f'{self.__class__.__name__}({args[0]})'
            else:
                raise TypeError("Argument must be integer or float number or list of those")
        else:
            if not all(isinstance(num, int) or isinstance(num, float) for num in args):
                raise TypeError("All arguments must be integer or float")
            self._coefficients = list(args)
            self._repr_str= f'{self.__class__.__name__}('
            for arg in args:
                self._repr_str += f'{arg}, '
            self._repr_str = self._repr_str[:-2] + ')'

    def __str__(self):
        self_str = ''.join(
            f'{co:+}*x{num + 1} '
            if num != len(self._coefficients) - 1
            else f'{self._coefficients[-1]:+}'
            for num, co in enumerate(self._coefficients)
        )
        self_str = f'y = {self_str[1:]}'
        return self_str

    def __repr__(self):
        return self._repr_str

    def __eq__(self, other):
        return self._coefficients == other
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def __call__(self, *args):
        inputs = self._get_inputs(*args)
        return sum(co * x for co, x in zip(self._coefficients, inputs))
    
    def _get_inputs(self, *args):
        argslen=len(args)
        if argslen == 0:
            if len(self._coefficients) > 1:
                inputs = [0 for _ in range(len(self._coefficients) - 1)]
            else:
                inputs = []
        elif argslen == 1:
            if isinstance(args[0], int) or isinstance(args[0], float):
                if len(self._coefficients) > 2:
                    inputs = [0 for _ in range(len(self._coefficients) - 2)]
                    inputs.append(args[0])
                elif len(self._coefficients) == 1:
                    raise ValueError("Dosen't need any argument")
                else:
                    inputs = [args[0]]
            elif isinstance(args[0], list):
                if len(args[0]) > (len(self._coefficients) - 1):
                    raise ValueError(f"Must pass {len(self._coefficients) - 1} inputs to function")
                if not all(isinstance(num, int) or isinstance(num, float) for num in args[0]):
                    raise TypeError("All elements in list must be integer or float")
                if len(args[0]) < (len(self._coefficients) - 1):
                    inputs = [0 for _ in range(len(self._coefficients) - len(args[0]) - 1)]
                    inputs.extend(args[0])
                else:
                    inputs = args[0]
            else:
                raise TypeError("Argument must be integer or float number or list of those")
        else:
            if len(args) > (len(self._coefficients) - 1):
                raise ValueError(f"Must pass {len(self._coefficients) - 1} inputs to function")
            if not all(isinstance(num, int) or isinstance(num, float) for num in args):
                raise TypeError("All arguments must be integer or float")
            if len(args) < (len(self._coefficients) - 1):
                inputs = [0 for _ in range(len(self._coefficients) - len(args) - 1)]
                inputs.extend(args)
            else:
                inputs = list(args)

        inputs.append(1)
        return inputs
    
    def gradient_descent(self, eta: float, weigth: float, error: float, *args):
        inputs = self._get_inputs(*args)
        self._coefficients = [
            co - eta * weigth * error * x
            for co, x in zip(self._coefficients, inputs)
        ]