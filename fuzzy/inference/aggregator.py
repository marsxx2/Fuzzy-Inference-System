from fuzzy.datatype import grade
from fuzzy.inference.consequent import Consequent


class Aggregator:
    def __call__(self, rules_infer: list[tuple[Consequent, grade]]) -> list[tuple[Consequent, grade]]:
        categories: list[Consequent] = []
        grades: list[list[grade]] = []
        for cons, grd in rules_infer:
            if cons in categories:
                indx = categories.index(cons)
                grades[indx].append(grd)
            else:
                categories.append(cons)
                grades.append([grd])

        return [
            (cons, self._aggregate(grds))
            for cons, grds in zip(categories, grades)
        ]


class Max(Aggregator):
    def __call__(self, rules_infer: list[tuple[Consequent, grade]]):
        return super().__call__(rules_infer)

    def _aggregate(self, grades: list[grade]):
        result = grade(0)
        for grd in grades:
            result |= grd
        return result


class Sum(Aggregator):
    def __call__(self, rules_infer: list[tuple[Consequent, grade]]):
        return super().__call__(rules_infer)

    def _aggregate(self, grades: list[grade]):
        result = grade(0)
        for grd in grades:
            result += grd
        return result