
import tkinter as tk
import speech_recognition as sr
from tkinter import messagebox
import threading  # To avoid freezing the UI during speech recognition

def Speech_to_Text(language):
    # Run the recognition in a separate thread
    threading.Thread(target=record_and_recognize, args=(language,), daemon=True).start()

def record_and_recognize(language):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        txtSpeech.insert(tk.END, "Listening...\n")  # Visual feedback
        txtSpeech.see(tk.END)  # Auto-scroll to the latest message
        root.update()  # Update the UI immediately
        
        r.adjust_for_ambient_noise(source)  # Adjust for background noise
        
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=10)  # Longer timeout
            txtSpeech.insert(tk.END, "Processing...\n")
            txtSpeech.see(tk.END)
            root.update()

            # Set the language for speech recognition
            language_code = "zh-CN" if language == 'Chinese' else "en-US"
            text = r.recognize_google(audio, language=language_code)
            
            txtSpeech.insert(tk.END, text + "\n")
            txtSpeech.see(tk.END)
        except sr.UnknownValueError:
            txtSpeech.insert(tk.END, "Could not understand audio.\n")
        except sr.RequestError as e:
            txtSpeech.insert(tk.END, f"Request Error: {e}\n")
        except Exception as e:
            txtSpeech.insert(tk.END, f"Error: {e}\n")
        txtSpeech.see(tk.END)  # Scroll to the latest message
        root.update()

def reset_txtSpeech():
    txtSpeech.delete(1.0, tk.END)  # Clear the text area

def exit_system():
    result = messagebox.askquestion("Exit System", "Confirm if you want to exit?")
    if result == 'yes':
        messagebox.showinfo("Goodbye", "Goodbye")  # Display goodbye message
        root.destroy()  # Close the window

def set_language(lang):
    global selected_language
    selected_language = lang
    txtSpeech.insert(tk.END, f"Language set to: {lang}\n")
    txtSpeech.see(tk.END)

# UI setup
root = tk.Tk()
root.title("Speech to Text")

# Main Frame setup
MainFrame = tk.Frame(root, bd=20, width=900, height=600)
MainFrame.pack()

# "Select Language" heading
lblLanguageHeading = tk.Label(MainFrame, font=('arial', 20, 'bold'), text="Select Language")
lblLanguageHeading.pack(anchor='w')

# Language selection buttons frame
langFrame = tk.Frame(MainFrame)
langFrame.pack(anchor='w')

# Language selection buttons
btnEnglish = tk.Button(langFrame, font=('arial', 15, 'bold'), text="English", width=10, height=1, command=lambda: set_language('English'))
btnEnglish.pack(side=tk.LEFT, padx=5)

btnChinese = tk.Button(langFrame, font=('arial', 15, 'bold'), text="Chinese", width=10, height=1, command=lambda: set_language('Chinese'))
btnChinese.pack(side=tk.LEFT, padx=5)

# Title label
lblTitle = tk.Label(MainFrame, font=('arial', 30, 'bold'), text="Speech to Text")
lblTitle.pack()

# Text box for displaying speech-to-text output
txtSpeech = tk.Text(MainFrame, font=('arial', 20), height=10, width=50)
txtSpeech.pack()

# Convert button
btnConvert = tk.Button(MainFrame, font=('arial', 20, 'bold'), text="Convert To Text", width=20, height=2, command=lambda: Speech_to_Text(selected_language))
btnConvert.pack(side=tk.LEFT, padx=5)

# Reset button
btnReset = tk.Button(MainFrame, font=('arial', 20, 'bold'), text="Reset", width=18, height=2, command=reset_txtSpeech)
btnReset.pack(side=tk.LEFT, padx=5)

# Exit button
btnExit = tk.Button(MainFrame, font=('arial', 20, 'bold'), text="Exit", width=18, height=2, command=exit_system)
btnExit.pack(side=tk.LEFT, padx=5)

# Set default language to English
selected_language = 'English'

root.mainloop()



# python3 -m venv myenv

# source myenv/bin/activate

# python /Users/admin/speechtotext.py
