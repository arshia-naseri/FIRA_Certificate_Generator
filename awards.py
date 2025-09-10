# awards.py
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import os
import shutil

class Awards:
    df:pd.DataFrame = None
    baseImage: Image.Image = None
    width, height = -1,-1
    dpi = (300, 300)  # For printing/actual size for image
    font_path = "./Arial Unicode.ttf"
    output_dir = "./Awards"

    def __init__(self, df, baseImagePath = "./Base/award_base.png"):
        self.df = df
        self.createOutputDir(self.output_dir)
        # Image
        self.baseImage = Image.open(baseImagePath)
        self.width, self.height = self.baseImage.width, self.baseImage.height
        self.dpi = self.baseImage.info.get("dpi",(300,300))

    # Create Award Directory
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

    def generate(self):
        print("\nAward Certification")
        print(5*"-")
        counter = 1
        for name, league, team, role, place in zip(self.df["Name"], self.df["League"], self.df["Team Name"], self.df["Member Type"], self.df["Place"]):
            # Text Positions
            centre_x = 0.4
            name_rate_x, name_rate_y = centre_x, 0.39
            team_rate_x, team_rate_y = centre_x, 0.50
            title_rate_x, title_rate_y = centre_x, 0.54
            ###########

            name = str(name).strip().title()
            league = str(league).strip().title()
            role = str(role).strip().title()
            team = str(team).strip().upper()
            place = str(place).strip().title()

            img = self.baseImage.copy()
            draw = ImageDraw.Draw(img)

            team = f"{role} of {team}"

            # If the placement was numerical
            if place == "1": place = f"{place}st Award"
            elif place == "2": place = f"{place}nd Award"
            elif place == "3": place = f"{place}rd Award"

            title = f"{place} in {league}"

            # Rates based on width
            name_x, name_y = int(name_rate_x * self.width), int(name_rate_y * self.height)
            team_x, team_y = int(team_rate_x * self.width), int(team_rate_y * self.height)
            title_x, title_y = int(title_rate_x * self.width), int(title_rate_y * self.height)

            # Sizes Boxes
            name_font, name_width, name_height = self.boxGen(draw, name, 65)
            name_box_x = name_x - name_width // 2

            team_font, team_width, team_height = self.boxGen(draw, team, 40)
            team_box_x = team_x - team_width // 2

            title_font, title_width, title_height = self.boxGen(draw, title, 50)
            title_box_x = title_x - title_width // 2
            
            draw.text((name_box_x, name_y), name, stroke_width=2, font=name_font, fill="black")
            draw.text((team_box_x, team_y), team, stroke_width= 0, font=team_font, fill="black")
            draw.text((title_box_x, title_y), title, stroke_width=0.5, font=title_font, fill="black")
            
            print(f"{counter}-{name}-{title}")
            img.save(f"{self.output_dir}/awards_certification_{counter}.webp", dpi=self.dpi, format="webp")
            counter += 1
        
        print(f"===== Total No. of {counter}(s) Awards generated =====\n")
