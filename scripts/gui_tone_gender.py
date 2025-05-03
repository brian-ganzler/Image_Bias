from tkinter import *
from PIL import Image, ImageTk

class SkinToneGenderApp:
    def __init__(self, root):
        # Root setup
        self.root = root
        self.width, self.height = 800, 600
        self.root.title("Skin Tone and Gender Analysis")
        self.root.geometry(f"{self.width+200}x{self.height}")

        self.image_directory = "C:\\Users\\brian\\OneDrive\\Python Projects\\Generative AI Image Bias\\Images\\DALL-E\\Arts and Creative Fields\\Freelancer Writer (Entry-Level)\\01.png"
        self.coordinates_one = StringVar()
        self.coordinates_two = StringVar()
        self.average_rgb = StringVar()
        self.average_hex = StringVar()
        self.yonder_value = StringVar()
        self.gender_value = StringVar()

        # May need to change image to self.image
        self.image = Image.open(self.image_directory).convert("RGB").resize((self.width, self.height), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(self.image)

        # Canvas setup
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack(side="left", expand=True, padx=10, pady=10)
        # Suppose to replace this line with the one below, leaving this comment for reverting
        # Seems to be working but leave line for now and clean once everything is done
        # self.canvas.create_image(0, 0, anchor=NW, image=self.tk_image)
        self.canvas_image_id = self.canvas.create_image(0, 0, anchor=NW, image=self.tk_image)

        # Bind events to canvas
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # Panel setup
        self.panel = Frame(root, width=200, height=self.height)
        self.panel.pack(side="left", fill="y", padx=5, pady=5)
        Label(self.panel, text="Selection Info", font=("Arial", 12, "bold")).pack(pady=(0, 10))

        # Add buttons and fields
        Label(self.panel, text="Coordinates:").pack(anchor='w')
        Entry(self.panel, textvariable=self.coordinates_one, state='readonly').pack()
        Entry(self.panel, textvariable=self.coordinates_two, state='readonly').pack(pady=2)
        Label(self.panel, text="Average RGB:").pack(anchor='w', pady=(10, 0))
        Entry(self.panel, textvariable=self.average_rgb, state='readonly').pack()
        Label(self.panel, text="HEX Color:").pack(anchor='w', pady=(10, 0))
        Entry(self.panel, textvariable=self.average_hex, state='readonly').pack()
        Label(self.panel, text="Yonder Color:").pack(anchor='w', pady=(10, 0))
        Entry(self.panel, textvariable=self.yonder_value, state='readonly').pack()
        Label(self.panel, text="Select Gender:").pack(anchor='w', pady=(20, 5))
        Button(self.panel, text="Male", command=lambda: self.confirm_gender("Male"), width=15).pack(pady=2)
        Button(self.panel, text="Female", command=lambda: self.confirm_gender("Female"), width=15).pack(pady=2)

    def update_image(self, new_path):
        self.image_directory = new_path
        self.image = Image.open(self.image_directory).convert("RGB").resize((self.width, self.height), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(self.image)  # Keep a reference or it disappears
        self.canvas.itemconfig(self.canvas_image_id, image=self.tk_image)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.box_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_move_press(self, event):
        self.canvas.coords(self.box_id, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        x1, y1 = min(self.start_x, event.x), min(self.start_y, event.y)
        x2, y2 = max(self.start_x, event.x), max(self.start_y, event.y)

        region = self.image.crop((x1, y1, x2, y2))  # Specify the pixels within the box
        pixels = list(region.getdata())  # List of RGB values for each pixel within the box

        r_values = [pixel[0] for pixel in pixels]
        g_values = [pixel[1] for pixel in pixels]
        b_values = [pixel[2] for pixel in pixels]
        avg_r = sum(r_values) // len(r_values)
        avg_g = sum(g_values) // len(g_values)
        avg_b = sum(b_values) // len(b_values)
        avg_rgb = (avg_r, avg_g, avg_b)
        hex_color = '#%02x%02x%02x' % avg_rgb

        # Update info panel
        self.coordinates_one.set(f"({x1}, {y1})")
        self.coordinates_two.set(f"({x2}, {y2})")
        self.average_rgb.set(f"{avg_rgb}")
        self.average_hex.set(hex_color)
        self.yonder_value.set(self.calculate_yonder(avg_rgb))

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def calculate_yonder(self, avg_rgb):
        min_distance = float('inf')
        closest_tone = None
        yonder_tones = ["#E6C6BF", "#D4AFA3", "#C29C88", "#B18972", "#9B7966", "#886958", "#755848", "#614539", "#48352C", "#36251D"]

        for hex_value in yonder_tones:
            yonder_rgb = self.hex_to_rgb(hex_value)
            # Euclidean distance
            distance = sum((a - b) ** 2 for a, b in zip(avg_rgb, yonder_rgb)) ** 0.5

            if distance < min_distance:
                min_distance = distance
                closest_tone = hex_value
        return closest_tone

    def confirm_gender(self, gender):
        self.gender_value.set(gender)
        self.update_image("C:\\Users\\brian\\OneDrive\\Python Projects\\Generative AI Image Bias\\Images\\DALL-E\\Arts and Creative Fields\\Freelancer Writer (Entry-Level)\\02.png")




if __name__ == "__main__":
    root = Tk()
    app = SkinToneGenderApp(root)
    root.mainloop()

