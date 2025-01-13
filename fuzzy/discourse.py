import fuzzy.memberfuncs as mfs
from fuzzy.datatype import grade
from concurrent.futures import ThreadPoolExecutor


class Discourse:
    def __init__(self, *args):
        argslen = len(args)
        if argslen == 0:
            self._member_functions: list[mfs.MemberFunc] = []
            self._repr_str = f'{self.__class__.__name__}()'
        elif argslen == 1:
            if isinstance(args[0], int):
                if args[0]<0:
                    raise ValueError("Length must be a non_negative integer")
                self._member_functions = [mfs.MemberFunc() for _ in range(args[0])]
                self._repr_str = f'{self.__class__.__name__}({args[0]})'
            elif isinstance(args[0], list):
                if not all(isinstance(itm, mfs.MemberFunc) for itm in args[0]):
                    raise ValueError("All elements in list must be a MemberFunc classes")
                self._member_functions = args[0]
                self._repr_str = f'{self.__class__.__name__}({str(args[0])})'
            else:
                raise ValueError("Argument must be a non_negative integer or a list of MemberFunc classes")

        else:
            if not all(isinstance(itm, mfs.MemberFunc) for itm in args):
                raise ValueError("All arguments must be a MemberFunc classes")
            self._member_functions = list(args)
            self._repr_str = f'{self.__class__.__name__}('
            for a in args:
                self._repr_str += f'{a}, '
            self._repr_str = self._repr_str[:-2] + ')'

    def __str__(self):
        return str(self._member_functions)
    
    def __repr__(self):
        return self._repr_str
    
    def __len__(self):
        return len(self._member_functions)

    def __call__(self, value: float) -> list[grade]:
        # return [mf(value) for mf in self._member_functions]
        with ThreadPoolExecutor() as executor:
            futures=[executor.submit(mf, value) for mf in self._member_functions]
            results=[future.result() for future in futures]

        return list(results)
    
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
    
    def append(self, member_func: mfs.MemberFunc):
        self._member_functions.append(member_func)


class Domain:
    def __init__(self, *args):
        argslen = len(args)
        if argslen == 0:
            self._discourses: list[Discourse] = []
            self._repr_str = f'{self.__class__.__name__}()'
        elif argslen == 1:
            if isinstance(args[0], int):
                if args[0]<0:
                    raise ValueError("Length must be a non_negative integer")
                self._discourses = [Discourse() for _ in range(args[0])]
                self._repr_str = f'{self.__class__.__name__}({args[0]})'
            elif isinstance(args[0], list):
                if not all(isinstance(itm, Discourse) for itm in args[0]):
                    raise ValueError("All elements in list must be a Discourse class")
                self._discourses = args[0]
                self._repr_str = f'{self.__class__.__name__}({str(args[0])})'
            else:
                raise ValueError("Argument must be a non_negative integer or a list of Discourse classes")

        else:
            if not all(isinstance(itm, Discourse) for itm in args):
                raise ValueError("All arguments must be a Discourse class")
            self._discourses = list(args)
            self._repr_str = f'{self.__class__.__name__}('
            for a in args:
                self._repr_str += f'{a}, '
            self._repr_str = self._repr_str[:-2] + ')'

    def __str__(self):
        return str(self._discourses)
    
    def __repr__(self):
        return self._repr_str
    
    def __len__(self):
        return len(self._discourses)

    def __call__(self, *args) -> list[list[grade]]:
        argslen = len(args)
        if argslen == 0:
            raise ValueError(f"You must pass {len(self)} futures to domain")
        elif argslen == 1:
            if not all(isinstance(val, float) or isinstance(val , int) for val in args[0]):
                raise ValueError("All elements in list must be a float or int")
            if len(args[0]) != len(self):
                raise ValueError(f"You must pass {len(self)} futures to domain but you passed {len(args[0])} futures")
            futures=args[0]
        else:
            if not all(isinstance(val, float) or isinstance(val , int) for val in args):
                raise ValueError("All arguments must be a float or int")
            if len(args) != len(self):
                raise ValueError(f"You must pass {len(self)} futures to domain but you passed {len(args)} futures")
            futures=list(args)

        # return [dis(value) for dis, value in zip(self._discourses, futures)]
        with ThreadPoolExecutor() as executor:
            futures=[executor.submit(dis, value) for dis, value in zip(self._discourses, futures)]
            results=[future.result() for future in futures]

        return list(results)
    
    def __getitem__(self, index):
        return self._discourses[index]
    
    def __setitem__(self, index, value):
        self._discourses[index] = value

    def append(self, member_func: mfs.MemberFunc):
        self._discourses.append(member_func)
