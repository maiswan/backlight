from enum import Enum, auto
import math

class EasingMode(Enum):
    LINEAR = "linear"

    IN_SINE = "in_sine"
    OUT_SINE = "out_sine"
    IN_OUT_SINE = "in_out_sine"

    IN_QUAD = "in_quad"
    OUT_QUAD = "out_quad"
    IN_OUT_QUAD = "in_out_quad"

    IN_CUBIC = "in_cubic"
    OUT_CUBIC = "out_cubic"
    IN_OUT_CUBIC = "in_out_cubic"

    IN_QUART = "in_quart"
    OUT_QUART = "out_quart"
    IN_OUT_QUART = "in_out_quart"

    IN_QUINT = "in_quint"
    OUT_QUINT = "out_quint"
    IN_OUT_QUINT = "in_out_quint"

    IN_EXPO = "in_expo"
    OUT_EXPO = "out_expo"
    IN_OUT_EXPO = "in_out_expo"

    IN_CIRC = "in_circ"
    OUT_CIRC = "out_circ"
    IN_OUT_CIRC = "in_out_circ"


class Transitioner:

    @staticmethod
    def transit(
        old_buffer: list[tuple[float, float, float]] | list[tuple[float, float, float, float]], 
        new_buffer: list[tuple[float, float, float]] | list[tuple[float, float, float, float]],
        progress: float,
        mode: EasingMode
    ):
        ease_modes = {
            EasingMode.LINEAR: Transitioner.ease_linear,
            EasingMode.IN_SINE: Transitioner.ease_in_sine,
            EasingMode.OUT_SINE: Transitioner.ease_out_sine,
            EasingMode.IN_OUT_SINE: Transitioner.ease_in_out_sine,
            EasingMode.IN_QUAD: Transitioner.ease_in_quad,
            EasingMode.OUT_QUAD: Transitioner.ease_out_quad,
            EasingMode.IN_OUT_QUAD: Transitioner.ease_in_out_quad,
            EasingMode.IN_CUBIC: Transitioner.ease_in_cubic,
            EasingMode.OUT_CUBIC: Transitioner.ease_out_cubic,
            EasingMode.IN_OUT_CUBIC: Transitioner.ease_in_out_cubic,
            EasingMode.IN_QUART: Transitioner.ease_in_quart,
            EasingMode.OUT_QUART: Transitioner.ease_out_quart,
            EasingMode.IN_OUT_QUART: Transitioner.ease_in_out_quart,
            EasingMode.IN_QUINT: Transitioner.ease_in_quint,
            EasingMode.OUT_QUINT: Transitioner.ease_out_quint,
            EasingMode.IN_OUT_QUINT: Transitioner.ease_in_out_quint,
            EasingMode.IN_EXPO: Transitioner.ease_in_expo,
            EasingMode.OUT_EXPO: Transitioner.ease_out_expo,
            EasingMode.IN_OUT_EXPO: Transitioner.ease_in_out_expo,
            EasingMode.IN_CIRC: Transitioner.ease_in_circ,
            EasingMode.OUT_CIRC: Transitioner.ease_out_circ,
            EasingMode.IN_OUT_CIRC: Transitioner.ease_in_out_circ,
        }
        
        function = ease_modes[mode]
        y = min(max(0, function(progress)), 1)

        output = []

        for old_tuple, new_tuple in zip(old_buffer, new_buffer):
            output.append(tuple(
                (1 - y) * old + y * new
                for old, new in zip(old_tuple, new_tuple)
            ))
        
        return output

    @staticmethod
    def ease_linear(x: float):
        return x
    
    # The following implementations are adopted from https://easings.net/

    @staticmethod
    def ease_in_sine(x: float):
        return 1 - math.cos((x * math.pi) / 2)

    @staticmethod
    def ease_out_sine(x: float):
        return math.sin((x * math.pi) / 2)

    @staticmethod
    def ease_in_out_sine(x: float):
        return -(math.cos(x * math.pi) - 1) / 2


    @staticmethod
    def ease_in_power(x: float, power: int):
        return math.pow(x, power)

    @staticmethod
    def ease_out_power(x: float, power: int):
        return 1 - math.pow(1 - x, power)

    @staticmethod
    def ease_in_out_power(x: float, power: int):
        return math.pow(2, power) * x * x if x < 0.5 else 1 - math.pow(-2 * x + 2, power) / 2
        

    @staticmethod
    def ease_in_quad(x: float):
        return Transitioner.ease_in_power(x, 2)

    @staticmethod
    def ease_out_quad(x: float):
        return Transitioner.ease_out_power(x, 2)

    @staticmethod
    def ease_in_out_quad(x: float):
        return Transitioner.ease_in_out_power(x, 2)
    
    @staticmethod
    def ease_in_cubic(x: float):
        return Transitioner.ease_in_power(x, 3)

    @staticmethod
    def ease_out_cubic(x: float):
        return Transitioner.ease_out_power(x, 3)

    @staticmethod
    def ease_in_out_cubic(x: float):
        return Transitioner.ease_in_out_power(x, 3)

    @staticmethod
    def ease_in_quart(x: float):
        return Transitioner.ease_in_power(x, 4)

    @staticmethod
    def ease_out_quart(x: float):
        return Transitioner.ease_out_power(x, 4)

    @staticmethod
    def ease_in_out_quart(x: float):
        return Transitioner.ease_out_power(x, 4)

    @staticmethod
    def ease_in_quint(x: float):
        return Transitioner.ease_in_power(x, 5)

    @staticmethod
    def ease_out_quint(x: float):
        return Transitioner.ease_out_power(x, 5)

    @staticmethod
    def ease_in_out_quint(x: float):
        return Transitioner.ease_out_power(x, 5)

    
    @staticmethod
    def ease_in_expo(x: float):
        return 0 if x == 0 else math.pow(2, 10 * x - 10)

    @staticmethod
    def ease_out_expo(x: float):
        return 1 if x == 1 else 1 - math.pow(2, -10 * x)

    @staticmethod
    def ease_in_out_expo(x: float):
        if x == 0: return 0
        if x == 1: return 1
        return math.pow(2, 20 * x - 10) / 2 if x < 0.5 else (2 - math.pow(2, -20 * x + 10)) / 2


    @staticmethod
    def ease_in_circ(x: float):
        return 1 - math.sqrt(1 - math.pow(x, 2))

    @staticmethod
    def ease_out_circ(x: float):
        return math.sqrt(1 - math.pow(x - 1, 2))

    @staticmethod
    def ease_in_out_circ(x: float):
        if x < 0.5:
            return (1 - math.sqrt(1 - math.pow(2 * x, 2))) / 2
        return (math.sqrt(1 - math.pow(-2 * x + 2, 2)) + 1) / 2

    