from ..command_union import CommandUnion
from .blender import Blender, BlendMode
import time

class Renderer:
    @staticmethod
    def toRgbwTuple(tuple: tuple[float, float, float]):
        white = min(tuple[0], tuple[1], tuple[2])
        red = (tuple[0] - white) * 255
        green = (tuple[1] - white) * 255
        blue = (tuple[2] - white) * 255
        white *= 255
        return (red, green, blue, white)

    @staticmethod
    def toRgbTuple(tuple: tuple[float, float, float]):
        return (tuple[0] * 255, tuple[1] * 255, tuple[2] * 255)

    @staticmethod
    def render(commands: CommandUnion, buffer_length: int, need_rgbw_conversion: bool):
        now = time.monotonic()
        is_static = True
        commands.sort(key=lambda x: x.z_index)
        buffer = [(0.0, 0.0, 0.0)] * buffer_length
    
        for command in commands:
            if (not command.is_enabled):
                continue

            is_static = is_static and command.is_static
            try:
                # Compute buffer
                new_buffer = buffer[:]
                command.execute(new_buffer, buffer_length, now)

                # Blend
                # Transform commands do not support the blend property (since it doesn't really makes sense)
                blend_mode = command.blend if "source" in command.mode else BlendMode.NORMAL

                for index in command.get_targets(buffer_length):
                    buffer[index] = Blender.blend(
                        buffer[index],
                        new_buffer[index],
                        blend_mode,
                        command.alpha
                    )

            except Exception as exception:
                print(exception)

        scale = Renderer.toRgbwTuple if need_rgbw_conversion else Renderer.toRgbTuple
        for i in range(len(buffer)):
            buffer[i] = scale(buffer[i])

        return (is_static, buffer)

    @staticmethod
    def transit_exponential(
        old_buffer: list[tuple[float, float, float]] | list[tuple[float, float, float, float]], 
        new_buffer: list[tuple[float, float, float]] | list[tuple[float, float, float, float]],
        alpha: float,
        buffer_length: int
    ):
        for i in range(buffer_length):
            old_tuple = old_buffer[i]
            new_tuple = new_buffer[i]

            old_buffer[i] = tuple(
                (1 - alpha) * old + alpha * new
                for old, new in zip(old_tuple, new_tuple)
            )