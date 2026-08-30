from ..command_union import CommandUnion
from .blender import Blender, BlendMode
from ..buffer_types import RgbTuple
import time

class Renderer:
    @staticmethod
    def toRgbwTuple(tuple: RgbTuple):
        red = min(max(0, tuple[0] * 255), 255)
        green = min(max(0, tuple[1] * 255), 255)
        blue = min(max(0, tuple[2] * 255), 255)

        # Offload as much brightness to white LED as possible
        white = min(red, green, blue)
        red -= white
        green -= white
        blue -= white
        return (red, green, blue, white)

    @staticmethod
    def toRgbTuple(tuple: RgbTuple):
        red = min(max(0, tuple[0] * 255), 255)
        green = min(max(0, tuple[1] * 255), 255)
        blue = min(max(0, tuple[2] * 255), 255)
        return (red, green, blue)

    @staticmethod
    def render(commands: CommandUnion, buffer_length: int):
        now = time.monotonic()

        enabled_commands = sorted([ x for x in commands if x.is_enabled], key=lambda x: x.z_index)
        is_static = all(x.is_static for x in enabled_commands)
        
        buffer = [(0.0, 0.0, 0.0)] * buffer_length
    
        for command in enabled_commands:
            # Compute buffer
            new_buffer = buffer[:]
            command.execute(new_buffer, buffer_length, now)

            # Blend
            # Transform commands do not support the blend property (since it doesn't really makes sense)
            blend_mode = command.blend if "source" in command.mode else BlendMode.NORMAL
            Blender.blend(buffer, new_buffer, command.target_indices, blend_mode, command.alpha)

        # scale = Renderer.toRgbwTuple if need_rgbw_conversion else Renderer.toRgbTuple
        # buffer = [ scale(i) for i in buffer ]
        return (is_static, buffer)
