from pydantic import BaseModel, Field
from ..renderer.transitioner import EasingMode

class FramerateConfig(BaseModel):
    active: float = Field(gt=0, default=60)
    idle: float = Field(ge=0, default=0)     # 0 => don't redraw

class TransitionConfig(BaseModel):
    duration: float = Field(ge=0, default=2000) # 0 => no transition
    mode: EasingMode = Field(default=EasingMode.IN_OUT_CUBIC)

class RendererConfig(BaseModel):
    framerate: FramerateConfig = Field(default_factory=FramerateConfig)
    transitions: TransitionConfig = Field(default_factory=TransitionConfig)
