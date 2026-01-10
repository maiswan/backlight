from pydantic import BaseModel, Field
from ..renderer.transitioner import EasingMode

class FramerateConfig(BaseModel):
    active: float = Field(gt=0)
    idle: float = Field(ge=0)     # 0 => don't redraw

class TransitionConfig(BaseModel):
    duration: float = Field(ge=0) # 0 => no transition
    mode: EasingMode

class RendererConfig(BaseModel):
    framerate: FramerateConfig
    transitions: TransitionConfig
