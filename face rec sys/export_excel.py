import pandas as pd
import os

for file in os.listdir():
    if file.startswith("attendance_") and file.endswith(".csv"):
        df = pd.read_csv(file)
        excel_name = file.replace(".csv", ".xlsx")
        df.to_excel(excel_name, index=False)
        print(f"Exported {excel_name}")
