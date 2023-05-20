# Import the necessary modules
import customtkinter  # Custom tkinter library
from captureIa import exe
from creatDataset import creatdataset
from cnnAlgo import CNNTest
# from PIL import Image, ImageTk
import json
import os
import tkinter.filedialog as filedialog
import shutil

# Set the appearance mode of the app to match the system's appearance
customtkinter.set_appearance_mode("System")

# Set the default color theme of the app to green
customtkinter.set_default_color_theme("green")

# Create the app
app = customtkinter.CTk()

# Set the geometry (size) of the app window
app.geometry("600x330")

# Set the title of the app
app.title("wires detector")


# Set the icon of the app
# app.iconbitmap("C:\\Users\\Administrator\\Desktop\\Work\\last iapo\\pfeIaA\\img\\IALogo.ico")

# creat the dataset from images
# creatdataset()

# Define the function to be called when the "Tester" button is clicked
def button_event():
    # Call the webcam execution function

    dataPath = "./dataset/" + optionmenu_1.get() + "/" + optionmenu_1.get() + ".txt"
    print(dataPath)

    # Open the file for reading
    with open(dataPath, 'r') as f:
        # Read the contents of the file into a string variable
        file_contents = f.read()

    # Load the dictionary from the file contents using json.loads
    my_dict = json.loads(file_contents)

    # Call the exe function with the dictionary object
    exe(my_dict)


# Define the function to be called when the app is closed
def close_event():
    # Add any code to run before closing the app here
    app.destroy()


def help_event():
    # Create the new window
    new_window = customtkinter.CTk()
    new_window.geometry("300x150")
    new_window.title("Detect connecteur")
    # new_window.iconbitmap("./img/IALogo.ico")

    global selected_files
    selected_files = None
    button_submit = None  # Define button_submit before the nested functions

    # Define a function to handle the button click event
    def select_files():
        nonlocal button_submit
        filetypes = (("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*"))
        selected_file = filedialog.askopenfilename(title="Select Photo", filetypes=filetypes)
        if selected_file:
            global selected_files
            selected_files = selected_file
            button_submit.configure(state="normal")
        else:
            images_label.configure(text="Image du connecteur: No file selected.")
            button_submit.configure(state="disabled")

    def submit():
        global selected_files
        if selected_files:
            # print(selected_files)
            # print(CNNTest(selected_files))
            optionmenu_1.set(CNNTest(selected_files))

            new_window.destroy()
        else:
            customtkinter.messagebox.showerror("Error", "No file selected.")

    # Add an input field for connector images
    images_label = customtkinter.CTkLabel(new_window, text="sélectionner l'image du connecteur")
    images_label.pack(pady=5)
    button = customtkinter.CTkButton(new_window, text="Select Photos", command=select_files)
    button.pack(pady=5)

    # Add a button to submit the form
    button_submit = customtkinter.CTkButton(new_window, text="Detecter connector", command=submit, state="disabled")
    button_submit.pack(pady=10)

    # Display the new window
    new_window.mainloop()


def open_new_window():
    # Create the new window
    new_window = customtkinter.CTk()
    new_window.geometry("400x340")
    new_window.title("Ajouter connecteur")
    # new_window.iconbitmap("./img/IALogo.ico")
    selected_files = None

    # Define a function to handle the button click event
    def select_files():
        nonlocal selected_files
        filetypes = (("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*"))
        selected_files = filedialog.askopenfilenames(title="Select Photos", filetypes=filetypes)
        if selected_files:
            num_files = len(selected_files)
            images_label.configure(
                text=f"images du connecteur: {num_files} file{'s' if num_files != 1 else ''} selected.")
        else:
            images_label.configure(text="images du connecteur: No files selected.")

    def submit():
        reference = reference_input_field.get()
        colors_list = color_num_input.get().split(",")
        valid_colors = ["black", "brown", "red", "orange", "yellow", "green", "blue", "purple", "white"]
        colors = {str(i + 1): color.strip() for i, color in enumerate(colors_list)}

        # Check if all colors are valid
        for color in colors.values():
            if color not in valid_colors:
                customtkinter.messagebox.showerror("Error", f"{color} is not a valid color.")
                return

        folder_name = f"{reference}_images"
        folder_name = os.path.join("connector_images", folder_name)
        images_folder_path = os.path.join(os.getcwd(), folder_name)
        if not os.path.exists(images_folder_path):
            os.makedirs(images_folder_path)  # use makedirs to create all necessary parent directories

        for file_path in selected_files:
            file_name = os.path.basename(file_path)
            new_file_path = os.path.join(images_folder_path, file_name)
            shutil.copy(file_path, new_file_path)

        dataset_folder_path = os.path.join("dataset", reference)
        os.makedirs(dataset_folder_path, exist_ok=True)  # use makedirs to create all necessary parent directories
        file_name = reference + ".txt"
        dataPath = os.path.join(dataset_folder_path, file_name)
        with open(dataPath, 'w') as f:
            json.dump(colors, f)
        # creat the dataset from images
        creatdataset()
        new_window.destroy()

    # Add an input field for reference
    reference_input = customtkinter.StringVar()
    reference_label = customtkinter.CTkLabel(new_window, text="Référence du connecteur:")
    reference_label.pack(pady=5)
    reference_input_field = customtkinter.CTkEntry(new_window, textvariable=reference_input)
    reference_input_field.pack(pady=5)

    # Add an input field for connector images
    images_label = customtkinter.CTkLabel(new_window, text="images du connecteur:")
    images_label.pack(pady=5)
    button = customtkinter.CTkButton(new_window, text="Select Photos", command=select_files)
    button.pack(pady=5)

    # Add an input field for number of colors
    color_num_label = customtkinter.CTkLabel(new_window, text="les couleurs dans l'ordre:")
    color_num_label.pack(pady=5)
    color_num_input = customtkinter.CTkEntry(new_window)
    color_num_input.pack(pady=5)

    # Add a button to submit the form
    button_submit = customtkinter.CTkButton(new_window, text="Enregistrer", command=submit)
    button_submit.pack(pady=10)

    # available colors
    color_num_label = customtkinter.CTkLabel(new_window,
                                             text="les couleurs disponibles\n\nblack, brown, red, orange, yellow, green, blue, purple, white")
    color_num_label.pack(pady=5)

    # Display the new window
    new_window.mainloop()


# Create a frame within the app
frame_1 = customtkinter.CTkFrame(master=app)

# Set the padding and expansion properties of the frame
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

# Create a label within the frame with some text and formatting properties
label_1 = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT, text="connecteur electrique",
                                 font=customtkinter.CTkFont(family='Courier New', size=24))
# Set the padding and expansion properties of the label
label_1.pack(pady=10, padx=10)

logo_button = customtkinter.CTkButton(master=frame_1, text="Ajouter connecteur", command=open_new_window)
logo_button.pack(pady=10, padx=10)

# the dataset directory
connecteur_dir = 'dataset'  # Replace with the actual path to the directory

# Create a dictionary with the file names as keys and their paths as values
file_dict = {}
for root, dirs, files in os.walk(connecteur_dir):
    for file in files:
        file_path = os.path.join(root, file)
        filename, file_extension = os.path.splitext(file)
        if file_extension == ".txt":
            file_dict[filename] = file_path

# Pass the dictionary keys to the CTkOptionMenu
optionmenu_1 = customtkinter.CTkOptionMenu(frame_1, values=list(file_dict.keys()),
                                           font=customtkinter.CTkFont(family='Courier New', size=18))
optionmenu_1.pack()

# Set the default value of the option menu
optionmenu_1.set("Référence")

# Create a button within the frame with some text and formatting properties, and bind it to the button_event function
button_1 = customtkinter.CTkButton(master=frame_1, font=customtkinter.CTkFont(family='Courier New', size=18),
                                   command=button_event, text="Tester")

# Set the padding and expansion properties of the button
button_1.pack(pady=10, padx=10)

# Add an input field for number of colors
help_label = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT,
                                    text="Si vous ne connaissez pas le numéro de référence,\n           cliquez sur le bouton Aide.",
                                    font=customtkinter.CTkFont(family='Courier New', size=12))
help_label.pack(pady=10, padx=10)
help_input = customtkinter.CTkButton(master=frame_1, font=customtkinter.CTkFont(family='Courier New', size=18),
                                     command=help_event, text="Aide")
help_input.pack(padx=10)

# Bind the close_event function to the app
app.protocol("WM_DELETE_WINDOW", close_event)

# Start the main loop of the app
app.mainloop()
