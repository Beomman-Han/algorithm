"""This is for artificial neural network practice."""
from __future__ import annotations
from functools import reduce
from random import random
from typing import Callable, List, Optional, TypeVar
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
    
    def outputs(self, inputs : List[float]) -> float:
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
    
    def outputs(self, inputs: List[float]) -> List[float]:
        if self.previous_layer is None:
            ## input layer
            self.output_cache = inputs
        else:
            self.output_cache = [n.output(inputs) for n in self.neurons]
        return self.output_cache

    def calculate_deltas_for_output_layer(self,
        expected : List[float]
        ) -> None:
        for n in range(len(self.neurons)):
            self.neurons[n].delta = self.neurons[n].derivative_activation_function(
                self.neurons[n].output_cache) * (expected[n] - self.output_cache[n])
    
    def calculate_deltas_for_hidden_layer(self, next_layer : Layer) -> None:
        for index, neuron in enumerate(self.neurons):
            next_weights : List[float] = [n.weights[index] for n in next_layer.neurons]
            next_deltas : List[float] = [n.delta for n in next_layer.neurons]
            sum_weights_and_deltas : float = dot_product(next_weights, next_deltas)
            neuron.delta = neuron.derivative_activation_function(
                neuron.output_cache) * sum_weights_and_deltas
    

T = TypeVar('T')

class Network:
    def __init__(self,
        layer_structure : List[int],
        learning_rate : float,
        activation_function : Callable[[float], float] = sigmoid,
        derivative_activation_function : Callable[[float], float] = derivative_sigmoid
        ) -> None:
        
        if len(layer_structure) < 3:
            raise ValueError('오류 : 최소 3개 이상의 층이 필요합니다 (입력층, 은닉층, 출력층)!')
        self.layers : List[Layer] = []

        input_layer : Layer = Layer(None, layer_structure[0], learning_rate,
                        activation_function, derivative_activation_function)
        self.layers.append(input_layer)
        
        for previous, num_neurons in enumerate(layer_structure[1::]):
            next_layer = Layer(self.layers[previous], num_neurons, learning_rate,
                        activation_function, derivative_activation_function)
            self.layers.append(next_layer)
    
    def outputs(self, input: List[float]) -> List[float]:
        return reduce(lambda inputs, layer : layer.outputs(inputs), self.layers, input)
    
    def backpropagate(self, expected : List[float]) -> None:
        last_layer : int = len(self.layers) - 1
        self.layers[last_layer].calculate_deltas_for_output_layer(expected)
        for l in range(last_layer - 1, 0, -1):
            self.layers[l].calculate_deltas_for_hidden_layer(self.layers[l + 1])
    
    def update_weights(self) -> None:
        ## backpropagate() method does not update weights in ann.
        ## this method updates weights by delta at each neuron
        for layer in self.layers[1:]:
            for neuron in layer.neurons:
                for w in range(len(neuron.weights)):
                    neuron.weights[w] = neuron.weights[w] + \
                                    (neuron.learning_rate * \
                                    layer.previous_layer.output_cache[w] * \
                                    neuron.delta)
    
    def train(self,
        inputs : List[List[float]],
        expecteds : List[List[float]]
        ) -> None:
        for location, xs in enumerate(inputs):
            ys : List[float] = expecteds[location]
            outs : List[float] = self.outputs(xs)
            self.backpropagate()
            self.update_weights()