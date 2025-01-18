from fuzzy.datatype import grade


class Antecedent:
    def __init__(self, *args):
        argslen = len(args)
        if argslen == 0:
            raise ValueError("You must pass fuzzy set numbers to antecedent")
        elif argslen == 1:
            if isinstance(args[0], int):
                self._fuzzy_set_numbers=[args[0]]
                self._repr_str= f'({args[0]})'
            elif isinstance(args[0], list) or isinstance(args[0], tuple):
                if not all(isinstance(val , int) for val in args[0]):
                    raise TypeError("All elements in list must be int")
                self._fuzzy_set_numbers=args[0]
                self._repr_str= f'({args[0]})'
            else:
                raise TypeError("Argument must be integer or a list of ints")
        else:
            if not all(isinstance(val , int) for val in args):
                raise TypeError("All arguments must be int")
            self._fuzzy_set_numbers=list(args)
            self._repr_str= '('
            for arg in args:
                self._repr_str += f'{arg}, '
            self._repr_str = self._repr_str[:-2] + ')'

    def __str__(self):
        self_str = ''.join(
            f'x{discourse_number + 1} is SET({set_number}) and '
            for discourse_number, set_number in enumerate(self._fuzzy_set_numbers)
            if set_number >= 0
        )

        return self_str[:-5]
    
    def __repr__(self):
        return f'{self.__class__.__name__}{self._repr_str}'
    
    def __eq__(self, other):
        return self._fuzzy_set_numbers == other._fuzzy_set_numbers

    def __call__(self, grades: list[list[grade]]):
        self._antecedent_grades = [
            grades[discourse_number][set_number]
            for discourse_number, set_number in enumerate(self._fuzzy_set_numbers)
            if set_number >= 0
        ]
        
        return grade(0)


class Min(Antecedent):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return f'{self.__class__.__name__}{self._repr_str}'
    
    def __eq__(self, other):
        return super().__eq__(other)

    def __call__(self, grades: list[list[grade]]):
        super().__call__(grades)
        result=grade(1)
        for grd in self._antecedent_grades:
            result &= grd
        return result


class Product(Antecedent):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return f'{self.__class__.__name__}{self._repr_str}'
    
    def __eq__(self, other):
        return super().__eq__(other)

    def __call__(self, grades: list[list[grade]]):
        super().__call__(grades)
        result=grade(1)
        for grd in self._antecedent_grades:
            result *= grd
        return result