import time

import flet as ft
from flet_core import FontWeight


class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type


class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = "start"
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user_name)),
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name),
            ),
            ft.Column(
                [
                    ft.Text(message.user_name, weight=FontWeight.BOLD),
                    ft.Text(message.text, selectable=True),
                ],
                tight=True,
                spacing=10,
            ),
        ]

    def get_text(self):
        return self.controls[1].controls[1].value

    def get_user_name(self):
        return self.controls[1].controls[0].value

    def get_initials(self, user_name: str):
        return user_name[:1].capitalize()

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]


def send_message(from_user: str, text: str, chat, page, input_field):
    message = Message(
        from_user,
        text,
        message_type="chat_message",
    )
    chat_message = ChatMessage(message)
    chat.controls.append(chat_message)
    input_field.value = ""
    page.update()


def get_chat_messages(chat, user_name):
    return [
        chat_message
        for chat_message in chat.controls
        if chat_message.get_user_name() == user_name
    ]


def get_last_message(chat, user_name):
    return get_all_messages(chat, user_name)[-1]


def get_all_messages(chat, user_name):
    return [
        chat_message.get_text() for chat_message in get_chat_messages(chat, user_name)
    ]


def main(page: ft.Page):
    page.horizontal_alignment = "stretch"
    page.title = "Flet Chat"
    page.session.set("user_name", "User")

    def send_message_click(e):
        if input_field.value != "":
            send_message(
                from_user=page.session.get("user_name"),
                text=input_field.value,
                chat=chat,
                page=page,
                input_field=input_field,
            )
            # time.sleep(2)
            send_message(
                from_user="Bot",
                text=f"You last message was: {get_last_message(chat, page.session.get('user_name'))}. \n"
                f"Total messages: {len(get_all_messages(chat, page.session.get('user_name')))}",
                chat=chat,
                page=page,
                input_field=input_field,
            )

    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    # A new message entry form
    input_field = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    # Add everything to the page
    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        ft.Row(
            [
                input_field,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=send_message_click,
                ),
            ]
        ),
    )


ft.app(port=8550, target=main, view=ft.WEB_BROWSER)
