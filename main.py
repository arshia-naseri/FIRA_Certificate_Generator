# main.py
from participants import Participants
from awards import Awards
import pandas as pd

excel_file_name = "dummy_list.xlsx"

if __name__ == "__main__":
    
    while True:
        print(">> Please Select an Item:")
        print("1- Generate Participant")
        print("2- Generate Awards")
        print("3- Generate Badges")
        print("4- Exit Program")
        inp = input(">> ").strip()
        

        if inp == "1":     # participants
            cert = Participants(pd.read_excel(excel_file_name, sheet_name="participants"))
            cert.generateCertificates()
        elif inp == "2":   # Awards
            cert = Awards(pd.read_excel(excel_file_name, sheet_name="awards"))
            cert.generateCertificates()
        elif inp == "3":   # Badges
            print("Badges")
        elif inp == "4":
            break
        else:
            print(">> ERROR: Wrong Input. Try Again")
        
        break
        print(5*"-")