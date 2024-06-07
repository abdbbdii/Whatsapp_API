from django.utils import timezone
import requests, re, os
from pathlib import Path
import importlib.util
from .appSettings import appSettings
from Whatsapp_API.settings import DEBUG
from shlex import split
from typing import Any

# load_dotenv(find_dotenv()) if not os.getenv("VERCEL_ENV") else None

# ssh -R whatsapp-api:80:127.0.0.1:8000 serveo.net
# https://whatsapp-api.serveo.net


class SenderInBlackList(Exception):
    pass


class SenderNotAdmin(Exception):
    pass


class EmptyMessageInGroup(Exception):
    pass


class EmptyCommand(Exception):
    pass


class CommandNotFound(Exception):
    pass


class MessageNotValid(Exception):
    pass


class Plugin:
    def __init__(self, command_name, admin_privilege, description, handle_function, internal):
        self.command_name = command_name
        self.admin_privilege = admin_privilege
        self.description = description
        self.handle_function = handle_function
        self.internal = internal

    @staticmethod
    def load_plugins():
        plugins = {}
        for file in [file.rstrip(".py") for file in os.listdir(Path("api/plugins")) if file.endswith(".py")]:
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
        self.senderId: str | None
        self.groupId: str | None
        self.sender: str | None
        self.group: str | None

        self.senderId, self.groupId = self.getGroupAndSenderId(data["from"])
        self.sender, self.group = map(lambda id: re.sub(r"^(\d+).*[:@].*$", r"\1", id) if id else None, [self.senderId, self.groupId])

        self.arguments: list[str | int | float] | None = None
        self.admin_privilege: bool = False
        self.incoming_text_message: str | None = ""
        self.outgoing_text_message: str | None = None
        self.link: str | None = None
        self.send_to: list = [self.senderId if self.groupId is None else self.groupId]
        self.document: Any | None = data.get("document")
        self.media_mime_type: str | None = None
        self.media_path: str | None = None
        self.media: bytes | None = None

        self.set_media(data)
        self.set_incoming_text_message(data)

    def set_incoming_text_message(self, data):
        if not self.media_path:
            self.incoming_text_message = data["message"]["text"].replace("\xa0", " ")

        if self.incoming_text_message == "" and self.group:
            raise EmptyMessageInGroup("Message is empty in group.")
        elif self.sender not in appSettings.admin_ids and self.sender in appSettings.blacklist_ids:
            raise SenderInBlackList("Sender is in blacklist.")
        elif self.sender not in appSettings.admin_ids and DEBUG:
            raise SenderNotAdmin("Sender is not an admin.")

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

            if appSettings.admin_command_prefix == self.arguments[0]:
                if self.sender in appSettings.admin_ids:
                    self.admin_privilege = True
                    self.arguments = self.arguments[1:]

    def set_media(self, data):
        if data["image"]:
            self.incoming_text_message = data["image"]["caption"].replace("\xa0", " ")
            self.media_mime_type = data["image"]["mime_type"]
            self.media_path = data["image"]["media_path"]

    @staticmethod
    def getGroupAndSenderId(string):
        if " in " in string:
            sender, group = string.split(" in ")
            if not group.endswith("@g.us"):
                sender, group = group, None
        else:
            sender, group = string, None
        return sender, group

    def send_message(self):
        for phone in self.send_to:
            body = {
                "phone": phone,
                "message": self.outgoing_text_message,
            }
            print(requests.post(appSettings.whatsapp_client_url + "send/message", data=body).text)

    def send_link(self):
        for phone in self.send_to:
            body = {
                "phone": phone,
                "caption": self.outgoing_text_message,
                "link": self.link,
            }
            print(requests.post(appSettings.whatsapp_client_url + "send/link", data=body).text)

    def send_file(self, caption=False):
        for phone in self.send_to:
            body = {
                "phone": phone,
                "caption": self.outgoing_text_message if caption else None,
            }
            print(requests.post(appSettings.whatsapp_client_url + "send/file", data=body, files=self.media).text)

    def send_audio(self, caption=False):
        for phone in self.send_to:
            body = {
                "phone": phone,
                "caption": self.outgoing_text_message if caption else None,
            }
            print(requests.post(appSettings.whatsapp_client_url + "send/audio", data=body, files=self.media).text)

    def send_image(self, caption=False):
        for phone in self.send_to:
            body = {
                "phone": phone,
                "caption": self.outgoing_text_message if caption else None,
            }
            print(requests.post(appSettings.whatsapp_client_url + "send/image", data=body, files=self.media).text)

    def send_video(self, caption=False):
        for phone in self.send_to:
            body = {
                "phone": phone,
                "caption": self.outgoing_text_message if caption else None,
            }
            print(requests.post(appSettings.whatsapp_client_url + "send/video", data=body, files=self.media).text)

    def send_media(self, caption=False):
        if self.media_mime_type == "audio/ogg":
            self.send_audio(caption)
        elif self.media_mime_type == "image/jpeg":
            self.send_image(caption)
        elif self.media_mime_type == "video/mp4":
            self.send_video(caption)
        else:
            self.send_file(caption)


class API:
    def __init__(self, data) -> None:
        self.request_timestamp = timezone.now()
        self.message = Message(data)
        self.plugins = Plugin.load_plugins()

        try:
            self.command_handle() if self.message.arguments else self.message_handle()
        except CommandNotFound or SenderNotAdmin as e:
            self.message.outgoing_text_message = e
            self.message.send_message()

    def message_handle(self):
        self.message.outgoing_text_message = "Hello, I am a bot. Use `/help` to see available commands."
        self.message.send_message()

    def command_handle(self):
        if (self.message.arguments == [""]) or (self.message.arguments[0] == "help"):
            self.send_help()

        elif self.plugins.get(self.message.arguments[0]):
            if self.plugins[self.message.arguments[0]].admin_privilege == self.message.admin_privilege:
                self.plugins[self.message.arguments[0]].handle_function(self.message)
            else:
                raise SenderNotAdmin("Sender is not an admin.")

        else:
            raise CommandNotFound(f"Command `{self.message.arguments[0]}` not found. Use `/help` to see available commands.")

    def send_help(self):
        help_message = {}
        prefix = appSettings.admin_command_prefix + " " if self.message.admin_privilege else ""
        for _, plugin in self.plugins.items():
            if plugin.admin_privilege == self.message.admin_privilege and not plugin.internal:
                help_message.update({prefix + plugin.command_name: plugin.description})
        help_message.update({prefix + "help": "Show this message."})

        self.message.outgoing_text_message = "*Available commands:*\n"
        for command, description in help_message.items():
            self.message.outgoing_text_message += f"- `/{command}`: {description}\n"
        self.message.send_message()
