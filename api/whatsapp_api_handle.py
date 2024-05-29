from django.utils import timezone
import requests, re, os, json
from pathlib import Path
import importlib.util
from .appSettings import appSettings
from Whatsapp_API.settings import DEBUG

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
    def __init__(self, data):
        self.senderId, self.groupId = self.getGroupAndSenderId(data["from"])
        self.sender, self.group = map(lambda id: re.sub(r"^(\d+).*[:@].*$", r"\1", id) if id else None, [self.senderId, self.groupId])
        self.arguments = None
        self.admin_privilege = False
        self.incoming_text_message = self.get_incoming_text_message(data)
        self.outgoing_text_message = None
        self.send_to = [self.senderId if self.groupId is None else self.groupId]
        self.document = data.get("document")
        self.files = None

    def get_incoming_text_message(self, data):
        incoming_text_message = data["message"]["text"].replace("\xa0", " ")
        if incoming_text_message == "" and self.group:
            raise EmptyMessageInGroup("Message is empty in group.")
        elif self.sender not in appSettings.admin_ids and self.sender in appSettings.blacklist_ids:
            raise SenderInBlackList("Sender is in blacklist.")
        elif self.sender not in appSettings.admin_ids and DEBUG:
            raise SenderNotAdmin("Sender is not an admin.")

        if self.group:
            match = re.search(r"\.([^\.].*)", incoming_text_message)
            if match:
                incoming_text_message = str(match.group(1))
            else:
                raise EmptyMessageInGroup("Message is empty in group.")

        if incoming_text_message.startswith("/"):
            incoming_text_message = incoming_text_message[1:].strip()
            self.arguments = self.get_arguments(incoming_text_message)

            if appSettings.admin_command_prefix == self.arguments[0]:
                if self.sender in appSettings.admin_ids:
                    self.admin_privilege = True
                    self.arguments = self.arguments[1:]

        return incoming_text_message

    def get_arguments(self, command):
        arguments = []
        while command:
            if command[0] == '"':
                end = command.find('"', 1)
                arguments.append(command[: end + 1])
                command = command[end + 2 :]
            else:
                end = command.find(" ")
                if end == -1:
                    arguments.append(command)
                    break
                arguments.append(command[:end])
                command = command[end + 1 :]
        return arguments

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

    def send_file(self):
        for phone in self.send_to:
            body = {
                "phone": phone,
                "caption": self.outgoing_text_message,
            }
            print(requests.post(appSettings.whatsapp_client_url + "send/file", data=body, files=self.files).text)

    def send_audio(self):
        for phone in self.send_to:
            body = {
                "phone": phone,
                "message": self.outgoing_text_message,
            }
            print(requests.post(appSettings.whatsapp_client_url + "send/audio", data=body, files=self.files).text)

    def send_image(self):
        for phone in self.send_to:
            body = {
                "phone": phone,
                "message": self.outgoing_text_message,
            }
            print(requests.post(appSettings.whatsapp_client_url + "send/image", data=body, files=self.files).text)


class API:
    def __init__(self, data) -> None:
        self.request_timestamp = timezone.now()
        self.message = Message(data)
        self.plugins = Plugin.load_plugins()

        try:
            self.command_handle() if self.message.arguments else self.message_handle()

        except CommandNotFound or EmptyCommand or SenderNotAdmin as e:
            self.message.outgoing_text_message = e

        # except Exception as e:
        # self.message.outgoing_text_message = f"*Error:*\n```{e}```\n\nThis error has been reported to admins, please try again later in the next update."
        # self.message.send_message()

        # self.message.send_to = appSettings.get("adminIds")
        # self.message.outgoing_text_message = f"An error occurred while trying to process message from: {self.message.sender} in {self.message.group}.\nSender Name: ({data.get('pushname')})\n\n> {self.message.incoming_text_message.replace('\n', '\n> ')}\n\n```{e}```"
        # self.message.send_message()

    def message_handle(self):
        raise NotImplementedError("Message handling is not implemented.")  # TODO

    def command_handle(self):
        if (self.message.arguments == [""]) or (self.message.arguments[0] == "help"):
            self.set_help()
            self.message.send_message()

        elif self.plugins.get(self.message.arguments[0]):
            if self.plugins[self.message.arguments[0]].admin_privilege == self.message.admin_privilege:
                self.plugins[self.message.arguments[0]].handle_function(self.message)

        else:
            raise CommandNotFound(f"Command `{self.message.arguments[0]}` not found. Use `/help` to see available commands.")

    def set_help(self):
        help_message = []
        for _, plugin in self.plugins.items():
            if plugin.admin_privilege == self.message.admin_privilege and not plugin.internal:
                help_message.append(f"`{plugin.command_name}`: {plugin.description}")
        self.message.outgoing_text_message = f"*Available commands:*\n\n{'\n\n'.join(help_message)}"
