from fuzzy.datatype import grade


class Antecedent:
    def __init__(self, *args):
        argslen = len(args)
        if argslen == 0:
            raise ValueError("You must pass fuzzy set numbers to antecedent")
        elif argslen == 1:
            if not isinstance(args[0], list):
                raise ValueError("Argument must be a list of ints")
            if not all(isinstance(val , int) for val in args[0]):
                raise TypeError("All elements in list must be int")
            self._fuzzy_set_numbers=args[0]
        else:
            if not all(isinstance(val , int) for val in args):
                raise TypeError("All arguments must be int")
            self._fuzzy_set_numbers=list(args)

    def __call__(self, grades: list[list[grade]]):
        self._antecedent_grades = [
            grades[discourse_number][set_number]
            for discourse_number, set_number in enumerate(self._fuzzy_set_numbers)
            if set_number >= 0
        ]
        print(self._antecedent_grades)
        return grade(0)


class Min(Antecedent):
    def __init__(self, *args):
        super().__init__(*args)

    def __call__(self, grades: list[list[grade]]):
        super().__call__(grades)
        result=grade(1)
        for grd in self._antecedent_grades:
            result &= grd
        return result


class Product(Antecedent):
    def __init__(self, *args):
        super().__init__(*args)

    def __call__(self, grades: list[list[grade]]):
        super().__call__(grades)
        result=grade(1)
        for grd in self._antecedent_grades:
            result *= grd
        return result