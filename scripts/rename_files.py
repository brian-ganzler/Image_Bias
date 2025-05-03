import os

def main():
    Open_Journey()
    print("Open Journey Renamed.")
    Dalle()
    print("DALL-E Renamed.")
    Stable_Diffusion()
    print("Stable Diffusion Renamed.")

def Open_Journey():
    root = 'C:\\Users\\brian\\OneDrive\\Python Projects\\Generative AI Image Bias\\Images\\Open Journey\\'
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

def Dalle():
    root = 'C:\\Users\\brian\\OneDrive\\Python Projects\\Generative AI Image Bias\\Images\\DALL-E\\'
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

def Stable_Diffusion():
    root = 'C:\\Users\\brian\\OneDrive\\Python Projects\\Generative AI Image Bias\\Images\\Stable Diffusion\\'
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

if __name__ == '__main__':
    main()
