# Badges.py
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import os
import shutil
class BADGE_LIST:
    __base_dir_images = "./Base/"
    DIR_MEMBER = __base_dir_images + "team_member_fira_card.png"
    DIR_MENTOR = __base_dir_images + "team_mentor_fira_card.png"
    DIR_TC = __base_dir_images + "tc_fira_card.png"
    DIR_ORG = __base_dir_images + "org_fira_card.png"
    DIR_VIP = __base_dir_images + "vip_fira_card.png"

class Badges:
    df:pd.DataFrame = None
    baseImage: Image.Image = None
    width, height = -1,-1
    dpi = (300, 300)  # For printing/actual size for image
    font_path = "./Arial Unicode.ttf"
    output_dir = "./Badges"

    def __init__(self, df):
        self.df = df
        self.createOutputDir(self.output_dir)

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
        print("\Badges")
        print(5*"-")
        counter = 1
        for name, league, team, role in zip(self.df["Name"], self.df["League"], self.df["Team Name"], self.df["Member Type"]):
            
            ###########
            # Cleanup
            name = str(name).strip().title()
            league = str(league).strip().title()
            role = str(role).strip().title()
            team = str(team).strip().upper()

            # Type of Badge
            if role == "Member": self.baseImage = Image.open(BADGE_LIST.DIR_MEMBER)
            elif role == "Mentor": self.baseImage = Image.open(BADGE_LIST.DIR_MENTOR)
            elif role == "Org": self.baseImage = Image.open(BADGE_LIST.DIR_ORG)
            elif role == "Tc": self.baseImage = Image.open(BADGE_LIST.DIR_TC)
            elif role == "Vip": self.baseImage = Image.open(BADGE_LIST.DIR_VIP)
            
            self.width, self.height = self.baseImage.width, self.baseImage.height
            self.dpi = self.baseImage.info.get("dpi",(300,300))
            draw = ImageDraw.Draw(self.baseImage)

            left_x = 0.28
            team_font_size = 35 #Since in TVO (TC, VIP, Org) it is the title
            # Text Positions
            if role in ["Tc","Vip","Org"]:
                name_rate_x, name_rate_y = left_x, 0.79
                team_rate_x, team_rate_y = left_x, 0.86
                team_font_size = 40
            else:
                name_rate_x, name_rate_y = left_x, 0.77
                league_rate_x, league_rate_y = left_x, 0.88
                team_rate_x, team_rate_y = left_x, 0.85

                league_x, league_y = int(league_rate_x * self.width), int(league_rate_y * self.height)
                league_font, league_width, league_height = self.boxGen(draw, league, 45)
                draw.text((league_x, league_y), league, stroke_width=1, font=league_font, fill="black")

            
            # Rates based on width
            name_x, name_y = int(name_rate_x * self.width), int(name_rate_y * self.height)
            team_x, team_y = int(team_rate_x * self.width), int(team_rate_y * self.height)
            
            
            # Sizes Boxes
            name_font, name_width, name_height = self.boxGen(draw, name, 65)
            team_font, team_width, team_height = self.boxGen(draw, team, team_font_size)

            
            draw.text((name_x, name_y), name, stroke_width=2, font=name_font, fill="black")
            draw.text((team_x, team_y), team, stroke_width= 0, font=team_font, fill="black")
            
            print(f"{counter}-{name}-{league}")
            self.baseImage.save(f"{self.output_dir}/badge_{counter}.webp", dpi=self.dpi, format="webp")
            counter += 1
        
        print(f"===== Total No. of {counter}(s) badges generated =====\n")
