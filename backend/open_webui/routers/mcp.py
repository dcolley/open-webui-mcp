from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, ConfigDict
from open_webui.utils.auth import get_admin_user, get_verified_user

from open_webui.models.mcp_servers import (
    MCPServer,
    MCPServerModel,
    MCPServerResponse,
    MCPServers,
    MCPServerForm,
    MCPServerUserResponse,
)

router = APIRouter()

# class MCPServer(BaseModel):
#     name: str
#     command: Optional[str] = None
#     url: Optional[str] = None
#     variables: dict = {}
#     model_config = ConfigDict(from_attributes=True)

# class MCPServersConfig(BaseModel):
#     servers: List[MCPServer]
#     model_config = ConfigDict(from_attributes=True)


############################
# get a list of MCP servers
# GET [/api/v1/mcp]
############################


@router.get("/", response_model=List[MCPServerUserResponse])
async def get_mcp_servers(request: Request, user=Depends(get_admin_user)):
    if user.role == "admin":
        return MCPServers.get_mcp_servers()
    else:
        return MCPServers.get_mcp_servers_by_user_id(user.id)


############################
# get an MCP server by id
# GET [/api/v1/mcp]/{server_id}
############################


@router.get("/{server_id}", response_model=MCPServerUserResponse)
async def get_mcp_server_by_id(server_id: str, user=Depends(get_admin_user)):
    return MCPServers.get_mcp_server_by_id(server_id)


############################
# add an MCP server
# POST [/api/v1/mcp]
############################

@router.post("/create", response_model=MCPServerResponse)
async def add_mcp_server(
    request: Request, 
    form_data: MCPServerForm,
    user=Depends(get_verified_user),
):
    # print('add_mcp_server')
    # print(form_data)
    return MCPServers.insert_new_mcp_server(
        user.id,
        form_data
        # specs=[]
    )


############################
# update the MCP config
# POST [/api/v1/mcp]
############################

@router.post("/{server_id}/edit", response_model=MCPServerResponse)
async def update_mcp_config(
    server_id: str,
    request: Request, 
    form_data: MCPServerForm, 
    user=Depends(get_admin_user)
):
    print('update_mcp_config')
    print(server_id)
    print(form_data)
    return MCPServers.update_mcp_server_by_id(server_id, form_data)


############################
# delete an MCP server
# POST [/api/v1/mcp]/{server_id}/delete
############################

@router.post("/{server_id}/delete", response_model=bool)
async def delete_mcp_server(server_id: str, user=Depends(get_admin_user)):
    print('delete_mcp_server')
    print(server_id)
    return MCPServers.delete_mcp_server_by_id(server_id)

############################
# invoke an MCP tool
# POST [/api/v1/mcp]/{server_name}/call
############################

@router.post("/{server_id}/call", response_model=MCPServerResponse)
async def invoke_mcp_tool(request: Request, server_id: str, user=Depends(get_admin_user)):
    return MCPServers.get_mcp_server_by_id(server_id)

############################
# get the MCP config
# GET [/api/v1/mcp]
############################

# # corresponds to GET /api/mcp
# @router.get("/", response_model=MCPServersConfig)
# async def get_mcp_config(request: Request, user=Depends(get_admin_user)):
#     return {
#         "servers": request.app.state.config.MCP_SERVERS
#     }

