# Participants.py
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import os
import shutil

class Participants:
    df:pd.DataFrame = None
    baseImage: Image.Image = None
    width, height = -1,-1
    dpi = (300, 300)  # For printing/actual size for image
    font_path = "./Arial Unicode.ttf"
    output_dir = "./Participants"

    def __init__(self, df, baseImagePath = "./Base/participant_base.png"):
        self.df = df
        self.createOutputDir(self.output_dir)
        # Image
        self.baseImage = Image.open(baseImagePath)
        self.width, self.height = self.baseImage.width, self.baseImage.height
        self.dpi = self.baseImage.info.get("dpi",(300,300))

    # Create Participant Directory
    def createOutputDir(self,dir_path):
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path)

    def boxGen(self, draw, text, font_size, threshold = 0.7):
        text_font = ImageFont.truetype(self.font_path, font_size)
        text_bbox = draw.textbbox((0, 0), text, font=text_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        while text_width > self.width * threshold:
            text_font = ImageFont.truetype(self.font_path, font_size)
            text_bbox = draw.textbbox((0, 0), text, font=text_font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            font_size -= 1

        return text_font, text_width, text_height

    def show_preview(self,img):
        plt.figure(figsize=(img.width / 200, img.height / 200))
        plt.imshow(img)
        plt.axis('off') 
        plt.show()

    def generateCertificates(self):
        print("\nParticipant Certification")
        print(5*"-")
        counter = 1
        for name, league, team, role in zip(self.df["Name"], self.df["League"], self.df["Team Name"], self.df["Member Type"]):
            # Text Positions
            centre_x = 0.39
            role_rate_x, role_rate_y = centre_x, 0.35
            name_rate_x, name_rate_y = centre_x, 0.39
            team_rate_x, team_rate_y = centre_x, 0.51
            league_rate_x, league_rate_y = centre_x, 0.56
            ###########

            name = str(name).strip().title()
            league = str(league).strip().title()
            role = str(role).strip().title()
            team = str(team).strip().upper()

            img = self.baseImage.copy()
            draw = ImageDraw.Draw(img)

            # Rates based on width
            role_x, role_y = int(role_rate_x * self.width), int(role_rate_y * self.height)
            name_x, name_y = int(name_rate_x * self.width), int(name_rate_y * self.height)
            team_x, team_y = int(team_rate_x * self.width), int(team_rate_y * self.height)
            league_x, league_y = int(league_rate_x * self.width), int(league_rate_y * self.height)

            # Sizes Boxes
            role_font, role_width, role_height = self.boxGen(draw, role, 30)
            role_box_x = role_x - role_width // 2

            name_font, name_width, name_height = self.boxGen(draw, name, 65)
            name_box_x = name_x - name_width // 2

            team_font, team_width, team_height = self.boxGen(draw, team, 50)
            team_box_x = team_x - team_width // 2

            league_font, league_width, league_height = self.boxGen(draw, league, 65)
            league_box_x = league_x - league_width // 2
            
            draw.text((role_box_x, role_y), role, stroke_width=0.5, font=role_font, fill="black")
            draw.text((name_box_x, name_y), name, stroke_width=2, font=name_font, fill="black")
            draw.text((team_box_x, team_y), team, stroke_width= 0, font=team_font, fill="black")
            draw.text((league_box_x, league_y), league, stroke_width= 1, font=league_font, fill="black")

            print(f"{counter}-{name}-{league}")
            # self.show_preview(img)
            img.save(f"{self.output_dir}/certificate_participant_{counter}.png", dpi=self.dpi)
            counter += 1
        
        print(f"===== Total No. of {counter}(s) certificate of participation generated =====\n")