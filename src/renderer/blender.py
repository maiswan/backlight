from enum import Enum
import random
from math import sqrt
from .rgbToHsl import rgbToHsl, HslToRgb
from .buffer_types import RgbTuple, RgbBuffer

class BlendMode(Enum):
    # Normal group
    NORMAL = "normal"
    DISSOLVE = "dissolve"

    # Darken group
    DARKEN = "darken"
    MULTIPLY = "multiply"
    COLOR_BURN = "color_burn"
    LINEAR_BURN = "linear_burn"
    DARKER_COLOR = "darker_color"

    # Lighten group
    LIGHTEN = "lighten"
    SCREEN = "screen"
    COLOR_DODGE = "color_dodge"
    LINEAR_DODGE = "linear_dodge" # "Linear Dodge (Add)" in Photoshop

    # Contrast group
    OVERLAY = "overlay"
    SOFT_LIGHT = "soft_light"
    HARD_LIGHT = "hard_light"
    VIVID_LIGHT = "vivid_light"
    LINEAR_LIGHT = "linear_light"
    PIN_LIGHT = "pin_light"
    HARD_MIX = "hard_mix"

    # Comparative Group
    DIFFERENCE = "difference"
    EXCLUSION = "exclusion"       # "XOR" in Paint.NET
    SUBTRACT = "subtract"
    DIVIDE = "divide"

    # HSL Group
    HUE = "hue"
    SATURATION = "saturation"
    COLOR = "color"
    LUMINOSITY = "luminosity"

class Blender:

    @staticmethod
    def blend(bottom_buffer: RgbBuffer, top_buffer: RgbBuffer, indices: list[int], mode: BlendMode, alpha: float):
        
        blend_modes = {
            BlendMode.NORMAL: Blender.normal,
            BlendMode.DISSOLVE: Blender.dissolve,
            BlendMode.DARKEN: Blender.darken,
            BlendMode.MULTIPLY: Blender.multiply,
            BlendMode.COLOR_BURN: Blender.color_burn,
            BlendMode.LINEAR_BURN: Blender.linear_burn,
            BlendMode.DARKER_COLOR: Blender.darker_color,
            BlendMode.LIGHTEN: Blender.lighten,
            BlendMode.SCREEN: Blender.screen,
            BlendMode.COLOR_DODGE: Blender.color_dodge,
            BlendMode.LINEAR_DODGE: Blender.linear_dodge,
            BlendMode.OVERLAY: Blender.overlay,
            BlendMode.SOFT_LIGHT: Blender.soft_light,
            BlendMode.HARD_LIGHT: Blender.hard_light,
            BlendMode.VIVID_LIGHT: Blender.vivid_light,
            BlendMode.LINEAR_LIGHT: Blender.linear_light,
            BlendMode.PIN_LIGHT: Blender.pin_light,
            BlendMode.HARD_MIX: Blender.hard_mix,
            BlendMode.DIFFERENCE: Blender.difference,
            BlendMode.EXCLUSION: Blender.exclusion,
            BlendMode.SUBTRACT: Blender.subtract,
            BlendMode.DIVIDE: Blender.divide,
            BlendMode.HUE: Blender.hue,
            BlendMode.SATURATION: Blender.saturation,
            BlendMode.COLOR: Blender.color,
            BlendMode.LUMINOSITY: Blender.luminosity,
        }

        function = blend_modes[mode]
        for i in indices:
            blended = function(bottom_buffer[i], top_buffer[i])

            bottom_buffer[i] = (
                bottom_buffer[i][0] * (1 - alpha) + blended[0] * alpha,
                bottom_buffer[i][1] * (1 - alpha) + blended[1] * alpha,
                bottom_buffer[i][2] * (1 - alpha) + blended[2] * alpha,
            )

            

    @staticmethod
    def luminance(rgb: RgbTuple):
        return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]



    @staticmethod
    def normal(bottom: RgbTuple, top: RgbTuple):
        return top

    @staticmethod
    def dissolve(bottom: RgbTuple, top: RgbTuple):
        # Non-deterministic within the same runtime
        return random.choice([bottom, top])

    

    @staticmethod
    def darken(bottom: RgbTuple, top: RgbTuple):
        def do(bottom: float, top: float):
            return min(bottom, top)

        return (do(bottom[0], top[0]), do(bottom[1], top[1]), do(bottom[2], top[2]))

    @staticmethod
    def multiply(bottom: RgbTuple, top: RgbTuple):
        def do(bottom: float, top: float):
            return bottom * top

        return (do(bottom[0], top[0]), do(bottom[1], top[1]), do(bottom[2], top[2]))

    @staticmethod
    def color_burn(bottom: RgbTuple, top: RgbTuple):
        def do(bottom: float, top: float):
            if top == 0:
                return 0
            return 1 - min(1, (1 - bottom) / top)

        return (do(bottom[0], top[0]), do(bottom[1], top[1]), do(bottom[2], top[2]))

    @staticmethod
    def linear_burn(bottom: RgbTuple, top: RgbTuple):
        def do(bottom: float, top: float):
            return max(bottom + top - 1, 0)

        return (do(bottom[0], top[0]), do(bottom[1], top[1]), do(bottom[2], top[2]))

    @staticmethod
    def darker_color(bottom: RgbTuple, top: RgbTuple):
        return top if (Blender.luminance(top) < Blender.luminance(bottom)) else bottom



    @staticmethod
    def lighten(bottom: RgbTuple, top: RgbTuple):
        def do(bottom: float, top: float):
            return max(bottom, top)

        return (do(bottom[0], top[0]), do(bottom[1], top[1]), do(bottom[2], top[2]))

    @staticmethod
    def screen(bottom: RgbTuple, top: RgbTuple):
        def do(bottom: float, top: float):
            return 1 - (1 - bottom) * (1 - top)

        return (do(bottom[0], top[0]), do(bottom[1], top[1]), do(bottom[2], top[2]))

    @staticmethod
    def color_dodge(bottom: RgbTuple, top: RgbTuple):
        def do(bottom: float, top: float):
            return 1 if top == 1 else min(1, bottom / (1 - top))

        return (do(bottom[0], top[0]), do(bottom[1], top[1]), do(bottom[2], top[2]))

    @staticmethod
    def linear_dodge(bottom: RgbTuple, top: RgbTuple):
        def do(bottom: float, top: float):
            return min(bottom + top, 1)

        return (do(bottom[0], top[0]), do(bottom[1], top[1]), do(bottom[2], top[2]))



    @staticmethod
    def overlay(bottom: RgbTuple, top: RgbTuple):
        def do(bottom: float, top: float):
            if bottom < 0.5:
                return 2 * bottom * top
            return 1 - 2 * (1 - bottom) * (1 - top)
        
        return (do(bottom[0], top[0]), do(bottom[1], top[1]), do(bottom[2], top[2]))

    @staticmethod
    def soft_light(bottom: RgbTuple, top: RgbTuple):
        def do(bottom: float, top: float):
            if top <= 0.5:
                return bottom - (1 - 2 * top) * bottom * (1 - bottom)
            alpha = sqrt(bottom) - bottom if bottom <= 0.25 else 4 * bottom - 1
            return bottom + (2 * top - 1) * alpha

        return (do(bottom[0], top[0]), do(bottom[1], top[1]), do(bottom[2], top[2]))

    @staticmethod
    def hard_light(bottom: RgbTuple, top: RgbTuple):
        def do(bottom: float, top: float):
            if top < 0.5:
                return 2 * bottom * top
            return 1 - 2 * (1 - top) * (1 - bottom)

        return (do(bottom[0], top[0]), do(bottom[1], top[1]), do(bottom[2], top[2]))

    @staticmethod
    def vivid_light(bottom: RgbTuple, top: RgbTuple):
        def do(bottom: float, top: float):
            if top < 0.5:
                return 1 - min(1, (1 - bottom) / (2 * top)) * 2 * top
            return min(1, bottom / (2 * (1 - top))) * 2 * (1 - top) + 2 * top - 1

        return (do(bottom[0], top[0]), do(bottom[1], top[1]), do(bottom[2], top[2]))

    @staticmethod
    def linear_light(bottom: RgbTuple, top: RgbTuple):
        def do(bottom: float, top: float):
            return min(1, max(0, bottom + 2 * top - 1))
            
        return (do(bottom[0], top[0]), do(bottom[1], top[1]), do(bottom[2], top[2]))

    @staticmethod
    def pin_light(bottom: RgbTuple, top: RgbTuple):
        def do(bottom: float, top: float):
            if top < 0.5:
                return min(bottom, 2 * top)
            return max(bottom, 2 * top - 1)
            
        return (do(bottom[0], top[0]), do(bottom[1], top[1]), do(bottom[2], top[2]))

    @staticmethod
    def hard_mix(bottom: RgbTuple, top: RgbTuple):
        blend = Blender.linear_light(bottom, top)

        def do(blend: float):
            return 0 if blend < 0.5 else 1
            
        return (do(blend[0]), do(blend[1]), do(blend[2]))
        

        
    @staticmethod
    def difference(bottom: RgbTuple, top: RgbTuple):
        def do(bottom: float, top: float):
            return abs(bottom - top)

        return (do(bottom[0], top[0]), do(bottom[1], top[1]), do(bottom[2], top[2]))

    @staticmethod
    def exclusion(bottom: RgbTuple, top: RgbTuple):
        def do(bottom: float, top: float):
            return bottom + top - 2 * bottom * top

        return (do(bottom[0], top[0]), do(bottom[1], top[1]), do(bottom[2], top[2]))
    
    @staticmethod
    def subtract(bottom: RgbTuple, top: RgbTuple):
        def do(bottom: float, top: float):
            return max(0, bottom - top)
            
        return (do(bottom[0], top[0]), do(bottom[1], top[1]), do(bottom[2], top[2]))

    @staticmethod
    def divide(bottom: RgbTuple, top: RgbTuple):
        def do(bottom: float, top: float):
            if top == 0:
                return 1
            return min(1, bottom / top)
            
        return (do(bottom[0], top[0]), do(bottom[1], top[1]), do(bottom[2], top[2]))

    
    
    @staticmethod
    def hue(bottom: RgbTuple, top: RgbTuple):
        bottom_hsl = rgbToHsl(bottom[0], bottom[1], bottom[2])
        top_hsl = rgbToHsl(top[0], top[1], top[2])

        return HslToRgb(top_hsl[0], bottom_hsl[1], bottom_hsl[2])
        
    @staticmethod
    def saturation(bottom: RgbTuple, top: RgbTuple):
        bottom_hsl = rgbToHsl(bottom[0], bottom[1], bottom[2])
        top_hsl = rgbToHsl(top[0], top[1], top[2])

        return HslToRgb(bottom_hsl[0], top_hsl[1], bottom_hsl[2])

    @staticmethod
    def color(bottom: RgbTuple, top: RgbTuple):
        bottom_hsl = rgbToHsl(bottom[0], bottom[1], bottom[2])
        top_hsl = rgbToHsl(top[0], top[1], top[2])

        return HslToRgb(top_hsl[0], top_hsl[1], bottom_hsl[2])

    @staticmethod
    def luminosity(bottom: RgbTuple, top: RgbTuple):
        bottom_hsl = rgbToHsl(bottom[0], bottom[1], bottom[2])
        top_hsl = rgbToHsl(top[0], top[1], top[2])

        return HslToRgb(bottom_hsl[0], bottom_hsl[1], top_hsl[2])
        

    
    
