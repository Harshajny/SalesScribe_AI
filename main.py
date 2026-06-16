import os
import pandas as pd
EXCEL_FILE="sales_pipeline.xlsx"
def append_to_excel(extracted_data:dict):
    new_row=pd.DataFrame([extracted_data])
    if os.path.exists(EXCEL_FILE):
        print(f"->Found existing spreadsheet'{EXCEL_FILE}'. Reading history ...")
        existing_df=pd.read_excel(EXCEL_FILE)
        updated_df=pd.concat([existing_df,new_row],ignore_index=True)
    else:
         print(f"->No spreadsheet found.Creating a brand new file:'{EXCEL_FILE}'")
         updated_df=new_row
    updated_df.to_excel(EXCEL_FILE,index=False)
    print(f"Successfully logged data for:{extracted_data.get('client_name','Unknonw')}\n")
if __name__=="__main__":
    print("Initializing SalesScribe AI Storage Engine.../n")
    simulated_batch_results=[
    {"client_name":"Harsha Johny", "budget":"₹1200","next_steps":"Send contract on friday"},        
    {"client_name":"Samantha Lee", "budget":"₹5000","next_steps":"Schedule demo for next week"},
    {"client_name":"Rajesh Kumar", "budget":"₹3000","next_steps":"Follow up in 3 days"}
    ]
    print(f"Found{len(simulated_batch_results)}entries in queue. Starting batch Excel append.")
    print("-"*50)
    for call_data in simulated_batch_results:
        append_to_excel(call_data)
    print("Batch test complete! Look inside you project folder for 'sales_pipeline.xlsx' to see the results.")