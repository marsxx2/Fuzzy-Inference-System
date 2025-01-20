from fuzzy.datatype import grade
from fuzzy.datatype import DataTable
from fuzzy.input_space.discourse import Domain
from fuzzy.inference.antecedent import Antecedent
from fuzzy.inference.consequent import Sugeno
from fuzzy.utilies.report import MeanSquareError


class ANFIS:
    _input_domain: Domain
    _antecedents: list[Antecedent]
    _consequents: list[Sugeno]

    def __init__(
            self,
            input_domain = None,
            antecedents = None,
            consequents = None
    ):
        if input_domain:
            self.input_domain = input_domain
        if antecedents:
            self.antecedents = antecedents
        if consequents:
            self.consequents = consequents
        self._norm_weigths = []

    @property
    def input_domain(self):
        return self._input_domain
    
    @input_domain.setter
    def input_domain(self, value):
        if not isinstance(value, Domain):
            raise TypeError("'input_domain' must be Domain class")
        self._input_domain = value

    @property
    def antecedents(self):
        return self._antecedents
    
    @antecedents.setter
    def antecedents(self, value):
        if not isinstance(value, list):
            raise TypeError("'antecedents' must be list of Antecedent class")
        if not all(isinstance(val, Antecedent) for val in value):
            raise TypeError("All elements in list must be Antecedent class")
        self._antecedents = value

    @property
    def consequents(self):
        return self._consequents
    
    @consequents.setter
    def consequents(self, value):
        if not isinstance(value, list):
            raise TypeError("'consequents' must be list of Consequent class")
        if not all(isinstance(val, Sugeno) for val in value):
            raise TypeError("All elements in list must be Sugeno class")
        self._consequents = value

    @property
    def normalized_weigths(self):
        return self._norm_weigths

    def __call__(self, *args):
        if not self._input_domain:
            raise ValueError("'input_domain' is None")
        if not self._antecedents:
            raise ValueError("'antecedents' is None")
        if not self._consequents:
            raise ValueError("'consequents' is None")
        
        input_domain_grades = self._input_domain(*args)
        weigths = self._antecedent_layer(input_domain_grades)
        norm_weigths = self._normalize_layer(weigths)
        return sum(self._consequent_layer(norm_weigths, *args))
        
    def _antecedent_layer(self, grades: list[list[grade]]):
        return [float(ant(grades)) for ant in self.antecedents]
    
    def _normalize_layer(self, weigths: list[float]):
        denominator = sum(weigths)
        self._norm_weigths = [weigth/denominator for weigth in weigths]
        return self._norm_weigths
    
    def _consequent_layer(self, norm_weigths: list[float], *args):
        return [
            norm_weigth * f(*args) 
            for norm_weigth, f in zip(norm_weigths, self._consequents)
        ]
    

def train(anfis_system: ANFIS, eta, epochs_no, train_table: DataTable, test_tables = None):
    train_mse = MeanSquareError(anfis_system, train_table)
    train_mse_list = [train_mse()[0]]
    test_mse_list = []
    if test_tables:
        test_mse = MeanSquareError(anfis_system, test_tables)
        test_mse_list = [test_mse()[0]]
    for _ in range(epochs_no):
        for inputs, output in train_table:
            error = anfis_system(inputs) - output
            for func, norm_weigth in zip(anfis_system.consequents, anfis_system.normalized_weigths):
                func.gradient_descent(eta, norm_weigth, error, inputs)
        train_mse_list.append(train_mse()[0])
        if test_tables:
            test_mse_list.append(test_mse()[0])
    return train_mse_list, test_mse_list