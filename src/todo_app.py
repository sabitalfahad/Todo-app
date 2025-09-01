from functions import TodoApp
import FreeSimpleGUI as sg
import datetime

# Initialize the Todo app
app = TodoApp()
sg.theme("BluePurple")

# Get current date to display in the footer
date_now = datetime.datetime.now().strftime("%A, %B %d, %Y")
footer = sg.Push(), sg.Text(f"Date: {date_now}", font=("Helvetica", 10), text_color="gray")

# Create GUI elements
label = sg.Text("Type a To-Do:")
input_box = sg.InputText(tooltip="Enter todo", key="todo")
list_box = sg.Listbox(values=app.get_all(), key="todos", enable_events=False, size=(45, 10))
add_button = sg.Button("Add")
edit_button = sg.Button("Edit")
complete_button = sg.Button("Complete")

# Organize elements in a layout
layout = [
    [label],
    [input_box, add_button],
    [list_box],
    [edit_button, complete_button],
    footer
]

# Create the window
window = sg.Window("Your Todos", layout, font=("Helvetica", 12))

# Start the event loop
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    # Add a new todo when Add button is clicked or Enter is pressed
    elif event == "Add" or event == "todo":
        todo_text = values["todo"].strip()
        if todo_text:
            app.add(todo_text)
            window["todo"].update(value="")          # Clear the input box
            list_box.update(values=app.get_all())    # Refresh the list
        else:
            sg.Popup("Please enter a todo", font=("Helvetica", 12))

    # Edit a selected todo when Edit button is clicked
    elif event == "Edit":
        selected = values["todos"]
        if selected:
            current_todo = selected[0]
            new_todo = sg.PopupGetText("Edit your todo", default_text=current_todo)
            if new_todo and new_todo.strip():
                index = app.get_all().index(current_todo)
                app.edit(index, new_todo.strip())      # Update the todo
                window["todo"].update(value="")        # Clear input box
                list_box.update(values=app.get_all())  # Refresh the list
            else:
                sg.Popup("Please enter a new value", font=("Helvetica", 12))
        else:
            sg.Popup("Please select a todo to edit", font=("Helvetica", 12))

    # Complete a selected todo
    elif event == "Complete":
        selected = values["todos"]
        if selected:
            todo_name = selected[0]
            confirm = sg.PopupYesNo(f"Mark '{todo_name}' as complete?", font=("Helvetica", 12))
            if confirm == "Yes":
                index = app.get_all().index(todo_name)
                app.complete(index)
                list_box.update(values=app.get_all())  # Refresh the list
        else:
            sg.Popup("Please select a todo to complete", font=("Helvetica", 12))

# Close the window when the user exits
window.close()
