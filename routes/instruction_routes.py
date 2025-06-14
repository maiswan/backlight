from typing import Annotated, Union
from uuid import UUID
from fastapi import APIRouter, Body, HTTPException
from pydantic import Field
from model.instruction.alpha import AlphaInstructionUnion
from model.instruction.color import ColorInstructionUnion
from model.instruction.gamma import GammaInstructionUnion
from model.state import state

router = APIRouter()

instructionUnion = Annotated[
    Union[AlphaInstructionUnion, ColorInstructionUnion, GammaInstructionUnion],
    Field(discriminator="identifier")
]

# GET all commands
@router.get("/")
async def get():
    return state.config.instructions

# POST new instruction; return populated instruction with UUID
@router.post("/")
async def post(instruction: instructionUnion = Body(...)):
    state.config.instructions.append(instruction)
    return instruction

# POST new instructions and remove existing instructions
@router.post("/reset")
async def post_reset(instructions: list[instructionUnion] = Body(...)):
    # do stuff
    state.config.instructions = instructions[::]
    return state.config.instructions

# PUT existing instruction by ID
@router.put("/{id}")
async def put(id: UUID, newInstruction: instructionUnion = Body(...)):
    for i, instruction in enumerate(state.config.instructions):
        if instruction.id == id and newInstruction.id == id:
            state.config.instructions[i] = newInstruction
            return newInstruction
    else:
        raise HTTPException(status_code=404, detail="Instruction not found")
        
# DELETE existing instruction by ID
@router.delete("/{id}")
async def delete(id: UUID):
    before = len(state.config.instructions)
    state.config.instructions = [ inst for inst in state.config.instructions if inst.id != id ]
    after = len(state.config.instructions)

    if before == after:
        raise HTTPException(status_code=404, detail="Instruction not found")
    
    return {"detail": "Deleted"}

# DELETE all existing instructions
@router.delete("/all")
async def delete_all():
    if len(state.config.instructions) == 0:
        raise HTTPException(status_code=404, detail="No instructions to delete")

    state.config.instructions = []
    return {"detail": "Deleted"}
