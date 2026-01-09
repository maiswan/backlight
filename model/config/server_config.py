from pydantic import BaseModel, Field

class ServerConfig(BaseModel):
    port: int = Field(gt=0)