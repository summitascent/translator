import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from prompt_toolkit.shortcuts import button_dialog, input_dialog
# from threading import Thread

API_KEY_FILE = "api_key.txt"
console = Console()

ascii_art = r"""
::::::::::: :::::::::      :::     ::::    :::  ::::::::  :::            ::: ::::::::::: ::::::::  :::::::::  
    :+:     :+:    :+:   :+: :+:   :+:+:   :+: :+:    :+: :+:          :+: :+:   :+:    :+:    :+: :+:    :+: 
    +:+     +:+    +:+  +:+   +:+  :+:+:+  +:+ +:+        +:+         +:+   +:+  +:+    +:+    +:+ +:+    +:+ 
    +#+     +#++:++#:  +#++:++#++: +#+ +:+ +#+ +#++:++#++ +#+        +#++:++#++: +#+    +#+    +:+ +#++:++#:  
    +#+     +#+    +#+ +#+     +#+ +#+  +#+#+#        +#+ +#+        +#+     +#+ +#+    +#+    +#+ +#+    +#+ 
    #+#     #+#    #+# #+#     #+# #+#   #+#+# #+#    #+# #+#        #+#     #+# #+#    #+#    #+# #+#    #+# 
    ###     ###    ### ###     ### ###    ####  ########  ########## ###     ### ###     ########  ###    ### 
"""


def get_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, "r") as f:
            return f.read().strip()
    return None


def save_api_key(key):
    with open(API_KEY_FILE, "w") as f:
        f.write(key.strip())


def prompt_for_api_key():
    api_key = input_dialog(
        title="API Key Required",
        text="Enter your OPENAI API Key:"
    ).run()
    if api_key:
        save_api_key(api_key)
        return api_key
    return None


def run_main_app():
    # def background_task():
    #     while True:
    #         console.print("[green]Translator is running...[/green]")
    #         time.sleep(3)
    #
    # thread = Thread(target=background_task, daemon=True)
    # thread.start()

    result = button_dialog(
        title="App Running",
        text="What would you like to do?",
        buttons=[("Back to Menu", "back"), ("Exit App", "exit")],
    ).run()

    return result


def settings_page():
    api_key = prompt_for_api_key()
    if api_key:
        console.print("[bold green]API key saved successfully![/bold green]")
    else:
        console.print("[bold red]No API key entered.[/bold red]")
    time.sleep(1)


def show_title():
    console.clear()
    console.print(Rule(style="cyan"))
    console.print(Panel(Text(ascii_art, justify="center", style="bold magenta"), expand=False, border_style="bright_blue"))
    console.print(Rule(style="cyan"))


def main_menu():
    while True:
        console.clear()
        show_title()  # <- updated title

        choice = button_dialog(
            title="Main Menu",
            text="Choose an option:",
            buttons=[
                ("🚀 Start", "start"),
                ("⚙️ Settings", "settings"),
                ("📜 Credits", "credits"),
                ("❌ Exit", "exit"),
            ],
        ).run()

        if choice == "start":
            api_key = get_api_key()
            if not api_key:
                api_key = prompt_for_api_key()
                if not api_key:
                    continue  # user cancelled

            action = run_main_app()
            if action == "exit":
                break

        elif choice == "settings":
            settings_page()

        elif choice == "credits":
            console.print(Panel("Built with ❤️ by You", title="Credits"))
            time.sleep(2)

        elif choice == "exit":
            break


if __name__ == "__main__":
    main_menu()
