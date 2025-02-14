import tkinter as tk  # Importing the Tkinter library for GUI
from tkinter import ttk  # Importing themed Tkinter widgets
from PIL import Image, ImageTk  # Importing PIL for handling images
import requests  # Importing requests to fetch data from an API
from io import BytesIO  # Importing BytesIO to handle image data

# Function to fetch exchange rates from an API
def fetch_exchange_rates():
    url = "https://api.exchangerate-api.com/v4/latest/PLN"  # API endpoint for exchange rates with PLN as the base currency
    response = requests.get(url)  # Sending a GET request to the API
    if response.status_code == 200:  # Checking if the request was successful
        return response.json().get("rates", {})  # Extracting exchange rates from the JSON response
    return {}  # Returning an empty dictionary if request fails

# Function to load currency flag images from an external source
def load_flag_images():
    base_url = "https://flagcdn.com/w40/{}.png"  # URL pattern for flag images
    country_codes = {  # Dictionary mapping currency codes to country codes for flags
        "USD": "us", "EUR": "eu", "GBP": "gb", "INR": "in",
        "AUD": "au", "CAD": "ca", "SGD": "sg", "CHF": "ch",
        "MYR": "my", "JPY": "jp"
    }
    images = {}  # Dictionary to store the flag images
    for code, country in country_codes.items():  # Loop through each currency and country code pair
        try:
            response = requests.get(base_url.format(country), stream=True)  # Fetch flag image from URL
            if response.status_code == 200:  # If request was successful
                image = Image.open(BytesIO(response.content))  # Open image using PIL
                images[code] = ImageTk.PhotoImage(image)  # Convert image to Tkinter-compatible format
        except Exception:
            pass  # Ignore errors if image fetching fails
    return images  # Return dictionary containing flag images

# GUI Application class
class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root  # Assign the root Tkinter window
        self.root.title("Currency Converter")  # Set the window title
        self.root.geometry("700x400")  # Set the window size

        
        self.rates = fetch_exchange_rates()  # Fetch exchange rates when the app starts
        self.flag_images = load_flag_images()  # Load flag images

        # Header Label
        tk.Label(root, text="1 PLN =", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=10)
        
        # Listbox to display exchange rates
        self.rate_list = tk.Listbox(root, height=10, width=30)
        self.rate_list.grid(row=1, column=0, rowspan=5, padx=10, pady=5)
        self.update_rates_list()  # Populate the listbox with exchange rates
        
        # Refresh button to update exchange rates
        tk.Button(root, text="Refresh Exchange Rates", command=self.refresh_rates).grid(row=6, column=0, padx=10, pady=5)
        
        # Input field for amount
        tk.Label(root, text="Enter amount:").grid(row=1, column=1, sticky="w", padx=10)
        self.amount_entry = tk.Entry(root)  # Entry widget to accept amount input
        self.amount_entry.grid(row=1, column=2, padx=10)
        
        # Dropdown for selecting the currency to convert from
        tk.Label(root, text="From:").grid(row=2, column=1, sticky="e", padx=5)
        self.from_currency = ttk.Combobox(root, values=list(self.rates.keys()), state="readonly")  # Combobox with currency options
        self.from_currency.grid(row=2, column=2, padx=5)
        self.from_currency.set("PLN")  # Default selection as PLN
        
        # Dropdown for selecting the currency to convert to
        tk.Label(root, text="To:").grid(row=3, column=1, sticky="e", padx=5)
        self.to_currency = ttk.Combobox(root, values=list(self.rates.keys()), state="readonly")  # Combobox with currency options
        self.to_currency.grid(row=3, column=2, padx=5)
        
        # Convert button
        self.convert_button = tk.Button(root, text="Convert", command=self.convert)  # Button to trigger conversion
        self.convert_button.grid(row=4, column=2, padx=5, pady=5)
        
        # Label to display conversion results
        self.result_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
        self.result_label.grid(row=5, column=1, columnspan=2, pady=10)
    
    # Function to update the exchange rate listbox
    def update_rates_list(self):
        self.rate_list.delete(0, tk.END)  # Clear the listbox
        for currency, rate in self.rates.items():  # Loop through exchange rates
            if currency != "PLN":  # Exclude PLN as it's the base currency
                self.rate_list.insert(tk.END, f"{currency}: {rate:.6f}")  # Insert formatted exchange rate into listbox
    
    # Function to refresh exchange rates
    def refresh_rates(self):
        self.rates = fetch_exchange_rates()  # Fetch latest rates
        self.from_currency["values"] = list(self.rates.keys())  # Update currency dropdown
        self.to_currency["values"] = list(self.rates.keys())  # Update currency dropdown
        self.update_rates_list()  # Refresh the listbox
    
    # Function to perform currency conversion
    def convert(self):
        try:
            amount = float(self.amount_entry.get())  # Get amount entered by user
            from_curr = self.from_currency.get()  # Get selected currency to convert from
            to_curr = self.to_currency.get()  # Get selected currency to convert to
            if from_curr in self.rates and to_curr in self.rates:  # Check if currencies are valid
                converted_amount = round(amount * self.rates[to_curr] / self.rates[from_curr], 2)  # Convert amount
                self.result_label.config(text=f"{amount} {from_curr} = {converted_amount} {to_curr}")  # Display result
            else:
                self.result_label.config(text="Invalid currency selection")  # Show error message
        except ValueError:
            self.result_label.config(text="Please enter a valid amount")  # Handle invalid input error

# Running the application
if __name__ == "__main__":
    root = tk.Tk()  # Create the root Tkinter window
    app = CurrencyConverterApp(root)  # Initialize the application
    root.mainloop()  # Start the Tkinter event loop
