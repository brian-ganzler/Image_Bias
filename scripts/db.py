import sqlite3
from sqlite3 import Error
import sys
import os
import hashlib
import stone
from deepface import DeepFace
from tkinter import *
from PIL import Image, ImageTk

def main():
    conn = create_connection("image_bias_analysis.db")  # Connect to the specified database

    # Create tables if they don't exist
    create_model_table = '''CREATE TABLE IF NOT EXISTS Model (
                                model_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                model_name TEXT NOT NULL UNIQUE);'''
    create_theme_table = '''CREATE TABLE IF NOT EXISTS Theme (
                                theme_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                theme_name TEXT NOT NULL UNIQUE);'''
    create_prompt_table = '''CREATE TABLE IF NOT EXISTS Prompt (
                                prompt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                theme_id INTEGER NOT NULL,
                                prompt_name TEXT NOT NULL UNIQUE,
                                FOREIGN KEY (theme_id) REFERENCES Theme(theme_id));'''
    create_image_table = '''CREATE TABLE IF NOT EXISTS Image (
                                image_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                image_hash TEXT NOT NULL,
                                image_directory TEXT NOT NULL,
                                model_id INTEGER NOT NULL,
                                prompt_id INTEGER NOT NULL,
                                image_name TEXT NOT NULL,
                                FOREIGN KEY (model_id) REFERENCES Model (model_id),
                                FOREIGN KEY (prompt_id) REFERENCES Prompt(prompt_id));'''
    create_tone_analysis_table = '''CREATE TABLE IF NOT EXISTS ToneAnalysis (
                                tone_analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                image_id INTEGER NOT NULL,
                                dominant_tone_percent REAL,
                                dominant_tone TEXT,
                                predicted_tone_accuracy REAL,
                                predicted_tone TEXT,
                                manual_coordinates TEXT,
                                manual_rgb TEXT,
                                manual_hex TEXT,
                                manual_skin_tone TEXT,
                                FOREIGN KEY (image_id) REFERENCES Image(image_id));'''
    create_gender_analysis_table = '''CREATE TABLE IF NOT EXISTS GenderAnalysis (
                                    gender_analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    image_id INTEGER NOT NULL,
                                    predicted_gender TEXT,
                                    manual_coordinates TEXT,
                                    manual_gender TEXT,
                                    FOREIGN KEY (image_id) REFERENCES Image(image_id));'''

    # Scan directory for new images and updating the database
    response = input("Do you want to scan for new files: ")
    if response == "Y":
        print('Scanning...')
        tables = [create_model_table, create_theme_table, create_prompt_table, create_image_table, create_tone_analysis_table, create_gender_analysis_table]
        for table in tables:  # Create tables specified in the list above
            create_table(conn, table)
        root = "C:\\Users\\brian\\OneDrive\\Python Projects\\Generative AI Image Bias\\Images"  # Directory for folder to be scanned
        # Directory must have a model folder, theme folder, prompt folder otherwise loop will have to be refactored
        for model in os.listdir(root):  # Loop through each model in  the directory
            model_id = create_model(conn, {"model_name": model})
            for theme in os.listdir(os.path.join(root, model)):  # Loop through each theme in the model directory
                theme_id = create_theme(conn, {"theme_name": theme})
                for prompt in os.listdir(os.path.join(root, model, theme)):  # Loop through each prompt in the theme directory
                    prompt_id = create_prompt(conn, {"theme_id": theme_id, "prompt_name": prompt})
                    count = 0
                    for image in os.listdir(os.path.join(root, model, theme, prompt)):  # Loop through each image in the prompt directory
                        if count < 20:  # Database is set to add the first twenty images to the database
                            count += 1
                            image_directory = os.path.join(root, model, theme, prompt, image)  # Directory for each image
                            image_hash = hash_image(image_directory)  # Hash image for the database in the event image name is changed, hash can always be used to identify the image
                            create_image(conn, {"image_hash": image_hash, "image_directory": image_directory, "model_id": model_id, "prompt_id": prompt_id, "image_name": image}) # Function call to create new record in Image table
        print("Scan Complete\n")

    # Scan newly added images to the database for predicted skin tone
    response = input("Do you want to calculate skin tone: ")
    if response == "Y":
        print("Calculating skin tone...")
        predicted_skin_tone(conn)  # Function calls to use the Skin-Tone-Classifier library to predict skin tone
        print("Skin Tone Analysis Complete\n")

    # Scan newly added images to the database for predicted gender
    response = input("Do you want to calculate gender: ")
    if response == "Y":
        print("Calculating gender...")
        predicted_gender(conn)  # Function calls to use DeepFace to predict gender
        print("Gender Analysis Complete\n")

    # Manually categorize skin tone and gender
    response = input("Do you want to categorize skin tone and gender manually: ")
    if response == "Y":
        root = Tk()  # Create window using tkinter for GUI
        app = SkinToneGenderApp(root, conn)  # Initialize instance SkinToneGenderApp class
        root.mainloop()  # Keep the window open


def hash_image(image_directory):
    with open(image_directory, "rb") as f:
        data = f.read()
    return hashlib.md5(data).hexdigest()

def count_image_rows(conn): # This function may not be used at all since I can always look at DB Browser
    try:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM Image")
        count = c.fetchone()[0]
        print(f"Total rows in Image table: {count}")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

def list_row_with_names(conn):  # May want to keep this function for troubleshooting images
    try:
        c = conn.cursor()
        query = """SELECT Image.image_id, Image.image_directory, Model.model_name, Theme.theme_name, Prompt.prompt_name, Image.image_name  
                   FROM Image 
                    JOIN Model ON Image.model_id = Model.model_id 
                    JOIN Prompt ON Image.prompt_id = Prompt.prompt_id 
                    JOIN THEME on Prompt.theme_id = Theme.theme_id """
        c.execute(query)
        rows = c.fetchall()

        if rows:
            columns = [description[0] for description in c.description]
            for row in rows:
                print('-' * 40)
                for col, val in zip(columns, row):
                    print(f"{col}: {val}")

        else:
            print("No matching rows found.")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

def create_connection(db_file):
    try:
        print(f"Connecting to database file {db_file}.")
        conn = sqlite3.connect(db_file)
        print("Connected.\n")
        return conn
    except Error as e:
        print(f"Error connecting to database: \n{e}")
        sys.exit(1)

def create_table(conn, table):
    try:
        c = conn.cursor()
        c.execute(table)
    except Error as e:
        print(f"Error creating table: \n{e}")
        sys.exit(1)

def list_table(conn):
    try:
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = c.fetchall()
        print("List of Available Tables: ")
        print('-'*30)
        for table in tables:
            print(table[0])
        print()
    except Error as e:
        print(f"Error listing all tables: \n{e}")
        sys.exit(1)

def create_model(conn, model):
    try:
        c = conn.cursor()
        sql = "SELECT model_id from Model WHERE model_name = ?"
        c.execute(sql, (model["model_name"],))
        res = c.fetchone()
        if res:
            return res[0]
        sql = "INSERT INTO Model(model_name) VALUES (?)"
        c.execute(sql, (model["model_name"],))
        conn.commit()
        return c.lastrowid
    except Error as e:
        print(f"Error creating model: \n{e}")
        sys.exit(1)

def list_column(conn, table, column):
    try:
        c = conn.cursor()
        query = f"SELECT {column} FROM {table}"
        c.execute(query)
        res = c.fetchall()
        print(f"List of {table}: ")
        print('-' * 30)
        for row in res:
            print(row[0])
        print()
        return res
    except Error as e:
        print(f"Error listing {table}: \n{e}")

def create_theme(conn, theme):
    try:
        c = conn.cursor()
        sql = "SELECT theme_id from Theme WHERE theme_name = ?"
        c.execute(sql, (theme["theme_name"],))
        res = c.fetchone()
        if res:
            return res[0]
        sql = "INSERT INTO Theme(theme_name) VALUES (?)"
        c.execute(sql, (theme["theme_name"],))
        conn.commit()
        return c.lastrowid
    except Error as e:
        print(f"Error creating theme: \n{e}")
        sys.exit(1)


def create_prompt(conn, prompt):
    try:
        c = conn.cursor()
        sql = "SELECT prompt_id FROM Prompt WHERE prompt_name = ?"
        c.execute(sql, (prompt["prompt_name"],))
        res = c.fetchone()
        if res:
            return res[0]
        sql = "INSERT INTO Prompt(theme_id, prompt_name) VALUES (?, ?)"
        c.execute(sql, (prompt["theme_id"], prompt["prompt_name"],))
        conn.commit()
        return c.lastrowid
    except Error as e:
        print(f"Error creating prompt: \n{e}")
        sys.exit(1)

def create_image(conn, image):
    sql = '''INSERT OR IGNORE INTO Image(image_hash, image_directory, model_id, prompt_id, image_name) VALUES (?, ?, ?, ?, ?)'''
    try:
        c = conn.cursor()
        c.execute(sql, (image["image_hash"], image["image_directory"], image["model_id"], image["prompt_id"], image["image_name"]))
        conn.commit()
        return c.lastrowid
    except Error as e:
        print(f"Error creating image: \n{e}")
        sys.exit(1)

def create_tone_analysis(conn, tone_analysis):
    sql = '''INSERT OR IGNORE INTO ToneAnalysis(image_id, dominant_tone_percent, dominant_tone, 
                predicted_tone_accuracy, predicted_tone, manual_skin_tone) VALUES (?, ?, ?, ?, ?, ?)'''
    try:
        c = conn.cursor()
        c.execute(sql, (tone_analysis["image_id"], tone_analysis["dominant_tone_percent"], tone_analysis["dominant_tone"],
                        tone_analysis["predicted_tone_accuracy"], tone_analysis["predicted_tone"],tone_analysis["manual_skin_tone"]))
        conn.commit()
        return c.lastrowid
    except Error as e:
        print(f"Error creating skin tone analysis: \n{e}")
        sys.exit(1)


def create_gender_analysis(conn, gender_analysis):
    sql = '''INSERT OR IGNORE INTO GenderAnalysis(image_id, predicted_gender, manual_gender) VALUES (?, ?, ?)'''
    try:
        c = conn.cursor()
        c.execute(sql, (gender_analysis["image_id"], gender_analysis["predicted_gender"], gender_analysis["manual_gender"]))
        conn.commit()
        return c.lastrowid
    except Error as e:
        print(f"Error creating analysis: \n{e}")
        sys.exit(1)

def predicted_skin_tone(conn):
    # Need to add a way to update if new images are generated
    sql = '''SELECT image_id, image_directory, image_hash FROM Image'''
    c = conn.cursor()
    c.execute(sql)
    response = c.fetchall()
    for image_id, image_directory, image_hash in response:
        try:
            if image_hash != hash_image(image_directory):
                print(f"Image hash does not match database hash: \n{image_directory}\n")
            result = stone.process(image_directory, image_type="color", tone_palette="yadon-ostfeld", return_report_image=True)  # Process data from an image
            tone_analysis = {"image_id": image_id, "dominant_tone_percent": (float(result["faces"][0]["dominant_colors"][0]["percent"])*100), "dominant_tone": result["faces"][0]["dominant_colors"][0]['color'],
                             "predicted_tone_accuracy": result["faces"][0]['accuracy'], "predicted_tone": result["faces"][0]['skin_tone'], "manual_skin_tone": None}
            create_tone_analysis(conn, tone_analysis)
        except Exception as e:
            tone_analysis = {"image_id": image_id, "dominant_tone_percent": None, "dominant_tone": None,
                             "predicted_tone_accuracy": None, "predicted_tone": None, "manual_skin_tone": None}
            create_tone_analysis(conn, tone_analysis)
            print(f"Unable to predict skin tone for: \n{image_directory}\n{e}\n")


def predicted_gender(conn):
    sql = '''SELECT Image.image_id, image_directory, image_hash FROM Image
                    JOIN GenderAnalysis ON Image.image_id = GenderAnalysis.image_id
                    WHERE GenderAnalysis.manual_gender IS NULL'''
    c = conn.cursor()
    c.execute(sql)
    response = c.fetchall()
    for image_id, image_directory, image_hash in response:
        try:
            if image_hash != hash_image(image_directory):
                print(f"Image hash does not match database hash: \n{image_directory}\n")
            result = DeepFace.analyze(image_directory, actions=['gender'], detector_backend='mtcnn')
            gender_analysis = {"image_id": image_id, "predicted_gender": result[0]['dominant_gender'], "manual_gender": None}
            create_gender_analysis(conn, gender_analysis)
        except Exception as e:
            gender_analysis = {"image_id": image_id, "predicted_gender": None, "manual_gender": None}
            create_gender_analysis(conn, gender_analysis)
            print(f"Unable to predict gender for: \n{image_directory}\n{e}\n")

class SkinToneGenderApp:
    def __init__(self, root, conn):
        self.conn = conn
        self.root = root
        self.width, self.height = 800, 600
        self.root.title("Skin Tone and Gender Analysis")
        self.root.geometry(f"{self.width + 200}x{self.height}")

        self.coordinates_one = StringVar()
        self.coordinates_two = StringVar()
        self.average_rgb = StringVar()
        self.average_hex = StringVar()
        self.yonder_value = StringVar()
        self.gender_value = StringVar()

        # Canvas setup
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack(side="left", expand=True, padx=10, pady=10)

        # Load image data after canvas is created
        self.image_data = self.query_image_list()
        self.image_index = 0


        if self.image_data:
            image_id, image_directory, image_hash = self.image_data[self.image_index]
            self.current_image_id = image_id
            print(image_id)
            self.image = Image.open(image_directory).convert("RGB").resize((self.width, self.height),
                                                                           Image.Resampling.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas_image_id = self.canvas.create_image(0, 0, anchor=NW, image=self.tk_image)
            self.image_directory = image_directory  # Store the current path
        else:
            self.canvas_image_id = self.canvas.create_image(0, 0, anchor=NW)

        self.box_id = None

        # Bind events to canvas
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # Panel setup
        self.panel = Frame(root, width=200, height=self.height)
        self.panel.pack(side="left", fill="y", padx=5, pady=5)
        Label(self.panel, text="Selection Info", font=("Arial", 12, "bold")).pack(pady=(0, 10))

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

    def query_image_list(self):
        sql = '''SELECT Image.image_id, image_directory, image_hash FROM Image
                    JOIN GenderAnalysis ON Image.image_id = GenderAnalysis.image_id
                    WHERE GenderAnalysis.manual_gender IS NULL'''
        c = self.conn.cursor()
        c.execute(sql)
        response = c.fetchall()
        return response

    def update_image(self, new_path):
        if self.box_id:
            self.canvas.delete(self.box_id)
            self.box_id = None

        self.image_directory = new_path
        self.image = Image.open(self.image_directory).convert("RGB").resize((self.width, self.height), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(self.image)  # Keep a reference or it disappears
        self.canvas.itemconfig(self.canvas_image_id, image=self.tk_image)

    def on_button_press(self, event):
        if hasattr(self, 'box_id') and self.box_id:
            self.canvas.delete(self.box_id)

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
        if self.yonder_value.get() != "":

            self.gender_value.set(gender)
            coordinates = f"{self.coordinates_one.get()} to {self.coordinates_two.get()}"
            average_rgb = self.average_rgb.get()
            average_hex = self.average_hex.get()
            yonder_hex = self.yonder_value.get()
            gender = self.gender_value.get()

            sql = '''UPDATE ToneAnalysis SET manual_coordinates = ?,  manual_rgb = ?, manual_hex = ?, manual_skin_tone = ?  WHERE image_id = ?'''
            c = self.conn.cursor()
            c.execute(sql, (coordinates, average_rgb, average_hex, yonder_hex, self.current_image_id))
            self.conn.commit()
            
            sql = "UPDATE GenderAnalysis SET manual_coordinates = ?, manual_gender = ? WHERE image_id = ?"
            c.execute(sql, (coordinates, gender, self.current_image_id))

            self.image_index += 1
            if self.image_index < len(self.image_data):
                image_id, image_directory, image_hash = self.image_data[self.image_index]
                self.current_image_id = image_id
                self.update_image(image_directory)

                self.coordinates_one.set("")
                self.coordinates_two.set("")
                self.average_rgb.set("")
                self.average_hex.set("")
                self.yonder_value.set("")
                self.gender_value.set("")
        else:
            print("Fields not filled out.")

if __name__ == "__main__":
    main()
