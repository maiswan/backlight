from fastapi import APIRouter, Body, HTTPException, status, Request
from model.command_union import CommandUnion
import uuid

router = APIRouter()

# GET all commands
@router.get("/")
async def get_all(request: Request):
    state = request.state.state
    return state.config.commands

# POST new command
@router.post("/", status_code=status.HTTP_201_CREATED)
async def post(request: Request, command: CommandUnion = Body(...)):
    state = request.state.state
    state.config.commands.append(command)
    state.config.write()
    state.restart_rendering()
    return command

# PUT new commands and remove existing commands
@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def put_all(request: Request, commands: list[CommandUnion] = Body(...)):
    state = request.state.state
    state.config.commands = commands[::]
    state.config.write()
    state.restart_rendering()

# DELETE all existing commands
@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all(request: Request):
    state = request.state.state
    state.config.commands = []
    state.config.write()
    state.restart_rendering()

def find_command(commands: list[CommandUnion], identifier: str):
    try:
        command_id = uuid.UUID(identifier)
    except ValueError: # not an UUID
        command_id = None

    for i, command in enumerate(commands):
        if command.name == identifier or command.id == command_id:
            return i
    
    return -1

# GET existing command
@router.get("/{identifier}")
async def get_command(request: Request, identifier: str):
    config = request.state.state.config
    i = find_command(config.commands, identifier)

    if i == -1:
        raise HTTPException(status_code=404, detail="Command not found")

    return config.commands[i]

# PUT existing command
@router.put("/{identifier}", status_code=status.HTTP_204_NO_CONTENT)
async def put_command(request: Request, identifier: str, command: CommandUnion = Body(...)):
    state = request.state.state
    i = find_command(state.config.commands, identifier)

    if i == -1:
        raise HTTPException(status_code=404, detail="Command not found")

    state.config.commands[i] = command
    state.config.write()
    state.restart_rendering()

# PATCH existing command
@router.patch("/{identifier}", status_code=status.HTTP_204_NO_CONTENT)
async def patch_command(request: Request, identifier: str):
    state = request.state.state
    i = find_command(state.config.commands, identifier)

    if i == -1:
        raise HTTPException(status_code=404, detail="Command not found")

    body = await request.json()
    if "mode" in body:
        raise HTTPException(status_code=422, detail="Use PUT to change mode")

    for key, value in body.items():
        setattr(state.config.commands[i], key, value)
        
    state.config.write()
    state.restart_rendering()
        
# DELETE existing command
@router.delete("/{identifier}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_command(request: Request, identifier: str):
    state = request.state.state
    state.config.commands = [ x for x in state.config.commands if not (x.name == identifier or x.id == identifier) ]
    state.config.write()
    state.restart_rendering()
