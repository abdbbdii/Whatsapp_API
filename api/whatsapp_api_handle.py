from django.utils import timezone
import requests
import re
import os
from pathlib import Path
import importlib.util
from .appSettings import appSettings
from Whatsapp_API.settings import DEBUG
from shlex import split
from typing import Any, Dict, List, Optional, Tuple, Union


class SenderInBlackList(Exception):
    pass


class SenderNotAdmin(Exception):
    pass


class EmptyMessageInGroup(Exception):
    pass


class CommandNotFound(Exception):
    pass


class MessageNotValid(Exception):
    pass


class Plugin:
    def __init__(self, command_name: str, admin_privilege: bool, description: str, handle_function: Any, internal: bool):
        self.command_name = command_name
        self.admin_privilege = admin_privilege
        self.description = description
        self.handle_function = handle_function
        self.internal = internal

    @staticmethod
    def load_plugins() -> Dict[str, "Plugin"]:
        plugins = {}
        plugin_files = [file.rstrip(".py") for file in os.listdir(Path("api/plugins")) if file.endswith(".py")]

        for file in plugin_files:
            spec = importlib.util.spec_from_file_location(file, Path("api/plugins") / (file + ".py"))
            plugin = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin)
            plugins[plugin.pluginInfo["command_name"]] = Plugin(
                command_name=plugin.pluginInfo["command_name"],
                admin_privilege=plugin.pluginInfo["admin_privilege"],
                description=plugin.pluginInfo["description"],
                internal=plugin.pluginInfo["internal"],
                handle_function=plugin.handle_function,
            )
        return plugins


class Message:
    def __init__(self, data: dict):
        self.senderId: Optional[str]
        self.groupId: Optional[str]
        self.sender: Optional[str]
        self.group: Optional[str]

        self.senderId, self.groupId = self.get_group_and_sender_id(data["from"])
        self.sender, self.group = map(lambda id: re.sub(r"^(\d+).*[:@].*$", r"\1", id) if id else None, [self.senderId, self.groupId])

        self.command_prefix = "./" if self.group else "/"
        self.arguments: Optional[List[Union[str, int, float]]] = None
        self.admin_privilege: bool = False
        self.incoming_text_message: Optional[str] = ""
        self.outgoing_text_message: Optional[str] = None
        self.link: Optional[str] = None
        self.send_to: List[str] = [self.senderId if self.groupId is None else self.groupId]
        self.document: Optional[Any] = data.get("document")
        self.media_mime_type: Optional[str] = None
        self.media_path: Optional[str] = None
        self.media: Optional[bytes] = None

        self.set_media(data)
        self.set_incoming_text_message(data)

    def set_incoming_text_message(self, data: dict) -> None:
        if not self.media_path:
            self.incoming_text_message = data["message"]["text"].replace("\xa0", " ")

        if not self.incoming_text_message and self.group:
            raise EmptyMessageInGroup("Message is empty in group.")
        elif self.sender not in appSettings.admin_ids and self.sender in appSettings.blacklist_ids:
            raise SenderInBlackList("Sender is in blacklist.")
        elif self.sender not in appSettings.admin_ids and DEBUG:
            raise PermissionError("Debug mode is enabled.")

        if self.group:
            if re.search(r"\.[^\.].*", self.incoming_text_message):
                self.incoming_text_message = self.incoming_text_message.lstrip(".").strip()
            else:
                # special case for kharchey plugin ---------------------------------------------------------------------------------------------
                if self.group == appSettings.kharchey_group_id and self.incoming_text_message:
                    self.incoming_text_message = "/kharchey " + self.incoming_text_message
                else:
                    raise MessageNotValid("Message does not start with a dot.")
                # ------------------------------------------------------------------------------------------------------------------------------

        if self.incoming_text_message.startswith("/"):
            self.incoming_text_message = self.incoming_text_message[1:].strip()
            self.arguments = split(self.incoming_text_message)

            if appSettings.admin_command_prefix == self.arguments[0] and self.sender in appSettings.admin_ids:
                self.admin_privilege = True
                self.arguments = self.arguments[1:]
                if not self.arguments:
                    self.arguments = ["help"]

    def set_media(self, data: dict) -> None:
        if data.get("image"):
            self.incoming_text_message = data["image"]["caption"].replace("\xa0", " ")
            self.media_mime_type = data["image"]["mime_type"]
            self.media_path = data["image"]["media_path"]

    @staticmethod
    def get_group_and_sender_id(string: str) -> Tuple[Optional[str], Optional[str]]:
        if " in " in string:
            sender, group = string.split(" in ")
            if not group.endswith("@g.us"):
                sender, group = group, None
        else:
            sender, group = string, None
        return sender, group

    def send_message(self) -> None:
        for phone in self.send_to:
            body = {
                "phone": phone,
                "message": self.outgoing_text_message,
            }
            response = requests.post(appSettings.whatsapp_client_url + "send/message", data=body)
            print(response.text)

    def send_link(self) -> None:
        for phone in self.send_to:
            body = {
                "phone": phone,
                "caption": self.outgoing_text_message,
                "link": self.link,
            }
            response = requests.post(appSettings.whatsapp_client_url + "send/link", data=body)
            print(response.text)

    def send_file(self, caption: bool = False) -> None:
        for phone in self.send_to:
            body = {
                "phone": phone,
                "caption": self.outgoing_text_message if caption else None,
            }
            response = requests.post(appSettings.whatsapp_client_url + "send/file", data=body, files=self.media)
            print(response.text)

    def send_audio(self, caption: bool = False) -> None:
        for phone in self.send_to:
            body = {
                "phone": phone,
                "caption": self.outgoing_text_message if caption else None,
            }
            response = requests.post(appSettings.whatsapp_client_url + "send/audio", data=body, files=self.media)
            print(response.text)

    def send_image(self, caption: bool = False) -> None:
        for phone in self.send_to:
            body = {
                "phone": phone,
                "caption": self.outgoing_text_message if caption else None,
            }
            response = requests.post(appSettings.whatsapp_client_url + "send/image", data=body, files=self.media)
            print(response.text)

    def send_video(self, caption: bool = False) -> None:
        for phone in self.send_to:
            body = {
                "phone": phone,
                "caption": self.outgoing_text_message if caption else None,
            }
            response = requests.post(appSettings.whatsapp_client_url + "send/video", data=body, files=self.media)
            print(response.text)

    def send_media(self, caption: bool = False) -> None:
        if self.media_mime_type == "audio/ogg":
            self.send_audio(caption)
        elif self.media_mime_type == "image/jpeg":
            self.send_image(caption)
        elif self.media_mime_type == "video/mp4":
            self.send_video(caption)
        else:
            self.send_file(caption)


class API:
    def __init__(self, data: dict) -> None:
        self.request_timestamp = timezone.now()
        self.message = Message(data)
        self.plugins = Plugin.load_plugins()

        try:
            if self.message.arguments:
                self.command_handle()
            else:
                self.message_handle()
        except (CommandNotFound, SenderNotAdmin) as e:
            self.message.outgoing_text_message = str(e)
            self.message.send_message()

    def message_handle(self) -> None:
        self.message.outgoing_text_message = f"Hello, I am a bot. Use `{self.message.command_prefix}help` (or `{self.message.command_prefix + appSettings.admin_command_prefix} help` if you are an admin) to see available commands."
        self.message.send_message()

    def command_handle(self) -> None:
        if self.message.arguments[0] == appSettings.admin_command_prefix and not self.message.admin_privilege:
            raise SenderNotAdmin("You are not an admin and cannot use admin commands.")

        if self.message.arguments == [""] or self.message.arguments[0] == "help":
            self.send_help()
        elif self.message.arguments[0] in self.plugins:
            plugin = self.plugins[self.message.arguments[0]]
            if plugin.admin_privilege == self.message.admin_privilege:
                plugin.handle_function(self.message)
        else:
            raise CommandNotFound(f"Command `{self.message.arguments[0]}` not found. Use `{self.message.command_prefix}help` to see available commands.")

    def send_help(self) -> None:
        help_message = {}
        prefix = appSettings.admin_command_prefix + " " if self.message.admin_privilege else ""

        for _, plugin in self.plugins.items():
            if plugin.admin_privilege == self.message.admin_privilege and not plugin.internal:
                help_message[prefix + plugin.command_name] = plugin.description

        help_message[prefix + "help"] = "Show this message."
        self.message.outgoing_text_message = "*Available commands:*\n"

        for command, description in help_message.items():
            self.message.outgoing_text_message += f"- `{self.message.command_prefix + command}`: {description}\n"
        self.message.send_message()
