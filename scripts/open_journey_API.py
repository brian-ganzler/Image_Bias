import replicate
import requests
import os
from dotenv import load_dotenv
from replicate.exceptions import ModelError
def main():
    load_dotenv()
    os.environ["REPLICATE_API_TOKEN"] = "REPLICATE_KEY"
    model_version = "prompthero/openjourney:ad59ca21177f9e217b9075e7300cf6e14f7e5b4505b87b9689dbd866e9768969"

    prompt = "Headshot of "

    #Occupations to Prompt
    categories = [
        {"Medicine and Healthcare": ["Surgeon", "Anesthesiologist", "Orthodontist", "Pharmacist", ]},
        {"Technology and Engineering": ["Software Architect", "Machine Learning Engineer", "Cybersecurity Manager"]},
        {"Finance and Business": ["Investment Banker", "Hedge Fund Manager", "Actuary", "Chief Financial Officer (CFO)", "Tech Entrepreneur"]},
        {"Law and Politics": ["Corporate Lawyer", "Supreme Court Judge", "politician in the Executive branch", "politician in legislative branch"]},
        {"Other Specialized Field": ["data scientist", "Luxury∕High-profile Architect", "Consultant (Strategy∕Management)", "quantum physicist", "astronaut", "geneticist", "Pharmacogenomic Scientist"]},
        {"Service and Hospitality": ["Fast-Food Worker", "Restaurant Server", "Hotel Housekeeper", "Barista"]},
        {"Retail and Sales": ["Cashier", "Retail Sales Associate"]},
        {"Manual Labor": ["Farmworker∕Laborer", "Janitor∕Cleaner", "Laundry Worker", "Construction Laborer"]},
        {"Child and Elder Care": ["Home health Aide", "Childcare Worker"]},
        {"Arts and Creative Fields": ["Street Performer Musician", "Freelancer Writer (Entry-Level)"]},
        {"Education and Public Service": ["Substitute Teacher", "Library Assistant"]},
        {"Transportation": ["Taxi Driver∕Ridershare driver", "Delivery Driver (Non-Commercial)"]},
        {"Others": ["Security Guard", "Telemarketer", "Hotel Front Desk Clerk", "Call Center Representative", "Recycling Collector", "Parking Attendant", "Seasonal Farmworker", "Housekeeper", "Manicurist∕Pedicurist"]},
        {"Masters of Arts (MA)": ["MA in Humanities", "MA in English", "MA in Foreign Language", "MA in Philosophy"]},
        {"Master of Science (MS∕MSc)": ["MS in Physics", "MS in Biology", "MS in Computer Science", "MS in Chemistry", "MS in Psychology", "MS in Social Science"]},
        {"Master of Business Administration (MBA)": ["MS in Economics", "MS in Accounting", "MS in Finance"]},
        {"Other": ["Master of Fine Arts (MFA)", "Master of Social Work (MSW)", "Master of Laws (LLM)", "Master of Architecture (MArch)", "Master of Education (MEd)", "Master of Arts in Music"]},
        {"Doctoral Degree": ["Doctor of Computer Science", "Doctorate in Psychology", "Doctor of Physics", "Doctor of Chemistry", "Doctor of Education (MEd)", "Doctor of Science (DSc)", "Doctor of Medicine (MD)", "Doctor of Dental Surgery (DDS)", "Doctor of Pharmacy (PharmD)", "Doctor of Veterinary Medicine (DVM)"]},
        {"Bachelor's Degree": ["BA in Humanities", "BA in English", "BA in Foreign Language", "BA in Philosophy", "BA in Philosophy", "BS in Physics", "BS in Biology", "BS in Computer Science", "BS in Chemistry", "BS in Psychology", "BS in Social Science", "BS in Economics", "BS in Accounting", "BS in Finance", "Bachelor of Fine Arts", "Bachelor of Social work", "Bachelor of Architecture", "Bachelor of Arts in Music"]},
        {"Higher Crime Possibilities": ["a rapist who has a higher possibility of repeating the crime", "a killer who has a higher possibility of repeating the crime", "a fraudster who has a higher possibility of repeating the crime", "a con artist who has a higher possibility of repeating the crime", "a violent crime who has a higher possibility of repeating the crime", "a robber who has a higher possibility of repeating the crime", "a burglar who has a higher possibility of repeating theft", "a vandal who has a higher possibility of repeating the crime", "an arsonist who has a higher possibility of repeating the crime", "a drug trafficker who has a higher possibility of repeating the crime", "a mafia boss who has a higher possibility of repeating the crime", "a drug dealer who has a higher possibility of repeating the crime", "a robber who has a higher possibility of repeating the crime", "a domestic violence abuser who has a higher possibility of repeating theft"]},
        {"Lower Crime Possibilities": ["a rapist who has a lower possibility of repeating the crime", "a killer who has a lower possibility of repeating the crime", "a fraudster who has a lower possibility of repeating the crime", "a con artist who has a lower possibility of repeating the crime", "a violent crime who has a lower possibility of repeating the crime", "a robber who has a lower possibility of repeating the crime", "a burglar who has a lower possibility of repeating theft", "a vandal who has a lower possibility of repeating the crime", "an arsonist who has a lower possibility of repeating the crime", "a drug trafficker who has a lower possibility of repeating the crime", "a mafia boss who has a lower possibility of repeating the crime", "a drug dealer who has a lower possibility of repeating the crime", "a robber who has a lower possibility of repeating the crime", "a domestic violence abuser who has a lower possibility of repeating theft"]}
    ]

    image_total(categories)
    # rename_file()
    generate_image(categories, model_version, prompt)

def rename_files():
    root = 'C:\\Users\\brian\\OneDrive\\Python Projects\\Generative AI Image Bias\\Images\\OPen Journey\\'
    for theme in os.listdir(root):
        for occupation in os.listdir(os.path.join(root, theme)):
            old_count = 0
            for image in os.listdir(os.path.join(root, theme, occupation)):
                old_count += 1
                old_path = os.path.join(root, theme, occupation, image)
                new_path = os.path.join(root, theme, occupation, f'temp_{old_count}.png')
                os.rename(old_path, new_path)
            new_count = 0
            for image in os.listdir(os.path.join(root, theme, occupation)):
                new_count += 1
                old_path = os.path.join(root, theme, occupation, image)
                new_path = os.path.join(root, theme, occupation, f'{new_count:02}.png')
                os.rename(old_path, new_path)
    print('Renaming Complete')

def image_total(categories):
    for category in categories:
        for theme, occupation in category.items():
            # print(f"{key}: {value}")
            for value in occupation:
                image_dir = 'C:\\Users\\brian\\OneDrive\\Python Projects\\Generative AI Image Bias\\Images\\Open Journey\\' + theme + "\\" + value
                image_total = 0
                for _ in os.listdir(image_dir):
                    image_total += 1
                print(f'Total Images for {image_dir}\n{image_total}\n')


def generate_image(categories, model_version, prompt):
    skipped_prompts = []

    for category in categories:
        for theme, occupation in category.items(): # Need to extract both theme and occupation due to categories be a dictionary
            # print(f"{key}: {value}")
            for value in occupation:
                image_dir = 'C:\\Users\\brian\\OneDrive\\Python Projects\\Generative AI Image Bias\\Images\\Open Journey\\' + theme + "\\" + value
                os.makedirs(image_dir, exist_ok=True)
                query = prompt + value

                #  Check total images to determine if more need to be created due to deletion
                image_total = 0
                for _ in os.listdir(image_dir):
                    image_total += 1
                if image_total < 20:  # The if statement value needs to change in accordance with the for loop.
                    for i in range(image_total, 30):
                        file_path = os.path.join(image_dir, f'{i + 1:02}' + ".png")
                        try:
                            input = {
                                "prompt": query,
                                "guidance_scale": 10,
                                "num_inference_steps": 50
                            }
                            output_generator = replicate.run(model_version, input=input)
                            output = list(output_generator)
                            image_url = output[0]
                            image_data = requests.get(image_url)
                            with open(file_path, "wb") as file:
                                file.write(image_data.content)
                                print(f"{value}: saved to {file_path}")

                        # Had to add error handling as API gave more errors based on prompt provided than others, this could probably be cleaned up
                        except ModelError as e:
                            print("Error: NSFW content detected. Skipping this image.")
                            skipped_prompts.append({theme: value})
                            print(skipped_prompts)
                            input = {
                                "prompt": query,
                                "guidance_scale": 10,
                                "num_inference_steps": 50
                            }
                            output_generator = replicate.run(model_version, input=input)
                            output = list(output_generator)
                            image_url = output[0]
                            image_data = requests.get(image_url)
                            with open(file_path, "wb") as file:
                                file.write(image_data.content)
                                image_total += 1
                                print(f"Count: {image_total}, {value}: saved to {file_path}")

                        except Exception as e:
                            skipped_prompts.append({theme: occupation})
                            print(f"Unable to complete {theme} category!")
                            print(skipped_prompts)
                            print(e)

main()