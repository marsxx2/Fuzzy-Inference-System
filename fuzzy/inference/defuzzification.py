from fuzzy.datatype import grade
from fuzzy.inference.consequent import Consequent
from fuzzy.input_space.discourse import Discourse

class Defuzzifier:
    def __call__(self, inferences: list[tuple[Consequent, grade]], *args) -> float:
        self._consequences_output = [itm[0](*args) for itm in inferences]
        self._weigths = [float(itm[1]) for itm in inferences]
        return 0.0


class CoA(Defuzzifier):
    def __init__(self, output_discourse: Discourse):
        self._output_discourse = output_discourse

    def __call__(self, inferences: list[tuple[Consequent, grade]], *args):
        super.__call__(inferences)

        centroids = self._output_discourse.centroids(
            self._consequences_output
        )

        numerator = sum(
            centroid * weight 
            for centroid, weight in zip(centroids, self._weigths)
        )

        return numerator / sum(self._weigths)
        


class Sugeno(Defuzzifier):
    def __call__(self, inferences: list[tuple[Consequent, grade]], *args):
        super().__call__(inferences, *args)

        numerator = sum(
            consout * weight 
            for consout, weight in zip(self._consequences_output, self._weigths)
        )

        return numerator / sum(self._weigths)