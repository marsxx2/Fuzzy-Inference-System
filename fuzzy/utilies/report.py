from fuzzy.system.inferece_system import InferenceSystem
from fuzzy.datatype import DataTable
import numpy as np


class MeanSquareError:
    def __init__(self, inference_system, test_tables = None):
        self._inference_system = inference_system
        if test_tables:
            self.test_tables = test_tables
            
    def __call__(self):
        system_mse = [
            sum(
                (actual_output - self._inference_system(inputs)) ** 2
                for inputs, actual_output in data_table
            ) / len(data_table)
            for data_table in self._test_tables
        ]

        return np.mean(system_mse), np.std(system_mse)
    
    @property
    def test_tables(self):
        return self._test_tables
    
    @test_tables.setter
    def test_tables(self, value):
        if isinstance(value, DataTable):
            self._test_tables = [value]
        elif isinstance(value, list):
            if not all(isinstance(val, DataTable) for val in value):
                raise TypeError("All elements in the list must be DataTable class")
            self._test_tables = value
        else:
            raise TypeError("'test_tables' must be DataTable or list of that")