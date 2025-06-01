from fastapi import APIRouter
from model.instruction.alpha import AlphaInstructionUnion
from model.state import state

router = APIRouter()

@router.get("/")
async def get_alpha():
    return { "alpha": state.current_alpha }

@router.put("/")
async def put_alpha(instruction: AlphaInstructionUnion):
    return { "success": await state.execute_instruction(instruction) }