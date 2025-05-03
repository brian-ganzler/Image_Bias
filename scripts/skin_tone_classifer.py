import stone
import os
import pandas as pd

def main():
    skin_tone_dalle(r'C:\Users\brian\OneDrive\Python Projects\Generative AI Image Bias\Images\DALL-E')

def skin_tone_dalle(root_directory):
    total = 0  # Total images processed for personal reference
    data = []  # Storing image data

    for theme in os.listdir(root_directory):  # Loop through all themes in the directory
        for prompt in os.listdir(os.path.join(root_directory, theme)):  # Loop all prompts in the theme directory
            for image in os.listdir(os.path.join(root_directory, theme, prompt)):  # Loop all images in the prompt directory
                image_directory = os.path.join(root_directory, theme, prompt, image)  # Directory of image to process
                try:  # Encapsulated in try block to prevent the program from crashing
                    # print(f"Processing {theme}-{prompt}-{image}")
                    result = stone.process(image_directory, image_type="color", tone_palette="yadon-ostfeld", return_report_image=True)  # Process data from the image
                    # report_images = result.pop("report_images")  # Display image analysis
                    temp_data = [{  # Extracting specific data from the result to a temporary variable holder
                        "Directory": image_directory,
                        "Theme": theme,
                        "Prompt": prompt,
                        "File Name": image,
                        "Face ID": result["faces"][0]["face_id"],
                        "Predicted Dominant Tone Percent": result["faces"][0]["dominant_colors"][0]["percent"],
                        "Predicted Dominant Tone Color": result["faces"][0]["dominant_colors"][0]['color'],
                        "Predicted Average Accuracy": result["faces"][0]['accuracy'],
                        "Predicted Average Tone Color": result["faces"][0]['skin_tone']
                    }]
                    total += 1
                    data.append(temp_data)  # Add temp_data to a data list
                except FileNotFoundError:
                    print("Unable to find: " + image_directory)
    output = []
    for _ in data:  # Loop through data and to remove redundant list encapsulation for each image data
        for image in _:
            output.append(image)
    df = pd.DataFrame(output)  # Convert data into dataframe for excel export
    df.to_excel("test.xlsx", index=False)
    print("Total Images: ", total)

if __name__ == '__main__':
    main()
