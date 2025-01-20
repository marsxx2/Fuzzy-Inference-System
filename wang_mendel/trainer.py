from fuzzy.datatype import DataTable
from fuzzy.input_space.discourse import Domain, Discourse
from fuzzy.inference.antecedent import Antecedent, Min
from fuzzy.inference.consequent import Mamdani
from fuzzy.inference.rules import RuleBase, Rule
import math

class Trainer:
    _input_domain: Domain
    _output_discourse: Discourse
    _train_table: DataTable

    def __init__(
            self,
            input_domain = None,
            output_discourse = None,
            train_table = None,
            antecedent_type = None
    ):
        if input_domain:
            self.input_domain = input_domain
        if output_discourse:
            self.output_discourse = output_discourse
        if train_table:
            self.train_table = train_table
        if antecedent_type:
            self.antecedent_type = antecedent_type
        else:
            self._antecedent = Min

    @property
    def input_domain(self):
        return self._input_domain
    
    @input_domain.setter
    def input_domain(self, value):
        if not isinstance(value, Domain):
            raise TypeError("'input_domain' must be Domain class")
        self._input_domain = value

    @property
    def output_discourse(self):
        return self._output_discourse
    
    @output_discourse.setter
    def output_discourse(self, value):
        if not isinstance(value, Discourse):
            raise TypeError("'output_discourse' must be Discourse class")
        self._output_discourse = value

    @property
    def train_table(self):
        return self._train_table
    
    @train_table.setter
    def train_table(self, value):
        if not isinstance(value, DataTable):
            raise TypeError("'train_table' must be DataTable class")
        self._train_table = value

    @property
    def antecedent_type(self):
        return self._antecedent
    
    @antecedent_type.setter
    def antecedent_type(self, value):
        if not isinstance(value, type(Antecedent)):
            raise TypeError("'antecedent' must be Antecedent class")
        self._antecedent = value

    def train(self):
        if not self._input_domain:
            raise ValueError("'input_domain' is empty")
        if not self._output_discourse:
            raise ValueError("'output_discourse' is empty")
        if not self._train_table:
            raise ValueError("'train_table' is empty")
        
        rulebase = RuleBase()
        for inputs, output in self.train_table:
            input_domain_result = self._input_domain(inputs)
            output_discourse_result = self._output_discourse(output)
            degree = math.prod(
                float(max(future_result))
                for future_result in input_domain_result
            ) * float(max(output_discourse_result))
            rulebase.append(
                Rule(
                    self._antecedent([
                        future_result.index(max(future_result))
                        for future_result in input_domain_result
                    ]),
                    Mamdani(
                        output_discourse_result.index(
                            max(output_discourse_result)
                        )
                    )
                ),
                degree
            )
        return rulebase