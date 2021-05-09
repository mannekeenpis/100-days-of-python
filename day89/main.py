import tkinter as tk

win = tk.Tk()
win.title("Disappearing Text Writing App")

textbox = tk.Text(height=10, width=100)
textbox.insert(tk.END, "Default")
textbox.pack()

# This is for demonstration purposes
tk.Text(height=10, width=10).pack()


def default(event):
    current = textbox.get("1.0", tk.END)
    if current == "Default\n":
        textbox.delete("1.0", tk.END)
    elif current == "\n":
        textbox.insert("1.0", "Default")


textbox.bind("<FocusIn>", default)
textbox.bind("<FocusOut>", default)

tk.mainloop()