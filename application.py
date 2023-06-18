import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk
from Text2speech import Text2s
import tkinter.messagebox as messagebox
from tkinter import filedialog
import tempfile
import os
import pygame
import shutil


class MyApplication(tk.Tk,Text2s):
    def __init__(self, h, w, title) -> None:
        super().__init__()
        self.title(title)
        self.geometry(f"{h}x{w}")
        self.resizable(True, True)
        self.HeadlineFrame = tk.Frame(self, bg="white",background="black")
        self.HeadlineFrame.pack(side=tk.TOP, fill=tk.X)
        
        self.TextFrame = tk.Frame(self, borderwidth=2, relief="solid")
        self.AudioFrame = tk.Frame(self, borderwidth=2, relief="solid")
        
        self.TextFrame.pack(side=tk.LEFT, expand=True, fill="both")
        self.AudioFrame.pack(side=tk.RIGHT, expand=True, fill="both")
        
    def getWindowSize(self):
        self.update()
        return self.winfo_width(), self.winfo_height()
    
    def Convert_button(self):
        # text = str(self.Main_textarea.get("1.0", "end-1c"))
        # print(text)
        # voice = self.GetVoiceType
        self.submit_button = tk.Button(self.AudioFrame,
                                       text="Convert",
                                       command=self.Convert_toSpeech, 
                                       fg="black", bg="white", 
                                       relief="raised", font=("Arial", 12, "bold"))
        self.submit_button.pack(pady=10)
        
    
    
    def Textarea(self):
        self.Main_textarea = tk.Text(self.TextFrame, 
                                     height=10, width=40,
                                     bd=2, relief='solid',
                                     highlightthickness=2,
                                     exportselection = True,
                                     font=("Arial", 12))
        self.Main_textarea.pack(side=tk.TOP, pady=5,padx = 5, expand=True, fill="both")
        scrollbar = tk.Scrollbar(self.TextFrame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.Main_textarea.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.Main_textarea.yview)
        
        


        
    def Copy_button(self):
        self.copy_button = tk.Button(self.TextFrame,command=self.copy_text, 
                                       text="Copy", 
                                       fg="black", bg="white", 
                                       relief="raised", font=("Arial", 12, "bold"))
        self.update()
        
        self.copy_button.pack(side=tk.LEFT, pady=10, padx=self.winfo_width()//4)
        
    def Paste_button(self):
        self.paste_button = tk.Button(self.TextFrame,command=self.paste_text,
                                       text="Past", 
                                       fg="black", bg="white", 
                                       relief="raised", font=("Arial", 12, "bold"))
        self.paste_button.pack(side=tk.LEFT, pady=10, padx=5)
        
    def Clear_button(self):
        self.clear_button = tk.Button(self.TextFrame,command=self.clear_text,
                                       text="Clear", 
                                       fg="black", bg="white", 
                                       relief="raised", font=("Arial", 12, "bold"))
        self.clear_button.pack(side=tk.LEFT, pady=10, padx=5)
            
    def copy_text(self):
        text = self.Main_textarea.get("1.0", "end-1c")  # Get the text content of the textarea
        self.clipboard_clear()  # Clear the clipboard
        self.clipboard_append(text)  # Append the text to the clipboard

    def paste_text(self):
        text = self.clipboard_get()  # Get the content from the clipboard
        self.Main_textarea.insert(tk.END, text)  # Insert the text into the textarea
    
    def clear_text(self):
        self.Main_textarea.delete("1.0", tk.END)
        
    def add_headline(self):
        image_path = "Data/title.PNG"
        image = Image.open(image_path)
        self.update()
        w,h = self.winfo_width(),self.winfo_height()
        resized_image = image.resize((w, int(0.2*h)+1))
        photo = ImageTk.PhotoImage(resized_image)
        
        headline_label = tk.Label(self.HeadlineFrame, image=photo)
        headline_label.image = photo  # Store a reference to avoid garbage collection
        headline_label.pack()
    
    
    def create_voice_type_label(self,text_string):
        voice_type_label = tk.Label(
            self.AudioFrame,
            text=text_string,
            font=("Arial", 12, "bold")
        )
        voice_type_label.pack(pady=10)

    def create_item_selection(self,items):
        self.item_selection = ttk.Combobox(
            self.AudioFrame,
            values=items,
            state="readonly",
            font=("Arial", 12),
            width=20
        )
        self.item_selection.set(items[57])  # Set the default selected item
        self.item_selection.pack()
    
    
    def Convert_toSpeech(self):
        text = str(self.Main_textarea.get("1.0", "end-1c"))
        voicetype = "Microsoft Server Speech Text to Speech Voice ("+self.item_selection.get() + ")" 
        
        self.GetVoice(text,voicetype)
        self.save_audio_file()
        self.update_file_info()
    
    def save_audio_file(self):
        if self.audio_data:
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as file:
                file.write(self.audio_data)
                self.tmp_file_path = file.name
            messagebox.showinfo("Save As", "File saved successfully.")
            self.play_audio()
        else:
            messagebox.showerror("Save As", "No audio data available.")

    
    
    
    def play_button(self):
        
        self.submit_button = tk.Button(self.AudioFrame,
                                       text="Play",
                                       command=self.play_audio, 
                                       fg="black", bg="white", 
                                       relief="raised", font=("Arial", 12, "bold"))
        self.submit_button.pack(pady=10)
        
    
    
    def play_audio(self):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(self.tmp_file_path)
            pygame.mixer.music.play()
        except pygame.error:
            messagebox.showerror("Audio File Not found", "Convert before Play \n Audio file not found: tmp.mp3")
    
    def SaveAs_button(self):
        self.saveas_button = tk.Button(self.AudioFrame, command=self.save_as_file,
                                    text="Save As",
                                    fg="black", bg="white",
                                    relief="raised", font=("Arial", 12, "bold"))
        self.saveas_button.pack(pady=10)

    def save_as_file(self):
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".mp3",
                                                   filetypes=[("MP3 Files", "*.mp3"), ("All Files", "*.*")])
        if file_path:
            try:
                shutil.copyfile(self.tmp_file_path, file_path)
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save the file: {str(e)}")

    
    def file_info(self):
        self.file_info_label = tk.Label(self.AudioFrame, text="Temporary File Path:\n No File Found \nLast Modified:\n 0000-00-00 00:00:00" ,font=("Arial", 12))
        self.file_info_label.pack(pady=10)
    
        
    
    
    def update_file_info(self):
        if os.path.exists(self.tmp_file_path):
            modified_date = os.path.getmtime(self.tmp_file_path)
            formatted_date = self.format_date(modified_date)
            self.file_info_label.config(text=f"Temporary File Path:\n {self.tmp_file_path} \nLast Modified:\n {formatted_date}")
        else:
            self.file_info_label.config(text="File not found")
    
    @staticmethod
    def format_date(timestamp):
        import datetime
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
    
    
    # load text section 
    def Textsection(self):
        self.Textarea()
        self.Copy_button()
        self.Paste_button()
        self.Clear_button()
        
        
        
        
    # load audio section 
    def AudioSection(self):
        self.Convert_button()
        self.SaveAs_button()
        self.create_voice_type_label("voice type")
        self.create_item_selection(self.GetVoiceType("Data/voices.xlsx"))
        self.play_button()
        self.file_info()
        
        
if __name__ == "__main__":
    app = MyApplication(800, 600, "Text2speech")
    app.add_headline()
    app.AudioSection()
    app.Textsection()
    app.mainloop()


