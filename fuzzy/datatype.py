class grade:
    def __init__(self, value=0):
        self._value = self.__evaluate(value)

    def __evaluate(self, value) -> float:
        value = float(value)
        if value > 1: value = 1.0
        if value < 0: value = 0.0
        return value
    
    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return f'{self.__class__.__name__}({self._value})'

    def __and__(self, other):
        return self.__class__(min(self._value, self.__evaluate(other)))
    
    def __rand__(self, other):
        return self.__and__(other)

    def __iand__(self, other):
        return self.__and__(other)

    def __or__(self, other):
        return self.__class__(max(self._value, self.__evaluate(other)))
    
    def __ror__(self, other):
        return self.__or__(other)

    def __ior__(self, other):
        return self.__or__(other)

    def __add__(self, other):
        other_value = self.__evaluate(other)
        return self.__class__(self._value + other_value - (self._value * other_value))

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        return self.__class__(self._value * self.__evaluate(other))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        return self.__mul__(other)

    def __invert__(self):
        return self.__class__(1 - self._value)

    def __int__(self):
        return int(self._value)

    def __float__(self):
        return self._value
    
    def __eq__(self, other):
        return self._value == self.__evaluate(other)

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        return self._value < self.__evaluate(other)
    
    def __le__(self, other):
        return self._value <= self.__evaluate(other)
    
    def __gt__(self, other):
        return self._value > self.__evaluate(other)
    
    def __ge__(self, other):
        return self._value >= self.__evaluate(other)
    

class DataTable:
    def __init__(self, inputs = None, output = None):
        if inputs:
            self._inputs = inputs
        else:
            self._inputs = []

        if output:
            self._output = output
        else:
            self._output = []

    def __len__(self):
        return min(len(self._inputs), len(self._output))

    def __getitem__(self, index):
        return self._inputs[index], self._output[index]
    
    def __setitem__(self, index, value):
        self._inputs[index], self._output[index] = value

    @property
    def inputs(self):
        return self._inputs
    
    @inputs.setter
    def inputs(self, value):
        self._inputs = value

    @property
    def output(self):
        return self._output
    
    @output.setter
    def output(self, value):
        self._output = value

    def append(self, inputs, output):
        self._inputs.append(inputs)
        self._output.append(output)