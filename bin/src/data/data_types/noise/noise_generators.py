"""
This file contains noise generators classes for generating various types of noise.
"""

from abc import ABC, abstractmethod
from typing import Any
import numpy as np
import multiprocessing as mp

class AbstractNoiseGenerator(ABC):
    """
    Abstract class for noise generators. 
    All noise function should have the seed in it. Because the multiprocessing of them could unset the seed in short.
    """

    def __init__(self):
        pass

    @abstractmethod
    def add_noise(self, data: Any, seed: float = None) -> Any:
        """
        Adds noise to the data.  
        They should have the following line
        """
        #  np.random.seed(seed)
        raise NotImplementedError
    
    def add_noise_multiprocess(self, data: list, seed: float = None) -> list:
        """
        Adds noise to the data using multiprocessing.
        """
        with mp.Pool(mp.cpu_count()) as pool:
            # reshaping the inputs of this function to meet starmap requirements, basically adding into a tuple the list[elem] + seed
            function_specific_input = [(item, seed) for item in data]
            return pool.starmap(self.add_noise, function_specific_input)
        

class UniformTextMasker(AbstractNoiseGenerator):
    """
    This noise generators replace characters with 'N' with a given probability.
    """

    def __init__(self, probability: float = 0.1) -> None:
        self.probability = probability


    def add_noise(self, data: str, seed: float = None) -> str:
        """
        Adds noise to the data.
        """

        np.random.seed(seed)
        return ''.join([c if np.random.rand() > self.probability else 'N' for c in data])
    
class GaussianNoise(AbstractNoiseGenerator):
    """
    This noise generator adds gaussian noise to float values
    """

    def __init__(self, mean: float = 0, std: float = 1) -> None:
        self.mean = mean
        self.std = std

    def add_noise(self, data: float, seed: float = None) -> float:
        """
        Adds noise to a single point of data.
        """

        np.random.seed(seed)
        return data + np.random.normal(self.mean, self.std)
    
    def add_noise_multiprocess(self, data: list, seed: float = None) -> list:
        """
        Adds noise to the data using np arrays
        """

        np.random.seed(seed)
        return list(np.array(data) + np.random.normal(self.mean, self.std, len(data)))