
from matplotlib import pyplot as plt
import numpy as np
import fuzzy.input_space.memberfuncs as mfs
from fuzzy.input_space import discourse
from fuzzy.inference import aggregator
from fuzzy.inference import defuzzification
from fuzzy.system.inferece_system import InferenceSystem
from fuzzy.datatype import DataTable
import wang_mendel.trainer


fuzzy_system = InferenceSystem(
    input_domain = discourse.Domain(
        discourse.Discourse(
            mfs.Trapezoidal(rhead=-5, rbase=-3.333),
            mfs.Triangular(-5, -3.333, -1.666),
            mfs.Triangular(-3.333, -1.666, 0),
            mfs.Triangular(-1.666, 0, 1.666),
            mfs.Triangular(0, 1.666, 3.333),
            mfs.Triangular(1.666, 3.333, 5),
            mfs.Trapezoidal(3.333, 5)
        ),
        discourse.Discourse(
            mfs.Trapezoidal(rhead=-5, rbase=-3.333),
            mfs.Triangular(-5, -3.333, -1.666),
            mfs.Triangular(-3.333, -1.666, 0),
            mfs.Triangular(-1.666, 0, 1.666),
            mfs.Triangular(0, 1.666, 3.333),
            mfs.Triangular(1.666, 3.333, 5),
            mfs.Trapezoidal(3.333, 5)
        )
    ),
    aggregator = aggregator.Max(),
    defuzzifier = defuzzification.CoA(
        discourse.Discourse(
            mfs.Trapezoidal(rhead=0, rbase=8.333),
            mfs.Triangular(0, 8.333, 16.666),
            mfs.Triangular(8.333, 16.666, 25),
            mfs.Triangular(16.666, 25, 33.333),
            mfs.Triangular(25, 33.333, 41.666),
            mfs.Triangular(33.333, 41.666, 50),
            mfs.Trapezoidal(41.666, 50)
        )
    )
)

input_range = np.linspace(-5, 5, 41).tolist()
train_data = DataTable()
train_data.inputs = [
    [x1, x2]
    for x1 in input_range
    for x2 in input_range
]
train_data.output = [
    x1 ** 2 + x2 ** 2
    for x1, x2 in train_data.inputs
]

trainer = wang_mendel.trainer.Trainer(
    input_domain = fuzzy_system.input_domain,
    output_discourse = fuzzy_system.defuzzifier.output_discourse,
    train_table = train_data
)

fuzzy_system.rulebase = trainer.train()

set_names = ['INPUT SET 1', 'INPUT SET 2', 'OUTPUT SET']
inputs=[np.linspace(-7, 7, 1000), np.linspace(-7, 7, 1000), np.linspace(-10, 60, 1000)]
outputs=[np.array([dis(x) for x in input]).T for dis, input in zip(fuzzy_system.input_domain, inputs)]
outputs.append(np.array([fuzzy_system.defuzzifier.output_discourse(x) for x in inputs[2]]).T)

for input, output, name in zip(inputs, outputs, set_names):
    plt.figure(figsize=(8,5))
    for mfout in output:
        plt.plot(input, mfout)
    plt.title = name

plt.show()