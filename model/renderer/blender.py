from enum import Enum, auto

class BlendMode(Enum):
    NORMAL = "normal"
    MULTIPLY = "multiply"
    SCREEN = "screen"
    OVERLAY = "overlay"
    DARKEN = "darken"
    LIGHTEN = "lighten"
    ADDITIVE = "additive"
    SUBTRACT = "subtract"
    DIFFERENCE = "difference"
    COLOR_DODGE = "color_dodge"
    COLOR_BURN = "color_burn"
    SOFT_LIGHT = "soft_light"
    HARD_LIGHT = "hard_light"
    EXCLUSION = "exclusion" # aka XOR

class Blender:

    @staticmethod
    def blend(bottom: tuple[float, float, float], top: tuple[float, float, float], mode: BlendMode, alpha: float):
        
        blend_modes = {
            BlendMode.NORMAL: Blender.normal,
            BlendMode.MULTIPLY: Blender.multiply,
            BlendMode.SCREEN: Blender.screen,
            BlendMode.OVERLAY: Blender.overlay,
            BlendMode.DARKEN: Blender.darken,
            BlendMode.LIGHTEN: Blender.lighten,
            BlendMode.ADDITIVE: Blender.additive,
            BlendMode.SUBTRACT: Blender.subtract,
            BlendMode.DIFFERENCE: Blender.difference,
            BlendMode.COLOR_DODGE: Blender.color_dodge,
            BlendMode.COLOR_BURN: Blender.color_burn,
            BlendMode.SOFT_LIGHT: Blender.soft_light,
            BlendMode.HARD_LIGHT: Blender.hard_light,
            BlendMode.EXCLUSION: Blender.exclusion,
        }

        function = blend_modes[mode]
        r = bottom[0] * (1 - alpha) + function(bottom[0], top[0]) * alpha
        g = bottom[1] * (1 - alpha) + function(bottom[1], top[1]) * alpha
        b = bottom[2] * (1 - alpha) + function(bottom[2], top[2]) * alpha
        return (r, g, b)

    @staticmethod
    def normal(bottom: float, top: float):
        return top

    @staticmethod
    def multiply(bottom: float, top: float):
        return bottom * top

    @staticmethod
    def screen(bottom: float, top: float):
        return 1 - (1 - bottom) * (1 - top)

    @staticmethod
    def overlay(bottom: float, top: float):
        if bottom < 0.5:
            return 2 * bottom * top
            
        return 1 - 2 * (1 - bottom) * (1 - top)

    @staticmethod
    def darken(bottom: float, top: float):
        return min(bottom, top)
        
    @staticmethod
    def lighten(bottom: float, top: float):
        return max(bottom, top)

    @staticmethod
    def additive(bottom: float, top: float):
        return min(1, bottom + top)
    
    @staticmethod
    def subtract(bottom: float, top: float):
        return max(0, bottom - top)

    @staticmethod
    def difference(bottom: float, top: float):
        return abs(bottom - top)
    
    @staticmethod
    def color_dodge(bottom: float, top: float):
        if top == 1:
            return 1
        return min(1, bottom / (1 - top))

    @staticmethod
    def color_burn(bottom: float, top: float):
        if top == 0:
            return 0
        return 1 - min(1, bottom / (1 - top))

    @staticmethod
    def soft_light(bottom: float, top: float):
        return (1 - 2 * top) * pow(bottom, 2) + 2 * bottom * top

    @staticmethod
    def hard_light(bottom: float, top: float):
        if top < 0.5:
            return 2 * bottom * top
        return 1 - 2 * (1 - top) * (1 - bottom)

    @staticmethod
    def exclusion(bottom: float, top: float):
        return bottom + top - 2 * bottom * top
