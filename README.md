# 💧 Water Reminder App  

A modern desktop app to remind you to drink water during the day.  
Built with Python and CustomTkinter.  

---

## ✨ Features  

- **Hourly Reminders**  
  - Default schedule from **10 AM to 7 PM**  
  - Customizable hour slots with checkboxes  

- **Modern UI**  
  - Clean dark/light theme using **CustomTkinter**  

- **Notifications**  
  - Windows **toast notification** in bottom-right  
  - Popup window with reminder message, dismiss button, auto-close  

- **Voice Alert**  
  - Speaks “Time to drink water”  
  - If system is muted, app temporarily unmutes, plays alert, then restores mute state  

- **Do Not Disturb (DND)**  
  - Toggle button to silence reminders  

- **Minimize to Tray**  
  - Closing the window hides it to tray instead of quitting  
  - Tray menu options: Show, Toggle DND, Quit  

- **Daily Counter**  
  - Tracks how many times you drank water per day  
  - Reset button to start fresh each day  

---

## 🛠 Tech Stack  

- Python 3.10+  
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)  
- [pyttsx3](https://pypi.org/project/pyttsx3/)  
- [win10toast](https://pypi.org/project/win10toast/)  
- [schedule](https://pypi.org/project/schedule/)  
- [pystray](https://pypi.org/project/pystray/)  
- [pycaw](https://github.com/AndreMiras/pycaw)  

---

## 📦 Installation  

### 1. From Source (Python)  

Clone this repo:
```bash
git clone https://github.com/mokkabca/Drink-Water-Reminder.git

cd water-reminder
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the app:
```bash
python drinkwater.py
```
