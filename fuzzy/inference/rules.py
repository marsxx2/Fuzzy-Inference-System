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

    def __str__(self):
        if self._rules:
            self_str = ''.join(f'{rule}\n' for rule in self._rules)
            return self_str[:-1]
        return self.__repr__()

    def __repr__(self):
        return f'{self.__class__.__name__}()'
    
    def __len__(self):
        return len(self._rules)
    
    def __getitem__(self, index: int):
        return self._rules[index]
    
    def __setitem__(self, index: int, value: Rule):
        self._rules[index] = value

    def __call__(self, grades: list[list[grade]]) -> list[tuple[Consequent, grade]]:
        return [rule(grades) for rule in self._rules]
    
    def append(self, rule: Rule, degree = 0):
        if rule in self._rules:
            self._rules[self._rules.index(rule)].consequent.append(rule.consequent(), degree)
        else:
            self._rules.append(rule)