from fastapi import APIRouter, Body, status, Request
from .payloads import IntPayload, StrPayload

router = APIRouter()

# count
@router.get("/count")
async def get_count(request: Request):
    state = request.state.state
    return state.config.leds.count

@router.put("/count", status_code=status.HTTP_204_NO_CONTENT)
async def put_count(request: Request, payload: IntPayload = Body(...)):
    state = request.state.state
    
    state.uninitialize_output()
    state.config.leds.count = payload.value
    state.initialize_output()
    state.config.write()
        


# pixel_order
@router.get("/pixel_order")
async def get_pixel_order(request: Request):
    state = request.state.state
    return state.config.leds.pixel_order

@router.put("/pixel_order", status_code=status.HTTP_204_NO_CONTENT)
async def put_pixel_order(request: Request, payload: StrPayload = Body(...)):
    state = request.state.state
        
    state.uninitialize_output()
    state.config.leds.pixel_order = payload.value
    state.initialize_output()
    state.config.write()



# transport/mode
@router.get("/transport/mode")
async def get_transport_mode(request: Request):
    state = request.state.state
    return state.config.leds.transport.mode

@router.put("/transport/mode", status_code=status.HTTP_204_NO_CONTENT)
async def put_transport_mode(request: Request, payload: StrPayload = Body(...)):
    state = request.state.state

    state.uninitialize_output()
    state.config.leds.transport.mode = payload.value
    state.initialize_output()
    state.config.write()



# transport/pwm/pin
@router.get("/transport/pwm/pin")
async def get_transport_pwm_pin(request: Request):
    state = request.state.state
    return state.config.leds.transport.pwm.pin

@router.put("/transport/pwm/pin", status_code=status.HTTP_204_NO_CONTENT)
async def put_transport_pwm_pin(request: Request, payload: IntPayload = Body(...)):
    state = request.state.state

    state.uninitialize_output()
    state.config.leds.transport.pwm.pin = payload.value
    state.initialize_output()
    state.config.write()



# transport/spi/device
@router.get("/transport/spi/device")
async def get_transport_spi_device(request: Request):
    state = request.state.state
    return state.config.leds.transport.spi.device

@router.put("/transport/spi/device", status_code=status.HTTP_204_NO_CONTENT)
async def put_transport_spi_device(request: Request, payload: StrPayload = Body(...)):
    state = request.state.state
    state.uninitialize_output()
    state.config.leds.transport.spi.device = payload.value
    state.initialize_output()
    state.config.write()



# transport/spi/speed_khz
@router.get("/transport/spi/speed_khz")
async def get_transport_spi_speed_khz(request: Request):
    state = request.state.state
    return state.config.leds.transport.spi.speed_khz

@router.put("/transport/spi/speed_khz", status_code=status.HTTP_204_NO_CONTENT)
async def put_transport_spi_speed_khz(request: Request, payload: IntPayload = Body(...)):
    state = request.state.state
    state.uninitialize_output()
    state.config.leds.transport.spi.speed_khz = payload.value
    state.initialize_output()
    state.config.write()