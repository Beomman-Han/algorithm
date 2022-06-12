"""This is for artificial neural network practice."""

from typing import Callable, List
from math import exp


def dot_product(
    xs : List[float],
    ys : List[float]
    ) -> float:
    return sum([x * y for x, y in zip(xs, ys)])

def sigmoid(x : float) -> float:
    return 1.0 / (1.0 + exp(-x))

def derivative_sigmoid(x : float) -> float:
    sig : float = sigmoid(x)
    return sig * (1 - sig)


class Neuron:
    def __init__(self,
        weights : List[float],
        learning_rate : float,
        activation_function : Callable[[float], float],
        derivative_activation_function : Callable[[float], float]
        ) -> None:
        
        self.weights = weights
        self.activation_function = activation_function
        self.derivative_activation_function = derivative_activation_function
        self.learning_rate = learning_rate
        self.output_cache = 0.0
        self.delta = 0.0
    
    def output(self, inputs : List[float]) -> float:
        self.output_cache = dot_product(inputs, self.weights)
        return self.activation_function(self.output_cache)