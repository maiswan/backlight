from __future__ import annotations
from typing import TYPE_CHECKING
from .blender import Blender, BlendMode

if TYPE_CHECKING:
    from ..command import CommandUnion

class Renderer:
    @staticmethod
    def render(commands: list[CommandUnion], buffer_length: int, now: int):

        enabled_commands = sorted([ x for x in commands if x.is_enabled], key=lambda x: x.z_index)
        is_static = all(x.is_static for x in enabled_commands)
        
        buffer = [(0.0, 0.0, 0.0)] * buffer_length
    
        for command in enabled_commands:
            # Compute buffer
            new_buffer = buffer[:]
            command.execute(new_buffer, buffer_length, now)

            # Blend
            if (command.target_indices is None):
                continue

            # Transform commands do not support the blend property (since it doesn't really makes sense)
            blend_mode = command.blend if "source" in command.mode else BlendMode.NORMAL
            Blender.blend(buffer, new_buffer, command.target_indices, blend_mode, command.alpha)

        return (is_static, buffer)
