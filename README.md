# Drink Water Reminder

![drinkwater](https://github.com/user-attachments/assets/cc559f3a-5c51-4fe3-9d0f-cbaaa8d7be46)


## Overview

Drink Water Reminder is a simple Python application designed to remind users to drink water throughout the day. It sends notifications at scheduled intervals and includes a system tray icon for easy access. The application utilizes the `plyer` library for cross-platform notifications and the `pystray` library for creating a system tray icon.

## Features

- **Scheduled Reminders**: Receive notifications every hour from 10 AM to 7 PM, reminding you to drink water.
- **System Tray Icon**: Runs in the background with a system tray icon for easy access and notifications.
- **Base64 Icon Embedding**: The application embeds an icon directly into the code as a Base64 string, eliminating the need for external icon files.
- **Cross-Platform Compatibility**: Built with Python, making it compatible with various operating systems.

## Dependencies

To run the application, ensure you have the following Python libraries installed:

- `schedule`: For scheduling reminders.
- `plyer`: For sending notifications.
- `pystray`: For creating the system tray icon.
- `Pillow`: For image processing.

You can install these dependencies using pip:

```bash
pip install schedule plyer pystray Pillow
```

Clone the Repository:
```bash
git clone https://github.com/yourusername/drink-water-reminder.git
cd drink-water-reminder
```


Run the Application:
```bash
python drinkwater.py
```

Create an Executable (optional):

To create a standalone executable, use PyInstaller:

```bash
pyinstaller --noconsole --onefile --hidden-import=plyer.platforms.win.notification drinkwater.py
```
