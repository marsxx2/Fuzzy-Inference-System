from fuzzy.datatype import grade
import fuzzy.input_space.memberfuncs as mfs
from matplotlib import pyplot as plt
import numpy as np
from fuzzy.input_space import discourse
from fuzzy.inference import antecedent
from fuzzy.inference import consequent
from fuzzy.inference import rules
from fuzzy.inference import aggregator


disX1=discourse.Discourse(
    mfs.Trapezoidal(rhead=-5, rbase=-3.333),
    mfs.Triangular(-5, -3.333, -1.666),
    mfs.Triangular(-3.333, -1.666, 0),
    mfs.Triangular(-1.666, 0, 1.666),
    mfs.Triangular(0, 1.666, 3.333),
    mfs.Triangular(1.666, 3.333, 5),
    mfs.Trapezoidal(3.333, 5)
)

disX2=discourse.Discourse(
    mfs.Trapezoidal(rhead=-5, rbase=-3.333),
    mfs.Triangular(-5, -3.333, -1.666),
    mfs.Triangular(-3.333, -1.666, 0),
    mfs.Triangular(-1.666, 0, 1.666),
    mfs.Triangular(0, 1.666, 3.333),
    mfs.Triangular(1.666, 3.333, 5),
    mfs.Trapezoidal(3.333, 5)
)

dmnInput=discourse.Domain(disX1, disX2)

disOutput=discourse.Discourse(
    mfs.Trapezoidal(rhead=0, rbase=8.333),
    mfs.Triangular(0, 8.333, 16.666),
    mfs.Triangular(8.333, 16.666, 25),
    mfs.Triangular(16.666, 25, 33.333),
    mfs.Triangular(25, 33.333, 41.666),
    mfs.Triangular(33.333, 41.666, 50),
    mfs.Trapezoidal(41.666, 50)
)

rb=rules.RuleBase()
print(rb)
rb.append(rules.Rule(antecedent.Min(4, 6), consequent.Mamdani(3)))
rb.append(rules.Rule(antecedent.Min(3, 1), consequent.Mamdani(0)))
rb.append(rules.Rule(antecedent.Min(5, 6), consequent.Mamdani(3)))
rb.append(rules.Rule(antecedent.Min(2, 5), consequent.Mamdani(6)))
print(rb)
print(rb(dmnInput(3, 4)))
agg=aggregator.Max()
inferences=agg(rb(dmnInput(3, 4)))
print(inferences)
centroids = disOutput.centroids(
    [itm[0]() for itm in inferences]
)
weigths = [float(itm[1]) for itm in inferences]
print(centroids)
print(weigths)

class test:
    def __init__(self, **kwargs):
        if 'length' in kwargs:
            print(f'length = {kwargs['length']}')
        if 'pull' in kwargs:
            print(f'pull = {kwargs['pull']}')
        if 'system' in kwargs:
            print(f'system = {kwargs['system']}')
        

tst=test()

# inputs=[np.linspace(-7, 7, 1000), np.linspace(-7, 7, 1000), np.linspace(-10, 60, 1000)]
# outputs=[np.array([dis(x) for x in input]).T for dis, input in zip(dmnInput, inputs)]
# outputs.append(np.array([disOutput(x) for x in inputs[2]]).T)

# for input, output in zip(inputs, outputs):
#     plt.figure()
#     for mfout in output:
#         plt.plot(input, mfout)
# plt.show()