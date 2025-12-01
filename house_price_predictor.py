
import pandas as pd
from sklearn.linear_model import LinearRegression
import tkinter as tk
from tkinter import messagebox, ttk
import tkinter.font as tkFont
import os
import sys

# --- Asset Handling for PyInstaller ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# --- Machine Learning Model ---
def train_model():
    """
    Loads the dataset and trains a Linear Regression model.
    """
    try:
        # Load the dataset using the resource_path function
        csv_path = resource_path('tunisia_house_prices.csv')
        data = pd.read_csv(csv_path)

        # Define features (X) and target (y)
        features = ['size_sqft', 'bedrooms', 'age']
        target = 'price'

        X = data[features]
        y = data[target]

        # Create and train the Linear Regression model
        model = LinearRegression()
        model.fit(X, y)
        
        return model
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Le fichier 'tunisia_house_prices.csv' est introuvable.")
        return None
    except Exception as e:
        messagebox.showerror("Erreur de chargement du modèle", f"Une erreur est survenue: {e}")
        return None

# Train the model when the script starts
model = train_model()

# --- GUI ---
def predict_price():
    """
    Gets user input, predicts the price, and displays it in the main window.
    """
    if model is None:
        prediction_label.config(text="Le modèle n'a pas pu être chargé.", foreground="#FF0000")
        return

    try:
        # Get input values from the GUI
        size = float(entry_size.get())
        bedrooms = int(entry_bedrooms.get())
        age = int(entry_age.get())

        # Validate input ranges
        if not (0 < size < 1000 and 0 < bedrooms < 10 and 0 <= age < 100):
            messagebox.showerror("Erreur d'entrée", "Veuillez entrer des valeurs réalistes.")
            return

        # Create a DataFrame for the input
        input_data = pd.DataFrame([[size, bedrooms, age]], columns=['size_sqft', 'bedrooms', 'age'])

        # Predict the price
        predicted_price = model.predict(input_data)[0]

        # Display the result
        prediction_label.config(text=f"Prix estimé: {predicted_price:,.0f} TND", foreground="#00FF00")

    except ValueError:
        prediction_label.config(text="Veuillez entrer des valeurs numériques valides.", foreground="#FF0000")
    except Exception as e:
        prediction_label.config(text=f"Une erreur est survenue: {e}", foreground="#FF0000")


# --- Window Setup ---
root = tk.Tk()
root.title("Prédicteur de prix de maison - Tunisie")
root.geometry("600x450")
root.resizable(False, False)

# Set the application icon
try:
    logo_path = resource_path("logo.png")
    logo_image = tk.PhotoImage(file=logo_path)
    root.iconphoto(True, logo_image)
except tk.TclError:
    print("Logo 'logo.png' non trouvé ou format non supporté. L'icône par défaut sera utilisée.")
except Exception as e:
    print(f"Erreur lors du chargement de l'icône: {e}")


# --- Styling ---
BG_COLOR = "#1A1A1A"
FG_COLOR = "#E0E0E0"
ACCENT_COLOR = "#6A0DAD"
ENTRY_BG = "#333333"
ENTRY_FG = "#FFFFFF"

root.configure(bg=BG_COLOR)

# --- Fonts ---
title_font = tkFont.Font(family="Helvetica Neue", size=20, weight="bold")
label_font = tkFont.Font(family="Helvetica Neue", size=12)
entry_font = tkFont.Font(family="Helvetica Neue", size=12)
button_font = tkFont.Font(family="Helvetica Neue", size=14, weight="bold")
prediction_font = tkFont.Font(family="Helvetica Neue", size=16, weight="bold")

# --- Main Layout ---
main_frame = tk.Frame(root, bg=BG_COLOR, padx=30, pady=30)
main_frame.pack(expand=True, fill="both")

# Title
title_label = tk.Label(main_frame, text="PRÉDICTEUR DE PRIX DE MAISON", font=title_font, bg=BG_COLOR, fg=ACCENT_COLOR)
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))

# Input Fields
tk.Label(main_frame, text="Taille (m²):", font=label_font, bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_size = tk.Entry(main_frame, font=entry_font, bg=ENTRY_BG, fg=ENTRY_FG, relief="flat", highlightthickness=1)
entry_size.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

tk.Label(main_frame, text="Chambres:", font=label_font, bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry_bedrooms = tk.Entry(main_frame, font=entry_font, bg=ENTRY_BG, fg=ENTRY_FG, relief="flat", highlightthickness=1)
entry_bedrooms.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

tk.Label(main_frame, text="Âge (années):", font=label_font, bg=BG_COLOR, fg=FG_COLOR).grid(row=3, column=0, padx=10, pady=10, sticky="w")
entry_age = tk.Entry(main_frame, font=entry_font, bg=ENTRY_BG, fg=ENTRY_FG, relief="flat", highlightthickness=1)
entry_age.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

# Configure column weights
main_frame.grid_columnconfigure(1, weight=1)

# Prediction Button
predict_button = tk.Button(main_frame, text="PRÉDIRE LE PRIX", command=predict_price, font=button_font, bg=ACCENT_COLOR, fg=FG_COLOR, relief="flat", padx=20, pady=10)
predict_button.grid(row=5, column=0, columnspan=2, pady=30)

# Prediction Result Label
prediction_label = tk.Label(main_frame, text="Entrez les détails et cliquez sur Prédire", font=prediction_font, bg=BG_COLOR, fg=FG_COLOR, wraplength=500)
prediction_label.grid(row=6, column=0, columnspan=2, pady=(10, 0))

# --- Start GUI ---
root.mainloop()
