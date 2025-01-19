from fuzzy.datatype import grade
from fuzzy.inference.antecedent import Antecedent
from fuzzy.inference.consequent import Consequent


class Rule:
    def __init__(self, antecedent: Antecedent, consequent: Consequent):
        self._antecedent = antecedent
        self._consequent = consequent

    def __str__(self):
        return f'if {self._antecedent} then {self._consequent}'
    
    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self._antecedent)}, {repr(self._consequent)})'
    
    def __eq__(self, other):
        return self.antecedent == other.antecedent
    
    def __call__(self, grades: list[list[grade]]):
        return self._consequent, self._antecedent(grades)
    
    @property
    def antecedent(self):
        return self._antecedent
    
    @property
    def consequent(self):
        return self._consequent
    

class RuleBase():
    def __init__(self):
        self._rules: list[Rule] = []
        self._rules_neighbors: list[list[tuple[Rule, float]]] = []

    def __str__(self):
        if self._rules:
            self_str = ''.join(f'{rule}\n' for rule in self._rules)
            return self_str[:-1]
        return self.__repr__()

    def __repr__(self):
        return f'{self.__class__.__name__}()'
    
    def __len__(self):
        return len(self._rules)
    
    def __getitem__(self, index):
        return self._rules[index], self._rules_neighbors[index]
    
    def __setitem__(self, index, value):
        self._rules[index], self._rules_neighbors[index] = value

    def __call__(self, grades: list[list[grade]]) -> list[tuple[Consequent, grade]]:
        return [rule(grades) for rule in self._rules]
    
    def append(self, rule: Rule, degree = 1):
        if degree > 0:
            if rule in self._rules:
                indx = self._rules.index(rule)
                self._rules_neighbors[indx].append((rule, degree))
                self._rules[indx] = max(self._rules_neighbors[indx], key=lambda x: x[1])[0]
            else:
                self._rules.append(rule)
                self._rules_neighbors.append([(rule, degree)])