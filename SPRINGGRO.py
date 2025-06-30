import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext, PhotoImage

# Sample plant database with image paths
plant_database = {
    "Daffodil": {
        "info": "Bright yellow spring flower. Origin: Europe. Grows in 6-8 weeks.",
        "image": "daffodil.png"
    },
    "Tulip": {
        "info": "Colorful bulb plant. Origin: Central Asia. Grows in spring.",
        "image": "tulip.png"
    },
    "Crocus": {
        "info": "Small purple flower. Origin: Europe/Asia. Blooms early spring.",
        "image": "crocus.png"
    }
}

library_plants = list(plant_database.keys())

# Main App Class
class SpringGrowApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Spring Grow")
        self.geometry("400x500")
        self.minsize(300, 400)
        self.current_frame = None
        self.plant_images = {}  # Cache for PhotoImage objects
        self.show_welcome()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_welcome(self):
        self.clear_frame()
        frame = tk.Frame(self)
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="Welcome to Spring Grow!", font=("Arial", 16)).pack(pady=20)
        tk.Button(frame, text="Get Started", command=self.show_library).pack(pady=10)
        
        self.current_frame = frame

    def show_library(self):
        self.clear_frame()
        frame = tk.Frame(self)
        frame.pack(expand=True, fill='both')

        tk.Label(frame, text="Your Plant Library", font=("Arial", 14)).pack(pady=10)

        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for plant in library_plants:
            plant_frame = tk.Frame(scroll_frame, bd=1, relief="solid", padx=5, pady=5)
            plant_frame.pack(fill="x", pady=5, padx=5)

            image_path = plant_database[plant].get("image")
            if image_path and image_path not in self.plant_images:
                try:
                    self.plant_images[image_path] = PhotoImage(file=image_path)
                except:
                    self.plant_images[image_path] = None

            img_label = tk.Label(plant_frame)
            if self.plant_images.get(image_path):
                img_label.config(image=self.plant_images[image_path])
                img_label.image = self.plant_images[image_path]
            img_label.pack(side="left", padx=5)

            name_button = tk.Button(plant_frame, text=plant, command=lambda p=plant: self.show_plant_info(p))
            name_button.pack(side="left", padx=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        button_frame = tk.Frame(frame)
        button_frame.pack(side="bottom", pady=10, fill="x")

        tk.Button(button_frame, text="+ Add New Plant", command=self.add_plant_page).pack(side="left", padx=5)
        tk.Button(button_frame, text="Back to Home", command=self.show_welcome).pack(side="right", padx=5)

        self.current_frame = frame

    def show_plant_info(self, plant_name):
        self.clear_frame()
        frame = tk.Frame(self)
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text=plant_name, font=("Arial", 16)).pack(pady=10)

        info_text = plant_database.get(plant_name, {}).get("info", "No information available.")
        info_box = scrolledtext.ScrolledText(frame)
        info_box.pack(pady=10, expand=True, fill="both")
        info_box.insert(tk.END, info_text)
        info_box.config(state='disabled')

        def delete_plant():
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {plant_name}?")
            if confirm:
                if plant_name in plant_database:
                    del plant_database[plant_name]
                if plant_name in library_plants:
                    library_plants.remove(plant_name)
                messagebox.showinfo("Deleted", f"{plant_name} has been deleted from your library.")
                self.show_library()

        button_frame = tk.Frame(frame)
        button_frame.pack(side="bottom", pady=10, fill="x")

        tk.Button(button_frame, text="Delete Plant", command=delete_plant).pack(side="left", padx=5)
        tk.Button(button_frame, text="Back to Library", command=self.show_library).pack(side="right", padx=5)

        self.current_frame = frame

    def add_plant_page(self):
        self.clear_frame()
        frame = tk.Frame(self)
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="AI Plant Scanner (Simulated)", font=("Arial", 14)).pack(pady=10)

        def simulate_ai_scan():
            scan_window = tk.Toplevel(self)
            scan_window.title("AI Scanning...")
            scan_window.geometry("300x200")
            
            tk.Label(scan_window, text="Scanning plant image...", font=("Arial", 12)).pack(pady=20)
            self.after(2000, lambda: show_scan_result(scan_window))  # Simulate a 2 second scan

        def show_scan_result(scan_window):
            for widget in scan_window.winfo_children():
                widget.destroy()
            
            tk.Label(scan_window, text="AI Identified: Lavender", font=("Arial", 12)).pack(pady=10)
            tk.Label(scan_window, text="Fragrant purple flower. Origin: Mediterranean. Grows in spring/summer.").pack(pady=10)
            
            def add_plant():
                plant_database["Lavender"] = {
                    "info": "Fragrant purple flower. Origin: Mediterranean. Grows in spring/summer.",
                    "image": "lavender.png"
                }
                library_plants.append("Lavender")
                messagebox.showinfo("Success", "Lavender added to your library!")
                scan_window.destroy()
                self.show_library()
            
            tk.Button(scan_window, text="Add to Library", command=add_plant).pack(pady=5)
            tk.Button(scan_window, text="Cancel", command=scan_window.destroy).pack(pady=5)

        tk.Button(frame, text="Simulate AI Scan", command=simulate_ai_scan).pack(pady=20)

        button_frame = tk.Frame(frame)
        button_frame.pack(side="bottom", pady=10, fill="x")

        tk.Button(button_frame, text="Back to Library", command=self.show_library).pack(side="right", padx=5)

        self.current_frame = frame

# Run the App
if __name__ == "__main__":
    app = SpringGrowApp()
    app.mainloop()

