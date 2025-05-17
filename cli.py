import os
import sys
import time
from enum import IntEnum
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from prompt_toolkit.shortcuts import button_dialog, input_dialog
# from threading import Thread

API_KEY_FILE = "_secrets.py"
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


class MenuChoice(IntEnum):
    """
    Enumerates the available menu options used throughout the application.

    Values:
    - START (1): Begin the translation process. Prompts for API key if not set.
    - SETTINGS (2): Open the settings menu to configure the API key.
    - CREDITS (3): Display application credits.
    - EXIT (4): Exit the application cleanly.
    """
    START = 1
    SETTINGS = 2
    CREDITS = 3
    EXIT = 4


def get_api_key():
    if os.path.exists(API_KEY_FILE):
        try:
            import importlib.util

            spec = importlib.util.spec_from_file_location("_secrets", API_KEY_FILE)
            secrets = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(secrets)

            return getattr(secrets, "OPEN_AI_API_KEY", None)
        except Exception as e:
            console.print(f"[red]Failed to load API key: {e}[/red]")

    return None


def save_api_key(key):
    with open(API_KEY_FILE, "w") as f:
        f.write(f'OPEN_AI_API_KEY = "{key.strip()}"')


def prompt_for_api_key():
    api_key = input_dialog(
        title="API Key Required",
        text="Enter your OpenAI API Key:"
    ).run()
    if api_key:
        save_api_key(api_key)
        return api_key
    return None


def in_terminal():
    return sys.stdin.isatty() and sys.stdout.isatty()


def run_main_app():
    # def background_task():
    #     while True:
    #         console.print("[green]Translator is running...[/green]")
    #         time.sleep(3)
    #
    # thread = Thread(target=background_task, daemon=True)
    # thread.start()

    result = button_dialog(
        title="Translator Running...",
        # text="What would you like to do?",
        buttons=[("Main Menu", "back"), ("Exit App", "exit")],
    ).run()

    return result


def settings_page():
    api_key = prompt_for_api_key()
    if api_key:
        console.print("[bold green]API key saved successfully![/bold green]")
    else:
        console.print("[bold red]No API key entered.[/bold red]")
    time.sleep(1)


def fallback_main_menu():
    console.clear()
    console.rule("[bold red]Fallback Mode Activated")
    console.print("[yellow]You're not running this in a real terminal.[/yellow]")
    console.print("[green]Functionality is preserved, but UI is simplified.[/green]\n")

    while True:
        print("\n==== Translator ====")
        print("1. Start")
        print("2. Settings")
        print("3. Credits")
        print("4. Exit")

        choice = -1

        while choice not in MenuChoice:
                choice = input("Select an option (1-4): ").strip()

                if not choice.isnumeric():
                    continue

                choice = int(choice)
                if choice in MenuChoice:
                    break
                else:
                    print("Please enter a number between 1 and 4.")

        match choice:
            case MenuChoice.START:
                api_key = get_api_key()
                if not api_key:
                    api_key = input("Enter your OpenAI API Key: ").strip()
                    if api_key:
                        save_api_key(api_key)
                    else:
                        print("No key entered. Returning to menu.")
                        continue
                print("Translator is running in background...")

                try:
                    input("[running] Press any key to return to main menu.")
                except KeyboardInterrupt:
                    continue

            case MenuChoice.SETTINGS:
                key = input("Enter your OPENAI API Key: ").strip()
                if key:
                    save_api_key(key)
                    print("API key saved.")
                else:
                    print("No key entered.")

            case MenuChoice.CREDITS:
                print("Built by Brian (Wei Hao) Ma & Ryan B. Green")
                time.sleep(2)

            case MenuChoice.EXIT:
                print("Goodbye!")
                break

            case _:
                console.print("[red]Unknown menu choice[/red]")


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
                ("🚀 Start", MenuChoice.START),
                ("⚙️ Settings", MenuChoice.SETTINGS),
                ("📜 Credits", MenuChoice.CREDITS),
                ("❌ Exit", MenuChoice.EXIT),
            ],
        ).run()

        match choice:
            case MenuChoice.START:
                api_key = get_api_key()

                if not api_key:
                    api_key = prompt_for_api_key()
                    if not api_key:
                        continue  # user cancelled

                action = run_main_app()
                if action == "exit":
                    break

            case MenuChoice.SETTINGS:
                settings_page()

            case MenuChoice.CREDITS:
                console.print(Panel("Built by "
                                    "[blue]Brian (Wei Hao) Ma[/blue] & "
                                    "[green]Ryan B. Green[/green]",
                              title="Credits"))
                time.sleep(2)

            case MenuChoice.EXIT:
                break

            case _:
                console.print("[red]Unknown menu choice[/red]")


if __name__ == "__main__":
    if in_terminal():
        main_menu()
    else:
        fallback_main_menu()

