import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import subprocess
import pandas as pd

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My Application")

        # Create a container to hold the frames
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}  # Dictionary to store the frames

        self.show_frame(Frame1)  # Show the first frame at startup

    def show_frame(self, frame_class):
        # Hide the current frame and the second frame (if any)
        for frame in self.frames.values():
            frame.pack_forget()

        # Create the requested frame if it doesn't exist
        if frame_class not in self.frames:
            frame = frame_class(self.container, self)
            self.frames[frame_class] = frame

        # Show the requested frame
        frame = self.frames[frame_class]
        frame.pack(fill="both", expand=True)


class Frame1(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Create the first frame GUI elements here
        # ...
        # Function to save the input data to a CSV file
        def save_input_data():
            # Get the selected values from the input fields
            date = date_var.get()
            item_number = item_number_var.get()
            product_family = product_family_var.get()
            perishable = perishable_var.get()
            on_promotion = on_promotion_var.get()
            city = city_var.get()
            store_number = store_number_var.get()
            store_type = store_type_var.get()
            store_cluster = store_cluster_var.get()
            oil_price = oil_price_var.get()
            is_holiday = is_holiday_var.get()

            # Create a dictionary with the input data
            data = {
                'date': [date],
                'store_nbr': [store_number],
                'item_nbr': [item_number],
                'unit_sales': [0],  # Replace with the appropriate unit sales
                'onpromotion': [on_promotion],
                'city': [city],
                'type_x': [store_type],
                'cluster': [store_cluster],
                'family': [product_family],
                'perishable': [perishable],
                'type_y': ["Holiday" if is_holiday else ""],
                'locale': [""],
                'transferred': [""],
                'dcoilwtico': [oil_price]
            }

            # Create a DataFrame from the input data
            df = pd.DataFrame(data)

            # Get the output file path from the user
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                try:
                    # Save the DataFrame to the CSV file
                    df.to_csv(file_path, index=False)
                    tk.messagebox.showinfo("Success", "Input data saved successfully!")
                except Exception as e:
                    tk.messagebox.showerror("Error", f"Error saving input data: {str(e)}")

        # Create the Date input field
        date_label = tk.Label(self, text="Select a date:")
        date_label.pack(pady=10)
        date_var = tk.StringVar()
        date_entry = ttk.Combobox(self, textvariable=date_var, state="readonly")
        date_entry['values'] = pd.date_range(start='2023-07-11', end='2040-12-31', freq='D').strftime(
            '%Y-%m-%d').tolist()
        date_entry.pack()

        # Create the Item Number input field
        item_number_label = tk.Label(self, text="Item Number:")
        item_number_label.pack(pady=10)
        item_number_var = tk.StringVar()
        item_number_entry = ttk.Combobox(self, textvariable=item_number_var, state="readonly")
        item_number_entry['values'] = sorted(pd.read_csv("Data/salesdfAfterMerge.csv")['item_nbr'].unique().tolist())
        item_number_entry.pack()

        # Create the Product Family input field
        product_family_label = tk.Label(self, text="Product Family:")
        product_family_label.pack(pady=10)
        product_family_var = tk.StringVar()
        product_family_entry = ttk.Combobox(self, textvariable=product_family_var, state="readonly")
        product_family_entry['values'] = sorted(pd.read_csv("Data/salesdfAfterMerge.csv")['family'].unique().tolist())
        product_family_entry.pack()

        # Create the Perishable checkbox
        perishable_label = tk.Label(self, text="Is it perishable?")
        perishable_label.pack(pady=10)
        perishable_var = tk.IntVar()
        perishable_check = ttk.Checkbutton(self, text="Yes", variable=perishable_var)
        perishable_check.pack()

        # Create the On Promotion input field
        on_promotion_label = tk.Label(self, text="Is the product on promotion?")
        on_promotion_label.pack(pady=10)
        on_promotion_var = tk.StringVar()
        on_promotion_entry = ttk.Combobox(self, textvariable=on_promotion_var, state="readonly")
        on_promotion_entry['values'] = ["Yes", "No"]
        on_promotion_entry.pack()

        # Create the City input field
        city_label = tk.Label(self, text="City:")
        city_label.pack(pady=10)
        city_var = tk.StringVar()
        city_entry = ttk.Combobox(self, textvariable=city_var, state="readonly")
        city_entry['values'] = sorted(pd.read_csv("Data/salesdfAfterMerge.csv")['city'].unique().tolist())
        city_entry.pack()

        # Create the Store Number input field
        store_number_label = tk.Label(self, text="Store Number:")
        store_number_label.pack(pady=10)
        store_number_var = tk.StringVar()
        store_number_entry = ttk.Combobox(self, textvariable=store_number_var, state="readonly")
        store_number_entry['values'] = sorted(pd.read_csv("Data/salesdfAfterMerge.csv")['store_nbr'].unique().tolist())
        store_number_entry.pack()

        # Create the Store Type input field
        store_type_label = tk.Label(self, text="Store Type:")
        store_type_label.pack(pady=10)
        store_type_var = tk.StringVar()
        store_type_entry = ttk.Combobox(self, textvariable=store_type_var, state="readonly")
        store_type_entry['values'] = sorted(pd.read_csv("Data/salesdfAfterMerge.csv")['type_x'].unique().tolist())
        store_type_entry.pack()

        # Create the Store Cluster input field
        store_cluster_label = tk.Label(self, text="Store Cluster (1-17):")
        store_cluster_label.pack(pady=10)
        store_cluster_var = tk.IntVar()
        store_cluster_entry = ttk.Entry(self, textvariable=store_cluster_var)
        store_cluster_entry.pack()

        # Create the Oil Price input field
        oil_price_label = tk.Label(self, text="Oil Price:")
        oil_price_label.pack(pady=10)
        oil_price_var = tk.DoubleVar()
        oil_price_entry = ttk.Entry(self, textvariable=oil_price_var)
        oil_price_entry.pack()

        # Create the Is Holiday input field
        is_holiday_label = tk.Label(self, text="Is it a holiday?")
        is_holiday_label.pack(pady=10)
        is_holiday_var = tk.BooleanVar()
        is_holiday_check = ttk.Checkbutton(self, text="Yes", variable=is_holiday_var)
        is_holiday_check.pack()

        # Create the Save Data button
        save_button = tk.Button(self, text="Save Input Data", command=save_input_data)
        save_button.pack(pady=20)



        # Button to navigate to the second frame
        next_button = ttk.Button(self, text="Next", command=lambda: controller.show_frame(Frame2))
        next_button.pack(pady=10)


class Frame2(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Create the second frame GUI elements here
        # ...
        def load_input_data():
            file_path = filedialog.askopenfilename(title="Select Input Data File", filetypes=[("CSV files", "*.csv")])
            if file_path:
                try:
                    # Save the selected file directory to a text file
                    with open('input_data_path.txt', 'w') as file:
                        file.write(file_path)
                    messagebox.showinfo("Success", "Input data loaded successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Error loading input data: {str(e)}")

        def select_output_directory():
            directory = filedialog.askdirectory(title="Select Output Directory")
            if directory:
                try:
                    # Save the selected output directory to a text file
                    with open('output_directory_path.txt', 'w') as file:
                        file.write(directory)
                    messagebox.showinfo("Success", "Output directory selected successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Error selecting output directory: {str(e)}")

        # Function to deploy the ML model
        def deploy_model():
            try:
                # Run the deployment2y.py script using subprocess
                subprocess.run(["python", "deployment.py"])
                messagebox.showinfo("Success", "Model deployed successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error deploying the model: {str(e)}")

        # Create the Load Data button
        load_data_button = tk.Button(self, text="Load Input Data", command=load_input_data)
        load_data_button.pack(pady=20)

        # Create the Select Output Directory button
        select_output_button = tk.Button(self, text="Select Output Directory", command=select_output_directory)
        select_output_button.pack(pady=10)

        # Create the Deploy Model button
        deploy_button = tk.Button(self, text="Deploy Model", command=deploy_model)
        deploy_button.pack(pady=10)

        # Button to navigate back to the first frame
        back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame(Frame1))
        back_button.pack(pady=10)

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()


