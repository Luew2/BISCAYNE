import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import json
import subprocess
from PIL import Image, ImageTk
from tkinter import messagebox  # Add this import



# Set the root directory of the project
project_root_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.join(project_root_dir, '..')  # Move up one directory to get the project root
project_root_dir = os.path.normpath(project_root_dir)  # Normalize the path

# Define the variables globally
openai_api_key_entry = None
elvenlabs_api_key_entry = None
settings_window = None  # Define settings_window globally
selected_image_path = ""

def create_character_class():
    # Implement character class creation logic here
    pass

def open_char_selection_window():
    char_selection_window = tk.Toplevel(root)
    char_selection_window.title("Select Character")

    # List to store character images (original.png or original_x.png)
    character_images = []

    # Function to update the list of character images
    def update_character_images():
        character_images.clear()
        for filename in os.listdir(os.path.join(project_root_dir, 'character')):
            if filename.startswith('original') and filename.endswith('.png'):
                character_images.append(filename)

    # Function to select a character
    def select_character():
        selected_image = character_images_listbox.get(character_images_listbox.curselection())
        char_details_window(selected_image)
        char_selection_window.destroy()  # Close the character selection window

    update_character_images()

    # Create a listbox to display character images
    character_images_listbox = tk.Listbox(char_selection_window, selectmode=tk.SINGLE, exportselection=0)
    for image in character_images:
        character_images_listbox.insert(tk.END, image)
    character_images_listbox.pack()

    # Create a button to select a character
    select_button = tk.Button(char_selection_window, text="Select Character", command=select_character)
    select_button.pack()

    # Create a label to display the selected character image
    selected_char_image = tk.Label(char_selection_window)
    selected_char_image.pack()

    # Function to update the displayed character image
    def update_selected_char_image():
        # Check if there is a selection in the listbox
        if character_images_listbox.curselection():
            selected_image = character_images_listbox.get(character_images_listbox.curselection())
            image_path = os.path.join(project_root_dir, 'character', selected_image)
            char_img = Image.open(image_path)
            char_img.thumbnail((150, 150))  # Resize the image to fit the label
            char_img = ImageTk.PhotoImage(char_img)
            selected_char_image.config(image=char_img)
            selected_char_image.image = char_img

    # Bind a selection event to update the displayed character image
    character_images_listbox.bind('<<ListboxSelect>>', lambda event: update_selected_char_image())

    # Update the selected character image initially
    if character_images:
        update_selected_char_image()

def char_details_window(selected_image):
    char_details_window = tk.Toplevel(root)
    char_details_window.title("Character Details")

    # Create labels and entry fields for character details
    char_name_label = ttk.Label(char_details_window, text="Name:")
    char_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    char_name_entry = ttk.Entry(char_details_window)
    char_name_entry.grid(row=0, column=1, padx=10, pady=5)

    char_class_label = ttk.Label(char_details_window, text="Class:")
    char_class_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    char_class_entry = ttk.Entry(char_details_window)
    char_class_entry.grid(row=1, column=1, padx=10, pady=5)

    char_race_label = ttk.Label(char_details_window, text="Race:")
    char_race_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    char_race_entry = ttk.Entry(char_details_window)
    char_race_entry.grid(row=2, column=1, padx=10, pady=5)

    char_level_label = ttk.Label(char_details_window, text="Level:")
    char_level_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    char_level_entry = ttk.Entry(char_details_window)
    char_level_entry.grid(row=3, column=1, padx=10, pady=5)

    char_hp_label = ttk.Label(char_details_window, text="HP:")
    char_hp_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    char_hp_entry = ttk.Entry(char_details_window)
    char_hp_entry.grid(row=4, column=1, padx=10, pady=5)

    char_mana_label = ttk.Label(char_details_window, text="Mana:")
    char_mana_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    char_mana_entry = ttk.Entry(char_details_window)
    char_mana_entry.grid(row=5, column=1, padx=10, pady=5)

    char_inventory_label = ttk.Label(char_details_window, text="Inventory (comma-separated):")
    char_inventory_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
    char_inventory_entry = ttk.Entry(char_details_window)
    char_inventory_entry.grid(row=6, column=1, padx=10, pady=5)

    # Entry field for Eleven Labs Voice ID
    char_voice_label = ttk.Label(char_details_window, text="Eleven Labs Voice ID:")
    char_voice_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
    char_voice_entry = ttk.Entry(char_details_window)
    char_voice_entry.grid(row=7, column=1, padx=10, pady=5)

    # Entry field for AI System Message
    char_ai_system_msg_label = ttk.Label(char_details_window, text="AI System Message:")
    char_ai_system_msg_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")
    char_ai_system_msg_entry = ttk.Entry(char_details_window)
    char_ai_system_msg_entry.grid(row=8, column=1, padx=10, pady=5)

    def save_character_details():
        char_details = {
            "name": char_name_entry.get(),
            "class": char_class_entry.get(),
            "race": char_race_entry.get(),
            "level": char_level_entry.get(),
            "hp": char_hp_entry.get(),
            "mana": char_mana_entry.get(),
            "inventory": [item.strip() for item in char_inventory_entry.get().split(',')],
            "voice": char_voice_entry.get(),  # Get the entered AI voice ID
            "ai_system_message": char_ai_system_msg_entry.get()  # Get the entered AI System Message
        }

        
        # Add image paths
        char_details["image"] = selected_image
        char_details["without_mouth"] = selected_image.replace("original", "without_mouth")
        char_details["mouth"] = selected_image.replace("original", "mouth")

        # Save character details as JSON
        with open(os.path.join(project_root_dir, 'config', f'{char_name_entry.get()}_char_details.json'), 'w') as json_file:
            json.dump(char_details, json_file, indent=4)
        
        char_details_window.destroy()  # Close the character details window

    save_button = ttk.Button(char_details_window, text="Save Character", command=save_character_details)
    save_button.grid(row=9, column=1, padx=10, pady=10)





def upload_ai_image():
    global selected_image_path
    # Implement image upload logic here
    file_path = filedialog.askopenfilename()
    selected_image_path = file_path  # Store the selected image path
    print(f"Uploaded image: {file_path}")
    char_creator = os.path.join(project_root_dir, 'src/char_creator.py')  # Path to the 'char_creator'
    
    # Open char_creator.py with the selected image path as an argument
    subprocess.Popen(["python3", char_creator, selected_image_path])

def start_ai():
    global selected_character_json

    def select_character():
        # Ensure the selected_character_json is global
        global selected_character_json

        # Get the selected character name from the dropdown
        selected_character_name = character_dropdown.get()

        # Check if a character with the selected name exists in the JSON files
        character_json_path = os.path.join(project_root_dir, 'config', f'{selected_character_name}.json')

        if not os.path.exists(character_json_path):
            messagebox.showerror("Error", f"Character '{selected_character_name}' not found.")
            return

        # Set the selected character JSON path
        selected_character_json = character_json_path

        print(selected_character_json)
        character_selection_window.destroy()  # Close the character selection window

        # Call main.py with the selected character JSON path as an argument
        subprocess.Popen(["python", "src/main.py", selected_character_json])


    # Create a new window for character selection
    character_selection_window = tk.Toplevel(root)
    character_selection_window.title("Select Character")

    # List all JSON files in the /config directory
    config_files = [filename for filename in os.listdir(os.path.join(project_root_dir, 'config')) if filename.endswith('.json')]

    # Extract character names from JSON files and populate the dropdown
    character_names = [os.path.splitext(filename)[0] for filename in config_files]
    character_dropdown = ttk.Combobox(character_selection_window, values=character_names)
    character_dropdown.pack()

    # Create a button to select a character and start AI
    select_button = tk.Button(character_selection_window, text="Select Character", command=select_character)
    select_button.pack()




# Function to save settings
def save_settings():
    global openai_api_key_entry, elvenlabs_api_key_entry, settings_window
    
    openai_api_key = openai_api_key_entry.get()
    elvenlabs_api_key = elvenlabs_api_key_entry.get()
    
    # Save the environment variables
    os.environ["OPENAI_API_KEY"] = openai_api_key
    os.environ["ELVENLABS_API_KEY"] = elvenlabs_api_key
    
    # Save the values to a .env file
    with open(os.path.join(project_root_dir, '.env'), "w") as env_file:
        env_file.write(f"OPENAI_API_KEY={openai_api_key}\n")
        env_file.write(f"ELVENLABS_API_KEY={elvenlabs_api_key}\n")

    settings_window.destroy()

# Create the main application window
root = tk.Tk()
root.title("AI Interaction")

# Upload AI Image button
upload_image_button = tk.Button(root, text="Upload AI Image", command=upload_ai_image)
upload_image_button.pack()

# Create Character Class button
create_character_button = tk.Button(root, text="Create Character Class", command=open_char_selection_window)
create_character_button.pack()

# Start AI button
start_ai_button = tk.Button(root, text="Start AI", command=start_ai)
start_ai_button.pack()

# API Key Settings
def open_settings():
    global openai_api_key_entry, elvenlabs_api_key_entry, settings_window
    
    settings_window = tk.Toplevel(root)
    settings_window.title("AI Control Panel")

    # Create labels and entry fields for API keys
    openai_api_key_label = ttk.Label(settings_window, text="OpenAI API Key:")
    openai_api_key_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    openai_api_key_entry = ttk.Entry(settings_window)
    openai_api_key_entry.grid(row=0, column=1, padx=10, pady=5)
    openai_api_key_entry.insert(0, os.environ.get("OPENAI_API_KEY", ""))

    elvenlabs_api_key_label = ttk.Label(settings_window, text="Elven Labs API Key:")
    elvenlabs_api_key_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    elvenlabs_api_key_entry = ttk.Entry(settings_window)
    elvenlabs_api_key_entry.grid(row=1, column=1, padx=10, pady=5)
    elvenlabs_api_key_entry.insert(0, os.environ.get("ELVENLABS_API_KEY", ""))

    # Create a Save button
    save_button = ttk.Button(settings_window, text="Save Settings", command=save_settings)
    save_button.grid(row=2, column=1, padx=10, pady=10, sticky="e")

# Create a Settings button
settings_button = tk.Button(root, text="Settings", command=open_settings)
settings_button.pack()


# Run the GUI main loop
root.mainloop()
