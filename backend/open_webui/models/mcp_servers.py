import logging
import time
from typing import Optional

from open_webui.internal.db import Base, JSONField, get_db
from open_webui.models.users import Users, UserResponse
from open_webui.env import SRC_LOG_LEVELS
from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger, Column, String, Text, JSON, Boolean

from open_webui.utils.access_control import has_access


log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MAIN"])


####################
# MCP Servers DB Schema
####################


class MCPServer(Base):
    __tablename__ = "mcp_server"

    id = Column(String, primary_key=True)
    user_id = Column(String)
    name = Column(Text)
    description = Column(Text)
    type = Column(String)
    command = Column(String)
    url = Column(String)
    valves = Column(JSONField)
    enabled = Column(Boolean, default=True)

    # access_control = Column(JSON, nullable=True)  # Controls data access levels.

    # Defines access control rules for this entry.
    # - `None`: Public access, available to all users with the "user" role.
    # - `{}`: Private access, restricted exclusively to the owner.
    # - Custom permissions: Specific access control for reading and writing;
    #   Can specify group or user-level restrictions:
    #   {
    #      "read": {
    #          "group_ids": ["group_id1", "group_id2"],
    #          "user_ids":  ["user_id1", "user_id2"]
    #      },
    #      "write": {
    #          "group_ids": ["group_id1", "group_id2"],
    #          "user_ids":  ["user_id1", "user_id2"]
    #      }
    #   }

    updated_at = Column(BigInteger)
    created_at = Column(BigInteger)


class MCPServerMeta(BaseModel):
    description: Optional[str] = None
    manifest: Optional[dict] = {}


class MCPServerModel(BaseModel):
    id: str
    user_id: str
    name: str
    description: str
    type: str
    command: str
    url: str
    valves: list[dict]
    enabled: bool
    # access_control: Optional[dict] = None

    updated_at: int  # timestamp in epoch
    created_at: int  # timestamp in epoch

    model_config = ConfigDict(from_attributes=True)


####################
# Forms
####################


class MCPServerUserModel(MCPServerModel):
    user: Optional[UserResponse] = None


class MCPServerResponse(MCPServerModel):
    id: str
    user_id: str
    name: str
    description: str
    type: str
    command: str
    url: str
    valves: list[dict]
    enabled: bool
    # access_control: Optional[dict] = None
    updated_at: int  # timestamp in epoch
    created_at: int  # timestamp in epoch


class MCPServerUserResponse(MCPServerResponse):
    user: Optional[UserResponse] = None


class MCPServerForm(BaseModel):
    id: str
    name: str
    description: str
    type: str
    command: str
    url: str
    valves: list[dict]
    enabled: bool
    # access_control: Optional[dict] = None


class MCPServerValves(BaseModel):
    valves: Optional[dict] = None


class MCPServersTable:
    def insert_new_mcp_server(
        self,
        user_id: str,
        form_data: MCPServerForm,
        # specs: list[dict]
    ) -> Optional[MCPServerModel]:
        with get_db() as db:
            mcp_server = MCPServerModel(
                **{
                    **form_data.model_dump(),
                    # "specs": specs,
                    "user_id": user_id,
                    "updated_at": int(time.time()),
                    "created_at": int(time.time()),
                }
            )

            try:
                result = MCPServer(**mcp_server.model_dump())
                db.add(result)
                db.commit()
                db.refresh(result)
                if result:
                    return MCPServerModel.model_validate(result)
                else:
                    return None
            except Exception as e:
                log.exception(f"Error creating a new MCP server: {e}")
                return None

    def get_mcp_server_by_id(self, id: str) -> Optional[MCPServerModel]:
        try:
            with get_db() as db:
                mcp_server = db.get(MCPServer, id)
                return MCPServerModel.model_validate(mcp_server)
        except Exception:
            return None

    def get_mcp_servers(self) -> list[MCPServerUserModel]:
        with get_db() as db:
            mcp_servers = []
            for mcp_server in db.query(MCPServer).order_by(MCPServer.updated_at.desc()).all():
                user = Users.get_user_by_id(mcp_server.user_id)
                mcp_servers.append(
                    MCPServerUserModel.model_validate(
                        {
                            **MCPServerModel.model_validate(mcp_server).model_dump(),
                            "user": user.model_dump() if user else None,
                        }
                    )
                )
            return mcp_servers

    def get_mcp_servers_by_user_id(
        self, user_id: str, permission: str = "write"
    ) -> list[MCPServerUserModel]:
        mcp_servers = self.get_mcp_servers()

        return [
            mcp_server
            for mcp_server in mcp_servers
            if mcp_server.user_id == user_id
            or has_access(user_id, permission, mcp_server.access_control)
        ]

    # def get_mcp_server_valves_by_id(self, id: str) -> Optional[dict]:
    #     try:
    #         with get_db() as db:
    #             mcp_server = db.get(MCPServer, id)
    #             return mcp_server.valves if mcp_server.valves else {}
    #     except Exception as e:
    #         log.exception(f"Error getting MCP server valves by id {id}: {e}")
    #         return None

    # def update_mcp_server_valves_by_id(self, id: str, valves: dict) -> Optional[MCP_ServerValves]:
    #     try:
    #         with get_db() as db:
    #             db.query(MCP_Server).filter_by(id=id).update(
    #                 {"valves": valves, "updated_at": int(time.time())}
    #             )
    #             db.commit()
    #             return self.get_mcp_server_by_id(id)
    #     except Exception:
    #         return None

    def get_user_mcp_servers_by_id_and_user_id(
        self, id: str, user_id: str
    ) -> Optional[dict]:
        try:
            user = Users.get_user_by_id(user_id)
            user_settings = user.settings.model_dump() if user.settings else {}

            # Check if user has "tools" and "valves" settings
            if "tools" not in user_settings:
                user_settings["tools"] = {}
            if "valves" not in user_settings["tools"]:
                user_settings["tools"]["valves"] = {}

            return user_settings["tools"]["valves"].get(id, {})
        except Exception as e:
            log.exception(
                f"Error getting user values by id {id} and user_id {user_id}: {e}"
            )
            return None

    # def update_user_valves_by_id_and_user_id(
    #     self, id: str, user_id: str, valves: dict
    # ) -> Optional[dict]:
    #     try:
    #         user = Users.get_user_by_id(user_id)
    #         user_settings = user.settings.model_dump() if user.settings else {}

    #         # Check if user has "mcp_servers" and "valves" settings
    #         if "mcp_servers" not in user_settings:
    #             user_settings["mcp_servers"] = {}
    #         if "valves" not in user_settings["mcp_servers"]:
    #             user_settings["mcp_servers"]["valves"] = {}

    #         user_settings["mcp_servers"]["valves"][id] = valves

    #         # Update the user settings in the database
    #         Users.update_user_by_id(user_id, {"settings": user_settings})

    #         return user_settings["mcp_servers"]["valves"][id]
    #     except Exception as e:
    #         log.exception(
    #             f"Error updating user valves by id {id} and user_id {user_id}: {e}"
    #         )
    #         return None

    def update_mcp_server_by_id(self, id: str, updated: dict) -> Optional[MCPServerModel]:
        print('update_mcp_server_by_id')
        print(id)
        print(updated)
        try:
            with get_db() as db:
                db.query(MCPServer).filter_by(id=id).update(
                    {**updated.model_dump(), "updated_at": int(time.time())}
                )
                db.commit()

                # mcp_server = db.query(MCPServer).get(id)
                # db.refresh(mcp_server)
                # return MCPServerModel.model_validate(mcp_server)
                return self.get_mcp_server_by_id(id)
        except Exception:
            return None

    def delete_mcp_server_by_id(self, id: str) -> bool:
        try:
            with get_db() as db:
                db.query(MCPServer).filter_by(id=id).delete()
                db.commit()

                return True
        except Exception:
            return False


MCPServers = MCPServersTable()
