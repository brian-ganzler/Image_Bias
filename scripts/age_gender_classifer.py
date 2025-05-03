import os
import pandas as pd
from deepface import DeepFace

def main():
    gender_dalle("C:\\Users\\brian\\OneDrive\\Python Projects\\AI Image Skin Tone\\Images\\DALL-E\\")

def gender_dalle(root_directory):
    excel_directory = "skin_tone_data.xlsx"
    df = pd.read_excel(excel_directory, sheet_name="Sheet1")

    if "Gender" not in df.columns:  # Add Gender column to dataframe to append data
        df["Gender"] = "N/A"

    for theme in os.listdir(root_directory):
        for prompt in os.listdir(os.path.join(root_directory, theme)):
            for image in os.listdir(os.path.join(root_directory, theme, prompt)):
                image_directory = os.path.join(root_directory, theme, prompt, image)
                try:
                    result = DeepFace.analyze(image_directory, actions=['gender'], detector_backend='mtcnn')
                    # print(f'\n{result}')
                    gender = result[0]['dominant_gender']  # Index to extract gender
                    df.loc[df["Directory"] == image_directory, "Gender"] = gender
                except Exception as e:
                    print(f'\nNo Face Detected at: \n{image_directory}\n{e}')

    df.to_excel("gender_data.xlsx", index=False)







