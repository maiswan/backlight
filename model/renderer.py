from .command_union import CommandUnion
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
    def render(commands: CommandUnion, led_count: int, need_rgbw_conversion: bool):
        now = time.monotonic()
        is_static = True
        commands.sort(key=lambda x: x.z_index)
        buffer = [(0.0, 0.0, 0.0)] * led_count
    
        for command in commands:
            if (not command.is_enabled):
                continue

            is_static = is_static and command.is_static
            try:
                new_buffer = buffer[:]
                command.execute(new_buffer, led_count, now)

                # lerp between layers
                for index in command.get_targets(led_count):
                    r1, g1, b1 = buffer[index]
                    r2, g2, b2 = new_buffer[index]
                    a = command.alpha

                    r = r1 * (1 - a) + r2 * a
                    g = g1 * (1 - a) + g2 * a
                    b = b1 * (1 - a) + b2 * a

                    buffer[index] = (r, g, b)

            except Exception as exception:
                print(exception)

        scale = Renderer.toRgbwTuple if need_rgbw_conversion else Renderer.toRgbTuple
        for i in range(len(buffer)):
            buffer[i] = scale(buffer[i])

        return (is_static, buffer)