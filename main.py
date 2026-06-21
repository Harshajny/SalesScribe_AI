import os #lets the script to talk to the computer file system
import pandas as pd #pandas is a data manipulation library
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field
load_dotenv()

class SalesCallData(BaseModel):
    client_name:str=Field(description="The extracted name of the client or prospect")
    budget:str=Field(description="The financial budget figures or ranges dicussed, formatted nicely into standard currency (e.g., ₹X,XX,XXX).")
    next_steps: str=Field(description="A concise action-item summary of the follow-up next steps in professional business English ")
EXCEL_FILE="sales_pipeline.xlsx"
RECORDINGS_DIR="raw_recordings"

def scan_for_recordings():
    print(f"inspecting ")
    if not os.path.exists(RECORDINGS_DIR): #checks if the folder exists
        print(f"Directory '{RECORDINGS_DIR}' does not exist. Creating it now...")
        os.makedirs(RECORDINGS_DIR) #if there is no such folder it makes one
        return[]
    all_files=os.listdir(RECORDINGS_DIR) #provides a list of strings representing everything inside the folder( the folder names in string format and such)
    valid_extensions=('.mp3','.wav','.flac','.m4a')
    recording_files=[f for f in all_files if f.lower().endswith(valid_extensions)] #list comprehension: a single loop to filter out according to extensions
    return recording_files
def analyze_audio_with_ai(audio_file_name: str)-> dict:
        full_path=os.path.join(RECORDINGS_DIR,audio_file_name)
        print(f"/n Uploading {audio_file_name} to Gemini Cloud Space...")
        client=genai.Client()
        audio_asset=client.files.upload(file=full_path)
        print(f"Audio file uploaded. Processing audio frequencies & transalation rules...")
        system_prompt=(
           "You are an elite, expert sales operations analyst. Listen closely to the provided call recording.\n\n"
        "CRITICAL RULES:\n"
        "1. Multilingual Handling: The speakers might code-switch, use broken English, or jump into their native languages mid-sentence. "
        "Completely understand the core semantic intent across all languages spoken.\n"
        "2. Translation & Cleanup: Automatically translate all non-English talk sections into clean, professional business English. "
        "Fix fragmented grammar, remove stutters, and omit filler words.\n"
        "3. Extraction: Extract the prospect's name, the target budget numbers, and the precise future follow-up action items."
        )
        response=client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[audio_asset,system_prompt],
            config={
                'response_mime_type':'application/json',
                'response_schema':SalesCallData
            
            }
        )
        client.files.delete(name=audio_asset.name)
        print("Temporary cloud file asset wiped clean.")
        return response.parsed.model_dump()
def append_to_excel(extracted_data:dict): # function expecting to receive a python dictionary
    new_row=pd.DataFrame([extracted_data]) #DataFrame converts dict keys to column headers and dict values to rows of data
    if os.path.exists(EXCEL_FILE): #os module to check where that file exists in this folder
        print(f"->Found existing spreadsheet'{EXCEL_FILE}'. Reading history ...")
        existing_df=pd.read_excel(EXCEL_FILE) #if it exists it is opened using pd.read_excel()
        updated_df=pd.concat([existing_df,new_row],ignore_index=True) #stacjs data frames on top of each other and resets the index(ignore_index=True, so rows are 0,1,2,3 instead of 0,1,2,0,1,2)
    else:
         print(f"->No spreadsheet found.Creating a brand new file:'{EXCEL_FILE}'")
         updated_df=new_row
    updated_df.to_excel(EXCEL_FILE,index=False) #to_excel command acts as a translator. It takes that live grid layout from RAM, translates it back into a binary stream structured as an Excel spreadsheet file, and drops it onto your hard drive.
    print(f"Successfully logged data for:{extracted_data.get('client_name','Unknonw')}\n")
if __name__=="__main__":
    print("Initializing SalesScribe AI Storage Engine.../n")
    found_recordings=scan_for_recordings()
    print('-'*50)
    if not found_recordings:
            print("No recordings found in the 'raw_recordings' folder")
    else:
        for audio_file in found_recordings:
            print(f"---Processing File: {audio_file}---")
            try:
                ai_payload=analyze_audio_with_ai(audio_file)
                append_to_excel(ai_payload)
                print(f"Successfully processed and logged data for: {ai_payload.get('client_name','Unknown')}\n")
            except Exception as e:
                print(f"Error processing {audio_file}: {str(e)}\n")
    print("\n Scanner processing iteration complete")
     
    