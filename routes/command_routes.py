# from typing import Annotated, Union
from fastapi import APIRouter, Body, HTTPException, status
# from pydantic import Field
# from model.command.alpha import AlphaCommandUnion
# from model.command.color import ColorCommandUnion
# from model.command.correction import CorrectionCommandUnion
# from model.state import state
# 
router = APIRouter()
# 
# commandUnion = Annotated[
#     Union[AlphaCommandUnion, ColorCommandUnion, CorrectionCommandUnion],
#     Field(discriminator="mode")
# ]
# 
# # GET all commands
# @router.get("/")
# async def get_all():
#     return state.config.commands
# 
# # POST new command
# @router.post("/", status_code=status.HTTP_201_CREATED)
# async def post(command: commandUnion = Body(...)):
#     state.config.commands.append(command)
#     state.write_config()
#     state.initialize_render_task()
#     return command
# 
# # PUT new commands and remove existing commands
# @router.put("/", status_code=status.HTTP_204_NO_CONTENT)
# async def put_all(commands: list[commandUnion] = Body(...)):
#     state.config.commands = commands[::]
#     state.write_config()
#     state.initialize_render_task()
# 
# # DELETE all existing commands
# @router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_all():
#     if len(state.config.commands) == 0:
#         raise HTTPException(status_code=404, detail="No commands to delete")
# 
#     state.config.commands = []
#     state.write_config()
#     state.initialize_render_task()
# 
# # GET existing command
# @router.get("/{id_or_name}")
# async def get_command(id_or_name: str):
#     for command in state.config.commands:
#         if command.name == id_or_name or command.id == id_or_name:
#             return command
#     else:
#         raise HTTPException(status_code=404, detail="Command not found")
# 
# # PUT existing command
# @router.put("/{id_or_name}", status_code=status.HTTP_204_NO_CONTENT)
# async def put_command(id_or_name: str, newCommand: commandUnion = Body(...)):
#     for i, command in enumerate(state.config.commands):
#         if command.name == id_or_name or command.id == id_or_name:
#             state.config.commands[i] = newCommand
#             state.write_config()
#             state.initialize_render_task()
#     else:
#         raise HTTPException(status_code=404, detail="Command not found")
#         
# # DELETE existing command
# @router.delete("/{id_or_name}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_command(id_or_name: str):
#     before = len(state.config.commands)
#     state.config.commands = [ x for x in state.config.commands if not (x.name == id_or_name or x.id == id_or_name) ]
#     after = len(state.config.commands)
# 
#     if before == after:
#         raise HTTPException(status_code=404, detail="Command not found")
#     
#     state.write_config()
#     state.initialize_render_task()