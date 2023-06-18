import asyncio

import edge_tts
import pandas as pd
import re




class Text2s: 
    async def Text2Speech(self,text,voice):
        communicate = edge_tts.Communicate(text,voice)
        audio_data = b''
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data+=chunk['data']
        return audio_data  

    def GetVoice(self,text,voice): 
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            self.audio_data = loop.run_until_complete(self.Text2Speech(text,voice))
            # self.save_audio_file("tmp")
        finally:
            loop.close()  
            # self.save_audio_file("tmp")

    def GetVoiceType(self,file_name):
        # Load the Excel file
        df = pd.read_excel(file_name)
    
        column_names = df.columns.tolist()
        extracted_info = []
        pattern = r'\((.*?)\)'  
        for string in df['Name'].tolist():
            match = re.search(pattern, string)
            if match:
                extracted_info.append(match.group(1))
        return extracted_info
            
    def save_audio_file(self):
        if self.audio_data:
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as file:
                file.write(self.audio_data)
                tmp_file_path = file.name
            messagebox.showinfo("Save As", "File saved successfully.")
            self.play_audio(tmp_file_path)
        else:
            messagebox.showerror("Save As", "No audio data available.")

