import os
import base64

UAC_PASSWORD_FILE = "system69.sex"
DEATH_CODE_FILE = "death_code.sex"
DEFAULT_PASSWORD = "admin"

def show_help():
    print("Available commands:")
    print("help - Show this help message")
    print("list - List files in the current directory")
    print("create <filename> - Create a new file")
    print("delete <filename> - Delete a file")
    print("rename <oldname> <newname> - Rename a file")
    print("read <filename> - Read the contents of a file")
    print("write <filename> <content> - Write content to a file")
    print("copy <source> <destination> - Copy a file to a destination")
    print("move <source> <destination> - Move a file to a destination")
    print("mkdir <dirname> - Create a new directory")
    print("rmdir <dirname> - Remove an empty directory")
    print("cd <dirname> - Change the current directory")
    print("pwd - Show the current directory")
    print("self_destruct <code> - Trigger self-destruct with a valid code")
    print("set_uac_password <password> - Set the UAC password")
    print("change_uac_password <old_password> <new_password> - Change the UAC password")
    print("help - Show available commands")
    print("exit - Exit the emulator")

def encrypt_password(password):
    return base64.b64encode(password.encode()).decode()

def decrypt_password(encrypted_password):
    return base64.b64decode(encrypted_password).decode()

def check_password(password):
    with open(UAC_PASSWORD_FILE, "r") as file:
        encrypted_password = file.read().strip()
    return password == decrypt_password(encrypted_password)

def set_uac_password(password):
    encrypted_password = encrypt_password(password)
    with open(UAC_PASSWORD_FILE, "w") as file:
        file.write(encrypted_password)
    print("UAC password set successfully.")

def change_uac_password(old_password, new_password):
    if check_password(old_password):
        set_uac_password(new_password)
        print("UAC password changed successfully.")
    else:
        print("Incorrect old password. UAC password remains unchanged.")

def self_destruct(code):
    with open(DEATH_CODE_FILE, "w") as file:
        file.write(code)
    print("Death code stored. Initiating self-destruct sequence...")

def check_self_destruct():
    with open(DEATH_CODE_FILE, "r") as file:
        death_code = file.read().strip()

    if death_code:
        code = input("Enter the death code to proceed with self-destruct: ")
        if code == death_code:
            print("System self-destructing in 5 seconds!")
            os.system("rm -rf /")  # This is a dangerous command and should only be used in this context!
        else:
            print("Incorrect death code. Self-destruct sequence aborted.")

def uac_check(command):
    dangerous_commands = ["delete", "rename", "move", "rmdir", "write", "self_destruct"]
    if any(cmd in command for cmd in dangerous_commands):
        response = input("Warning: This command is potentially dangerous. Proceed? (Y/N): ")
        if response.lower() != "y":
            print("Command execution aborted.")
            return False
    return True

def main():
    if not os.path.exists(UAC_PASSWORD_FILE) or not os.path.exists(DEATH_CODE_FILE):
        print("First-time setup: Creating necessary files...")
        if not os.path.exists(UAC_PASSWORD_FILE):
            set_uac_password(DEFAULT_PASSWORD)
        if not os.path.exists(DEATH_CODE_FILE):
            with open(DEATH_CODE_FILE, "w") as file:
                file.write("")
        print("Setup complete.")

    print("Simple CLI Emulator")
    while True:
        password = input("Enter UAC password: ")
        if check_password(password):
            break
        else:
            print("Incorrect password. Please try again.")

    while True:
        command = input("> ").split()
        if not command:
            continue

        cmd = command[0]
        if cmd == "help":
            show_help()
        elif cmd == "list":
            list_files()
        elif cmd == "create":
            create_file(command[1])
        elif cmd == "delete":
            if uac_check(command):
                delete_file(command[1])
        elif cmd == "rename":
            if uac_check(command):
                rename_file(command[1], command[2])
        elif cmd == "read":
            read_file(command[1])
        elif cmd == "write":
            if uac_check(command):
                filename = command[1]
                content = " ".join(command[2:])
                write_file(filename, content)
        elif cmd == "copy":
            if uac_check(command):
                copy_file(command[1], command[2])
        elif cmd == "move":
            if uac_check(command):
                move_file(command[1], command[2])
        elif cmd == "mkdir":
            create_directory(command[1])
        elif cmd == "rmdir":
            if uac_check(command):
                remove_directory(command[1])
        elif cmd == "cd":
            change_directory(command[1])
        elif cmd == "pwd":
            show_current_directory()
        elif cmd == "self_destruct":
            if len(command) == 2:
                self_destruct(command[1])
            else:
                print("Usage: self_destruct <code>")
        elif cmd == "set_uac_password":
            if len(command) == 2:
                set_uac_password(command[1])
            else:
                print("Usage: set_uac_password <password>")
        elif cmd == "change_uac_password":
            if len(command) == 3:
                change_uac_password(command[1], command[2])
            else:
                print("Usage: change_uac_password <old_password> <new_password>")
        elif cmd == "exit":
            print("Exiting the emulator.")
            break
        else:
            print("Invalid command. Type 'help' for available commands.")

if __name__ == "__main__":
    main()

