import tkinter as tk
from tkinter import filedialog
from tkinter import font
import os
import shutil
import configparser

# Set the working directory to the directory where the Python script is located
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Absolute path to the configuration file
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "nerevar_config.ini")

# Create a configuration file if it doesn't exist
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as configfile:
        configfile.write("[Paths]\n")
        configfile.write("Initialized = False\n")

# Load the configuration
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

def save_paths(mods_path, cfg_path):
    config["Paths"]["ModsPath"] = mods_path
    config["Paths"]["CfgPath"] = cfg_path
    config["Paths"]["Initialized"] = "True"
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)

def load_paths():
    mods_path = config["Paths"].get("ModsPath", "")
    cfg_path = config["Paths"].get("CfgPath", "")
    initialized = config["Paths"].get("Initialized", "False")
    return mods_path, cfg_path, initialized

def open_client_window(root):
    client_window = tk.Toplevel(root)
    client_window.title("Client Window")
    client_window.geometry("1000x800")

    # Function to browse for directory and populate entry field
    def browse_directory(entry):
        directory = filedialog.askdirectory()
        entry.delete(0, tk.END)  # Clear any existing text
        entry.insert(tk.END, directory)

    # Function to browse for file and populate entry field
    def browse_file(entry):
        file_path = filedialog.askopenfilename()
        entry.delete(0, tk.END)  # Clear any existing text
        entry.insert(tk.END, file_path)

    # Function to toggle clothing mode
    def toggle_clothing_mode():
        if clothing_mode.get() == 1:
            print("Clothed mode enabled")
        else:
            print("Nude mode enabled")

    # Function to change clothes
    def change_clothes():
        mods_folder_path = mods_folder_entry.get()
        if not mods_folder_path:
            print("Please select the 'morrowind-multiplayer-mods' folder first.")
            return

        clothing_mode_value = clothing_mode.get()
        if clothing_mode_value == 1:
            print("Clothed mode enabled")
            source_folder = os.path.join(mods_folder_path, "Body Options", "Underwear")
        else:
            print("Nude mode enabled")
            source_folder = os.path.join(mods_folder_path, "Body Options", "Nude")

        destination_folder = os.path.join(mods_folder_path, "Data Files")

        for root, dirs, files in os.walk(source_folder):
            relative_path = os.path.relpath(root, source_folder)
            destination_dir = os.path.join(destination_folder, relative_path)
            os.makedirs(destination_dir, exist_ok=True)
            for file in files:
                source_file = os.path.join(root, file)
                destination_file = os.path.join(destination_dir, file)
                shutil.copy2(source_file, destination_file)

        print("Clothes changed successfully.")

    # Function to apply CFG changes
    def apply_cfg_changes():
        # Get the path of CFGAdditions.txt and openmw.cfg
        cfg_additions_file = "CFGAdditions.txt"
        openmw_cfg_path = openmw_cfg_entry.get()
        mods_folder_path = mods_folder_entry.get()

        # Check if openmw.cfg is provided
        if not openmw_cfg_path:
            print("Please select the 'openmw.cfg' file first.")
            return

        # Check if CFGAdditions.txt exists
        if not os.path.exists(cfg_additions_file):
            print(f"'{cfg_additions_file}' not found.")
            return

        try:
            # Read the contents of CFGAdditions.txt
            with open(cfg_additions_file, "r") as f:
                cfg_additions = f.read()

            # Append the modified directory path and CFGAdditions.txt contents to openmw.cfg
            with open(openmw_cfg_path, "a") as f:
                # Add data path only if it's available
                data_path = apply_data_path()
                if data_path:
                    f.write(data_path)
                f.write(cfg_additions)

            print("CFG changes applied successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Update the openmw.cfg field with the appended changes
        openmw_cfg_entry.delete(0, tk.END)
        openmw_cfg_entry.insert(tk.END, openmw_cfg_path)

    # Function to apply Data Path
    def apply_data_path():
        mods_folder_path = mods_folder_entry.get()
        if not mods_folder_path:
            print("Please select the 'morrowind-multiplayer-mods' folder first.")
            return ""

        openmw_cfg_path = openmw_cfg_entry.get()
        if not openmw_cfg_path:
            print("Please select the 'openmw.cfg' file first.")
            return ""

        # Modify the directory path
        directory_line = f"\ndata=\"{mods_folder_path}/Data Files\"\n"
        
        print("Data Path applied successfully.")
        return directory_line

    # Function to copy settings.cfg
    def copy_settings_cfg():
        mods_folder_path = mods_folder_entry.get()
        openmw_cfg_path = openmw_cfg_entry.get()
        if not openmw_cfg_path:
            print("Please select the 'openmw.cfg' file first.")
            return

    # Get the directory where the global openmw.cfg is located
        cfg_directory = os.path.dirname(openmw_cfg_path)

    # Path to settings.cfg in the working directory
        settings_cfg_path = os.path.join(os.path.dirname(__file__), "settings.cfg")

        if not os.path.exists(settings_cfg_path):
            print("settings.cfg not found in the working directory.")
            return

        shutil.copy2(settings_cfg_path, cfg_directory)
        print("settings.cfg copied successfully.")

    # Label and entry field for Morrowind Multiplayer Mods folder
    mods_folder_label = tk.Label(client_window, text="Locate your 'morrowind-multiplayer-mods' folder")
    mods_folder_label.pack(pady=5)
    mods_folder_entry = tk.Entry(client_window, width=50)
    mods_folder_entry.pack()

    # Load the saved mods path
    mods_path, _, initialized = load_paths()
    mods_folder_entry.insert(tk.END, mods_path)

    mods_folder_button = tk.Button(client_window, text="Browse", command=lambda: browse_directory(mods_folder_entry))
    mods_folder_button.pack()

    # Label and entry field for OpenMW.cfg
    openmw_cfg_label = tk.Label(client_window, text="Locate your global openmw.cfg")
    openmw_cfg_label.pack(pady=5)
    openmw_cfg_entry = tk.Entry(client_window, width=50)
    openmw_cfg_entry.pack()

    openmw_cfg_button = tk.Button(client_window, text="Browse", command=lambda: browse_file(openmw_cfg_entry))
    openmw_cfg_button.pack()

    # Add space
    tk.Label(client_window, text="").pack()

    # Toggle switch for clothing mode
    clothing_mode = tk.IntVar()
    clothing_mode.set(1)  # Set default value to 'Clothed'
    clothing_mode_label = tk.Label(client_window, text="Clothing Mode:")
    clothing_mode_label.pack(pady=5)
    clothing_mode_frame = tk.Frame(client_window)
    clothing_mode_frame.pack()
    clothing_mode_nude = tk.Radiobutton(clothing_mode_frame, text="Nude", variable=clothing_mode, value=0, command=toggle_clothing_mode)
    clothing_mode_nude.pack(side=tk.LEFT)
    clothing_mode_clothed = tk.Radiobutton(clothing_mode_frame, text="Clothed", variable=clothing_mode, value=1, command=toggle_clothing_mode)
    clothing_mode_clothed.pack(side=tk.LEFT)

    # Add space
    tk.Label(client_window, text="").pack()

    # Button to change clothes
    change_clothes_button = tk.Button(client_window, text="Change Clothes Now", command=change_clothes)
    change_clothes_button.pack()

    # Add space
    tk.Label(client_window, text="").pack()

    # Button to apply Data Path
    apply_data_path_button = tk.Button(client_window, text="Apply Data Path", command=apply_data_path)
    apply_data_path_button.pack()

    # Add space
    tk.Label(client_window, text="").pack()

    # Button to apply CFG changes
    apply_cfg_changes_button = tk.Button(client_window, text="Apply CFG Changes", command=apply_cfg_changes)
    apply_cfg_changes_button.pack()

    # Add space
    tk.Label(client_window, text="").pack()

    # Button to copy settings.cfg
    copy_settings_cfg_button = tk.Button(client_window, text="Copy settings.cfg", command=copy_settings_cfg)
    copy_settings_cfg_button.pack()

    # Save paths when the window closes
    client_window.protocol("WM_DELETE_WINDOW", lambda: save_paths(mods_folder_entry.get(), openmw_cfg_entry.get()))

def main():
    root = tk.Tk()
    root.title("Nerevar")

    # Calculate the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set the initial size of the window
    window_width = 700
    window_height = 700

    # Calculate the position of the window
    window_x = (screen_width - window_width) // 2
    window_y = (screen_height - window_height) // 2

    # Set the window geometry
    root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    # Get the path to the font file
    font_path = os.path.join(os.path.dirname(__file__), "SovngardeLight.ttf")

    # Load the custom font
    custom_font = font.Font(family="SovngardeLight", size=24)

    # Create buttons with custom font
    client_button = tk.Button(root, text="Client", font=custom_font, width=10, command=lambda: open_client_window(root))
    client_button.pack(expand=True)
    server_button = tk.Button(root, text="Server", font=custom_font, width=10)
    server_button.pack(expand=True)

    # Load saved paths
    _, _, initialized = load_paths()

    # Pre-populate paths if available
    if initialized.lower() == "false":
        client_button.invoke()  # Open client window automatically

    root.mainloop()

if __name__ == "__main__":
    main()
