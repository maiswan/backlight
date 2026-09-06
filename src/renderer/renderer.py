from __future__ import annotations
from typing import TYPE_CHECKING
from .blender import Blender, BlendMode

if TYPE_CHECKING:
    from ..command import CommandUnion

class Renderer:

    @staticmethod
    def create_buffer(buffer_length: int):
        return [(0.0, 0.0, 0.0)] * buffer_length

    @staticmethod
    def render(commands: list[CommandUnion], buffer_length: int, now: int):

        enabled_commands = [ x for x in commands if x.is_enabled]
        is_static = all(x.is_static for x in enabled_commands)
        
        buffer = Renderer.create_buffer(buffer_length)
    
        for command in enabled_commands:
            # Compute buffer
            new_buffer = buffer[:]
            command.execute(new_buffer, now)

            if (command.target_indices is None):
                continue

            # Blend source commands (it doesn't make sense to blend transform commands)
            blend_mode = command.blend if "source" in command.mode else BlendMode.NORMAL
            Blender.blend(buffer, new_buffer, command.target_indices, blend_mode, command.alpha)

        return (is_static, buffer)
