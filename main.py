import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class CSVViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x500")
        self.title("CSV Viewer")

        # Create a frame to hold the options
        self.options_frame = tk.Frame(self)
        self.options_frame.pack(side="top", fill="x", padx=5, pady=5)

        # Create the option button to use the semicolon separator
        self.sep_var = tk.BooleanVar()
        self.sep_button = tk.Checkbutton(self.options_frame, text="Use semicolon separator (;) in header", variable=self.sep_var)
        self.sep_button.pack(side="left")

        # Create the button to load the CSV data
        self.load_button = tk.Button(self.options_frame, text="Load CSV", command=self.load_csv)
        self.load_button.pack(side="left", padx=5)

        # Create the button to visualize the CSV data
        self.visualize_button = tk.Button(self.options_frame, text="Visualize Data", command=self.visualize_data)
        self.visualize_button.pack(side="left")

        # Create a frame to hold the chart type options
        self.chart_type_frame = tk.Frame(self.options_frame)
        self.chart_type_frame.pack(side="left")

        # Create a label for the chart type options
        chart_type_label = tk.Label(self.chart_type_frame, text="Chart Type:")
        chart_type_label.pack(side="left")

        # Create radio buttons for different visualization options
        self.visualization_var = tk.StringVar(value="bar")
        self.bar_radio = tk.Radiobutton(self.options_frame, text="Bar Chart", variable=self.visualization_var, value="bar")
        self.pie_radio = tk.Radiobutton(self.options_frame, text="Pie Chart", variable=self.visualization_var, value="pie")
        self.line_radio = tk.Radiobutton(self.options_frame, text="Line Graph", variable=self.visualization_var, value="line")
        self.bar_radio.pack(side="left", padx=5)
        self.pie_radio.pack(side="left", padx=5)
        self.line_radio.pack(side="left", padx=5)

        # Create a frame to hold the canvas and scrollbar
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(side="top", fill="both", expand=True)

        # Create a scrollbar
        self.scrollbar = tk.Scrollbar(self.canvas_frame)
        self.scrollbar.pack(side="right", fill="y")

        # Create a canvas
        self.canvas = tk.Canvas(self.canvas_frame, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Configure the scrollbar to scroll the canvas
        self.scrollbar.config(command=self.canvas.yview)

        # Bind the canvas to the scrollbar
        self.canvas.bind("<Configure>", lambda event, canvas=self.canvas: self.on_canvas_configure(canvas))

        # Set the data frame to None initially
        self.df = pd.DataFrame()

        self.table = None

    def load_csv(self):
    # Open a file dialog to allow the user to select a file
        try:
            file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        except tk.TclError:
            return

        if not file_path:
            return

        # Read the CSV data using pandas
        sep = ";" if self.sep_var.get() else ","
        self.df = pd.read_csv(file_path, sep=sep)

        # Clear the canvas and scrollbar
        self.canvas.delete("all")
        self.scrollbar.set(0, 1)

        # Create a new table to display the CSV data
        self.table = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.table, anchor="nw")

        # Add the table headers to the table
        for i, column in enumerate(self.df.columns):
            label = tk.Label(self.table, text=column, relief="solid", borderwidth=1)
            label.grid(row=0, column=i, sticky="nsew")

        # Add the data rows to the table
        for i in range(len(self.df)):
            # Check if the row should be displayed based on user selection
            if self.row_var[i].get():
                for j, value in enumerate(self.df.iloc[i]):
                    # Check if the column should be displayed based on user selection
                    if self.column_var[j].get():
                        label = tk.Label(self.table, text=value, relief="solid", borderwidth=1)
                        label.grid(row=i+1, column=j, sticky="nsew")

        # Resize the columns to fit the data
        for i in range(len(self.df.columns)):
            # Get the maximum width of the cells in this column
            max_width = 0
            for j in range(len(self.df)):
                cell_text = str(self.df.iloc[j, i])
                cell_width = len(cell_text)
                if cell_width > max_width:
                    max_width = cell_width
            
            # Set the column width to the maximum cell width plus some padding
            self.table.columnconfigure(i, minsize=(max_width + 10))




    def visualize_data(self):
        if self.df.empty:
            return

        # Create a figure and axes using matplotlib
        fig, ax = plt.subplots()

        # Check which type of chart is selected and plot accordingly
        if self.visualization_var.get() == "bar":
            # Plot the data as a bar chart
            ax.bar(self.df.index, self.df[self.df.columns[0]])
            # Set the title and axis labels
            ax.set_title("CSV Data Visualization")
            ax.set_xlabel(self.df.index.name)
            ax.set_ylabel(self.df.columns[0])
        elif self.visualization_var.get() == "pie":
            # Plot the data as a pie chart
            ax.pie(self.df[self.df.columns[0]], labels=self.df.index)
            # Set the title
            ax.set_title("CSV Data Visualization")
        elif self.visualization_var.get() == "line":
            # Plot the data as a line graph
            ax.plot(self.df.index, self.df[self.df.columns[0]])
            # Set the title and axis labels
            ax.set_title("CSV Data Visualization")
            ax.set_xlabel(self.df.index.name)
            ax.set_ylabel(self.df.columns[0])

        # Create a canvas to display the plot
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()

        # Clear the canvas and scrollbar
        self.canvas.delete("all")
        self.scrollbar.set(0, 1)

        # Add the canvas to the scrollbar
        self.canvas.create_window((0, 0), window=canvas.get_tk_widget(), anchor="nw")
        canvas.get_tk_widget().bind("<Configure>", lambda event, canvas=self.canvas: self.on_canvas_configure(canvas))



    def on_canvas_configure(self, canvas):
        # Update the scrollbar to match the canvas size
        canvas.configure(scrollregion=canvas.bbox("all"))

if __name__ == "__main__":
    app = CSVViewer()
    app.mainloop()

