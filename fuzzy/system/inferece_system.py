from fuzzy.input_space.discourse import Domain
from fuzzy.inference.rules import RuleBase
from fuzzy.inference.aggregator import Aggregator
from fuzzy.inference.defuzzification import Defuzzifier


class InferenceSystem:
    _input_domain: Domain
    _rulebase: RuleBase
    _aggregator: Aggregator
    _defuzzifier: Defuzzifier

    def __init__(self, **kwargs):
        if 'input_domain' in kwargs:
            if not isinstance(kwargs['input_domain'], Domain):
                raise TypeError("'input_domain' must be Domain class")
            self._input_domain = kwargs['input_domain']
        if 'rulebase' in kwargs:
            if not isinstance(kwargs['rulebase'], RuleBase):
                raise TypeError("'rulebase' must be RuleBase class")
            self._rulebase = kwargs['rulebase']
        if 'aggregator' in kwargs:
            if not isinstance(kwargs['aggregator'], Aggregator):
                raise TypeError("'aggregator' must be Aggregator class")
            self._aggregator = kwargs['aggregator']
        if 'defuzzifier' in kwargs:
            if not isinstance(kwargs['defuzzifier'], Defuzzifier):
                raise TypeError("'defuzzifier' must be Defuzzifier class")
            self._defuzzifier = kwargs['defuzzifier']

    @property
    def input_domain(self):
        return self._input_domain
    
    @input_domain.setter
    def input_domain(self, value):
        if not isinstance(value, Domain):
            raise TypeError("'input_domain' must be Domain class")
        self._input_domain = value

    @property
    def rulebase(self):
        return self._rulebase
    
    @rulebase.setter
    def rulebase(self, value):
        if not isinstance(value, RuleBase):
            raise TypeError("'rulebase' must be RuleBase class")
        self._rulebase = value

    @property
    def aggregator(self):
        return self._aggregator
    
    @aggregator.setter
    def aggregator(self, value):
        if not isinstance(value, Aggregator):
            raise TypeError("'aggregator' must be Aggregator class")
        self._aggregator = value

    @property
    def defuzzifier(self):
        return self._defuzzifier
    
    @defuzzifier.setter
    def defuzzifier(self, value):
        if not isinstance(value, Defuzzifier):
            raise TypeError("'defuzzifier' must be Defuzzifier class")
        self._defuzzifier = value

    def __call__(self, *args):
        if not self._input_domain:
            raise ValueError("'input_domain' is None")
        if not self._rulebase:
            raise ValueError("'rulebase' is None")
        if not self._aggregator:
            raise ValueError("'aggregator' is None")
        if not self._defuzzifier:
            raise ValueError("'defuzzifier' is None")
        
        input_domain_grades = self._input_domain(*args)
        ruls_inference = self._rulebase(input_domain_grades)
        aggrigated_inferece = self._aggregator(ruls_inference)
        return self._defuzzifier(aggrigated_inferece, *args)