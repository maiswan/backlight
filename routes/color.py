from fastapi import APIRouter
from model.config import ColorInstructionUnion
from model.state import state

router = APIRouter()

# Apex functions
@router.get("/")
async def get():
    return {
        "red": state.current_red,
        "green": state.current_green,
        "blue": state.current_blue,
    } 

@router.put("/")
async def put(instruction: ColorInstructionUnion):
    return { "success": await state.execute_instruction(instruction) }
