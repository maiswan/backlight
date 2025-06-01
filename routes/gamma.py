from fastapi import APIRouter
from model.instruction.gamma import GammaInstructionUnion
from model.state import state

router = APIRouter()

@router.get("/")
async def get_gamma():
    return { "gamma": state.current_gamma[0] }

@router.put("/")
async def put_gamma(instruction: GammaInstructionUnion):
    return { "success": await state.execute_instruction(instruction) }