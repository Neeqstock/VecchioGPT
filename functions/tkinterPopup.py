import tkinter as tk
import threading


class NotificationPopup(tk.Toplevel):
    _instance = None  # Class variable to hold the current instance

    def __init__(self, master, message, duration=3000):
        super().__init__(master)
        self.message = message
        self.duration = duration
        self.setup_window()
        self.show_notification()

    def setup_window(self):
        self.overrideredirect(True)  # Remove window decorations (borderless)
        self.attributes("-topmost", True)  # Keep window on top
        self.configure(bg="black")  # Background color

        # Create a label to display the message
        self.label = tk.Label(self, text=self.message, fg="white", bg="black")
        self.label.pack(padx=10, pady=5)

        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Set window size and position
        self.update_idletasks()  # Update window "requested size" information
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        x = screen_width - window_width - 10
        y = screen_height - window_height - 10
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def show_notification(self):
        # Destroy the popup after the specified duration
        self.after(self.duration, self.destroy)
        NotificationPopup._instance = (
            self  # Update the class variable to the current instance
        )

    @classmethod
    def close_current(cls):
        if cls._instance is not None:
            cls._instance.destroy()  # Destroy the current instance
            cls._instance = None  # Reset the instance variable


def show_notification(message, duration=3000):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    NotificationPopup.close_current()  # Close any existing notification
    NotificationPopup(root, message, duration)
    root.mainloop()


def show_notification_async(message, duration=3000):
    threading.Thread(
        target=show_notification, args=(message, duration), daemon=True
    ).start()


# Example usage
if __name__ == "__main__":
    show_notification_async("This is a test notification", 3000)
    # Simulate calling a new notification after 1 second
    threading.Timer(
        1, lambda: show_notification_async("New notification after 1 second", 3000)
    ).start()
    # Keep the main thread alive to see the notifications
    threading.Event().wait(5)
