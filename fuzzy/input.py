import fuzzy.memberfuncs as mfs
from fuzzy.datatype import grade

class Discorse:
    def __init__(self, *args):
        argslen=len(args)
        if argslen == 0:
            self._member_functions: list[mfs.MemberFunc] = []
        elif argslen == 1:
            if isinstance(args[0], int):
                if args[0]<0:
                    raise ValueError("Length must be a non_negative integer")
                self._member_functions = [mfs.MemberFunc() for _ in range(args[0])]
            elif isinstance(args[0], list):
                if not all(isinstance(itm, mfs.MemberFunc) for itm in args[0]):
                    raise ValueError("All elements in list must be a MemberFunc classes")
                self._member_functions=args[0]
            else:
                raise ValueError("Argument must be a non_negative integer or a list of MemberFunc classes")

        else:
            if not all(isinstance(itm, mfs.MemberFunc) for itm in args):
                raise ValueError("All arguments must be a MemberFunc classes")
            self._member_functions=list(args)

    def __str__(self):
        return str(self._member_functions)
    
    def __len__(self):
        return len(self._member_functions)

    def __call__(self, value: float) -> list[grade]:
        return [mf(value) for mf in self._member_functions]
    
    def __getitem__(self, index):
        return self._member_functions[index]
    
    def __setitem__(self, index, value):
        self._member_functions[index] = value

    @property
    def crossover_points(self):
        return [mf.crossover_point for mf in self._member_functions]

    @property
    def centroids(self):
        return [mf.centroid for mf in self._member_functions]


class SetManager:
    def __init__(self, feature_count):
        self._sets: list[Discorse] = [Discorse() for _ in range(feature_count)]

    @property
    def sets(self):
        return self._sets

    def get_grades_list(self, x_list: list[float]) -> list[list[float]]:
        return [set_obj.get_grades(x) for set_obj, x in zip(self._sets, x_list)]
