import os
import sys
from plyer import notification
from settingsManager import read_popup_settings, read_sound_settings
from soundPlayer import play_sound
from tkinterPopup import show_notification_async


def popup(message, duration):
    type = read_popup_settings()

    match type:
        case "system":
            if sys.platform.startswith("linux"):
                os.system(f'notify-send --expire-time={duration} "{message}"')
            elif sys.platform.startswith("darwin"):
                os.system(
                    f'osascript -e \'display notification "{message}" with title "Notification"\''
                )
            elif sys.platform.startswith("win"):
                # Use plyer for Windows notifications
                notification.notify(
                    title="VecchioGPT",
                    message=message,
                    timeout=duration // 1000,  # Convert milliseconds to seconds
                )
            else:
                print(message)
        case "vecchio":
            show_notification_async(message, duration)
        case "off":
            return
        case _:
            return


def sound(filename):
    enabled = read_sound_settings()
    if enabled:
        play_sound(filename)