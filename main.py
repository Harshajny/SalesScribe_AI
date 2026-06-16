import os #lets the script to talk to the computer file system
import pandas as pd #pandas is a data manipulation library
EXCEL_FILE="sales_pipeline.xlsx"
RECORDINGS_DIR="raw_recordings"
def scan_for_recordings():
    print(f"inspecting ")
    if not os.path.exists(RECORDINGS_DIR):
        print(f"Directory '{RECORDINGS_DIR}' does not exist. Creating it now...")
        os.makedirs(RECORDINGS_DIR)
        return[]
    all_files=os.listdir(RECORDINGS_DIR)
    valid_extensions=('.mp3','.wav','.flac','.m4a')
    recording_files=[f for f in all_files if f.lower().endswith(valid_extensions)]
    return recording_files

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
        print("No recordings found in the 'raw_recordings' folder. Please add some audio files and rerun the script.")
    else:
        for audio_file in found_recordings:
            print(f"Processing file:{audio_file}")
            mock_payload= {
                "client_name": f"Client ({audio_file})",
                "budget": "Pending Ai extraction",
                "next_steps": "Pending Ai extraction"
            }
            append_to_excel(mock_payload)
    print("\n Scanner processing iteration complete")
    simulated_batch_results=[
    {"client_name":"Harsha Johny", "budget":"₹1200","next_steps":"Send contract on friday"},        
    {"client_name":"Samantha Lee", "budget":"₹5000","next_steps":"Schedule demo for next week"},
    {"client_name":"Rajesh Kumar", "budget":"₹3000","next_steps":"Follow up in 3 days"}
    ]
    print(f"Found{len(simulated_batch_results)}entries in queue. Starting batch Excel append.")
    print("-"*50)
    for call_data in simulated_batch_results:
        append_to_excel(call_data) #sends each of it to the append_to_excel function to be processed and stored in the Excel file
    print("Batch test complete! Look inside you project folder for 'sales_pipeline.xlsx' to see the results.")