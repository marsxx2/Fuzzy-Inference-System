from fuzzy.datatype import grade


class Consequent:
    def __init__(self, *args):
        pass

    def __call__(self, *args) -> int | float:
        pass


class Mamdani(Consequent):
    def __init__(self):
        super().__init__()


class Sugeno(Consequent):
    def __init__(self, *args):
        argslen=len(args)
        if argslen == 0:
            raise ValueError("You must pass function coefficients to consequent")
        elif argslen == 1:
            if isinstance(args[0], int) or isinstance(args[0], float):
                self._coefficients = [args[0]]
            elif isinstance(args[0], list):
                if not all(isinstance(num, int) or isinstance(num, float) for num in args[0]):
                    raise TypeError("All elements in list must be integer or float")
                self._coefficients = args[0]
            else:
                raise TypeError("Argument must be integer or float number or list of those")
        else:
            if not all(isinstance(num, int) or isinstance(num, float) for num in args):
                raise TypeError("All arguments must be integer or float")
            self._coefficients = list(args)

    def __call__(self, *args):
        inputs = self._get_inputs(*args)
        return sum(co * x for co, x in zip(self._coefficients, inputs))
    
    def _get_inputs(self, *args):
        argslen=len(args)
        if argslen == 0:
            if len(self._coefficients) > 1:
                raise ValueError(f"Must pass {len(self._coefficients) - 1} inputs to function")
            inputs = []
        elif argslen == 1:
            if isinstance(args[0], int) or isinstance(args[0], float):
                if len(self._coefficients) != 2:
                    raise ValueError(f"Must pass {len(self._coefficients) - 1} inputs to function")
                inputs = [args[0]]
            elif isinstance(args[0], list):
                if len(args[0]) != (len(self._coefficients) - 1):
                    raise ValueError(f"Must pass {len(self._coefficients) - 1} inputs to function")
                if not all(isinstance(num, int) or isinstance(num, float) for num in args[0]):
                    raise TypeError("All elements in list must be integer or float")
                inputs = args[0]
            else:
                raise TypeError("Argument must be integer or float number or list of those")
        else:
            if len(args) != (len(self._coefficients) - 1):
                raise ValueError(f"Must pass {len(self._coefficients) - 1} inputs to function")
            if not all(isinstance(num, int) or isinstance(num, float) for num in args):
                raise TypeError("All arguments must be integer or float")
            inputs = list(args)

        inputs.append(1)
        return inputs
    
    def gradient_descent(self, eta: float, weigth: float, error: float, *args):
        inputs = self._get_inputs(*args)
        self._coefficients = [
            co - eta * weigth * error * x
            for co, x in zip(self._coefficients, inputs)
        ]