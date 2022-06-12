"""This is for artificial neural network practice."""
from __future__ import annotations
from random import random
from typing import Callable, List, Optional
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


class Layer:
    def __init__(self,
        previous_layer : Optional[Layer],
        num_neurons : int,
        learning_rate : float,
        activation_function : Callable[[float], float],
        derivative_activation_function : Callable[[float], float],
        ) -> None:
        
        self.previous_layer = previous_layer
        self.neurons : List[Neuron] = []
        
        for i in range(num_neurons):
            if previous_layer is None:
                random_weights : List[float] =[]
            else:
                random_weights = [random() for _ in range(len(previous_layer.neurons))]
            neuron : Neuron = Neuron(random_weights, learning_rate,
                        activation_function, derivative_activation_function)
            self.neurons.append(neuron)
        self.ouput_cache : List[float] = [0.0 for _ in range(num_neurons)]
    
    def output(self, inputs: List[float]) -> List[float]:
        if self.previous_layer is None:
            ## input layer
            self.output_cache = inputs
        else:
            self.output_cache = [n.output(inputs) for n in self.neurons]
        return self.output_cache
