import io
import os
import sys
import time
from enum import IntEnum
from threading import (
    Thread,
    Event,
)
from controls import (
    SEND_REQUEST_KEY,
    VOICE,
)

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from prompt_toolkit.shortcuts import (
    button_dialog,
    input_dialog,
    radiolist_dialog,
)
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style

from constants import *
from main import run

console = Console()

stop_event = Event() # event flag indicating translator thread should terminate


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
        text="Enter your OpenAI API Key:",
    ).run()
    if api_key:
        save_api_key(api_key)
        return api_key
    return None


def in_terminal():
    return sys.stdin.isatty() and sys.stdout.isatty()


def run_main_app(logfile_path="translation.log", verbose: bool = False):

    if not verbose:
        # configure logging for run thread
        with open(logfile_path, 'w', encoding='utf-8') as f:
            pass

        class FileWriter(io.StringIO):
            def __init__(self, file_path):
                super().__init__()
                self.file_path = file_path

            def write(self, msg):
                if msg.strip():
                    with open(self.file_path, 'a', encoding='utf-8') as f:
                        f.write(msg + '\n')

    def target():
        try:
            if not verbose:
                sys.stdout = FileWriter(logfile_path)

            run(stop_event)
        finally:
            sys.stdout = sys.__stdout__

    thread = Thread(target=target, daemon=True)
    thread.start()
    return thread


def settings_page():
    api_key = prompt_for_api_key()
    if api_key:
        console.print("[bold green]API key saved successfully![/bold green]")
    else:
        console.print("[bold red]No API key entered.[/bold red]")
    time.sleep(1)


def choose_languages(cur_source: str = "", cur_target: str = "") -> (str, str):
    source = radiolist_dialog(
        title="Source Language",
        text="Choose the language to translate from:",
        values=LANGUAGES,
        default=cur_source,
    ).run()

    if not source:
        return None, None

    target = radiolist_dialog(
        title="Target Language",
        text="Choose the language to translate to:",
        values=LANGUAGES,
        default=cur_target,
    ).run()

    return source, target


def save_language_choices(source_code, target_code):
    with open("controls.py", "w") as f:
        f.write(f"SOURCE_LANGUAGE = \"{source_code}\"\n")
        f.write(f"TARGET_LANGUAGE = \"{target_code}\"\n")
        f.write(f"SEND_REQUEST_KEY = \"{SEND_REQUEST_KEY}\"\n")  # preserve current key
        f.write(f"VOICE = \"{VOICE}\"\n")


def show_title():
    console.clear()
    console.print(Rule(style="cyan"))
    console.print(Panel(Text(ASCII_LOGO, justify="center", style="bold magenta"),
                        expand=False, border_style="bright_blue"))
    console.print(Rule(style="cyan"))


def main_menu(verbose: bool = False):
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

                from controls import __dict__ as controls_dict
                source, target = choose_languages(controls_dict["SOURCE_LANGUAGE"],
                                                  controls_dict["TARGET_LANGUAGE"])
                if not source or not target:
                    continue  # user cancelled

                controls_dict["SOURCE_LANGUAGE"] = source
                controls_dict["TARGET_LANGUAGE"] = target

                save_language_choices(source, target)

                thread = run_main_app(verbose=verbose)

                style = Style.from_dict({
                    "bold": "bold",
                    "dialog frame.label": "bold",
                })

                msg = FormattedText([
                    ("", f"🌐 Translating {source.upper()} ➝ {target.upper()} - Press "),
                    ("bold", SEND_REQUEST_KEY),
                    ("", " to translate!"),
                ])

                action = button_dialog(
                    title="Translator Running...",
                    text=msg,
                    buttons=[("Main Menu", "back"), ("Exit App", "exit")],
                    style=style,
                ).run()

                stop_event.set()
                thread.join()
                stop_event.clear()

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
        from cli_fallback import fallback_main_menu
        fallback_main_menu()
