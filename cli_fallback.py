from cli import *


def choose_languages_fallback(cur_source: str, cur_target: str) -> (str, str):
    source = input(f"Enter a source language code (default: {cur_source}): ")

    if not source:
        source = cur_source

    if source not in [code for code, _ in LANGUAGES]:
        print("ERROR: Invalid Language Code")
        return None, None

    target = input(f"Enter a target language code (default: {cur_target}): ")

    if not target:
        target = cur_target

    if target not in [code for code, _ in LANGUAGES]:
        print("ERROR: Invalid Language Code")
        return None, None

    return source, target


def fallback_main_menu(verbose: bool = True):
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

                from controls import __dict__ as controls_dict
                source, target = choose_languages_fallback(
                    controls_dict["SOURCE_LANGUAGE"],
                    controls_dict["TARGET_LANGUAGE"],
                )

                if not source or not target:
                    continue  # user cancelled

                controls_dict["SOURCE_LANGUAGE"] = source
                controls_dict["TARGET_LANGUAGE"] = target

                save_language_choices(source, target)

                thread = run_main_app(verbose=verbose)

                print(f"🌐 Translating {source.upper()} ➝ "
                         f"{target.upper()} - "
                         f"Press {SEND_REQUEST_KEY} to translate!")

                try:
                    input("[running] Enter any key to return to main menu.\n")
                except KeyboardInterrupt:
                    continue

                stop_event.set()
                thread.join()
                stop_event.clear()

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


if __name__ == "__main__":
    fallback_main_menu()
