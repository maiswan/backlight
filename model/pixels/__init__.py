from ..config import LedConfig, SpiTransport
from .pixel_base import PixelBase

def get_pixels(led_config: LedConfig):
    if isinstance(led_config.transport, SpiTransport):
        from .spi import NeoPixelSPI
        return NeoPixelSPI(
            led_config.transport.device,
            led_config.transport.speed_khz,
            led_config.count,
            led_config.pixel_order
        )
    
    from .pwm import NeoPixelPWM
    return NeoPixelPWM(
        led_config.transport.pin,
        led_config.count,
        led_config.pixel_order,
    )

__all__ = [
    "PixelBase",
    "get_pixels",
]