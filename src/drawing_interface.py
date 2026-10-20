import customtkinter as ctk
from tkinter import Canvas, messagebox
from PIL import Image, ImageDraw
import os


class DrawingInterface(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Couleurs de l'interface
        self.bg_color = "#0B0B12"
        self.card_color = "#15152B"
        self.purple = "#7C3AED"
        self.purple_hover = "#9D5CFF"
        self.blue_night = "#252545"
        self.blue_hover = "#373763"
        self.text_color = "#F5F3FF"
        self.secondary_text = "#A5A3C7"

        # Configuration de la fenêtre
        self.title("AI Sketch - Reconnaissance de dessins")
        self.geometry("1150x720")
        self.minsize(950, 600)
        self.configure(fg_color=self.bg_color)

        # Variables du dessin
        self.brush_size = 8
        self.last_x = None
        self.last_y = None
        self.is_drawing = False

        # Image utilisée pour sauvegarder le dessin
        self.image = Image.new("RGB", (600, 450), "white")
        self.image_draw = ImageDraw.Draw(self.image)

        # Création de l'interface
        self.create_header()
        self.create_main_area()

    # En-tête de l'application
    def create_header(self):
        header = ctk.CTkFrame(
            self,
            fg_color=self.card_color,
            corner_radius=18,
            height=90
        )
        header.pack(fill="x", padx=20, pady=(20, 12))
        header.pack_propagate(False)

        title_frame = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )
        title_frame.pack(side="left", padx=25, pady=15)

        ctk.CTkLabel(
            title_frame,
            text="AI SKETCH",
            font=("Arial", 25, "bold"),
            text_color=self.text_color
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="Dessine un objet et laisse l'IA le reconnaître",
            font=("Arial", 12),
            text_color=self.secondary_text
        ).pack(anchor="w", pady=(3, 0))

        ctk.CTkLabel(
            header,
            text="●  SYSTÈME PRÊT",
            font=("Arial", 11, "bold"),
            text_color="#A78BFA"
        ).pack(side="right", padx=25)

    # Zone principale
    def create_main_area(self):
        main = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        main.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        main.grid_columnconfigure(0, weight=3)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # Partie dessin
        drawing_card = ctk.CTkFrame(
            main,
            fg_color=self.card_color,
            corner_radius=18
        )
        drawing_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 12)
        )

        drawing_card.grid_rowconfigure(1, weight=1)
        drawing_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            drawing_card,
            text="Zone de dessin",
            font=("Arial", 18, "bold"),
            text_color=self.text_color
        ).grid(row=0, column=0, sticky="w", padx=20, pady=15)

        # Canevas blanc pour dessiner
        self.canvas = Canvas(
            drawing_card,
            bg="#FFFFFF",
            highlightthickness=0,
            cursor="cross"
        )
        self.canvas.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=20,
            pady=(0, 15)
        )

        # Événements de la souris
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        ctk.CTkLabel(
            drawing_card,
            text="Utilise la souris pour dessiner dans la zone blanche.",
            font=("Arial", 11),
            text_color=self.secondary_text
        ).grid(row=2, column=0, sticky="w", padx=20, pady=(0, 15))

        # Partie commandes
        controls = ctk.CTkFrame(
            main,
            fg_color=self.card_color,
            corner_radius=18,
            width=260
        )
        controls.grid(row=0, column=1, sticky="nsew")
        controls.grid_columnconfigure(0, weight=1)
        controls.grid_propagate(False)

        ctk.CTkLabel(
            controls,
            text="COMMANDES",
            font=("Arial", 16, "bold"),
            text_color=self.text_color
        ).pack(anchor="w", padx=18, pady=(20, 15))

        # Réglage du pinceau
        ctk.CTkLabel(
            controls,
            text="Épaisseur du pinceau",
            font=("Arial", 12, "bold"),
            text_color=self.secondary_text
        ).pack(anchor="w", padx=18, pady=(0, 5))

        self.brush_label = ctk.CTkLabel(
            controls,
            text="8 px",
            font=("Arial", 12),
            text_color=self.text_color
        )
        self.brush_label.pack(anchor="w", padx=18)

        self.brush_slider = ctk.CTkSlider(
            controls,
            from_=2,
            to=25,
            number_of_steps=23,
            command=self.change_brush_size,
            progress_color=self.purple,
            button_color=self.purple,
            button_hover_color=self.purple_hover
        )
        self.brush_slider.set(8)
        self.brush_slider.pack(fill="x", padx=18, pady=(8, 20))

        # Boutons d'action
        self.create_button(
            controls,
            "Effacer le dessin",
            self.clear_canvas,
            self.blue_night,
            self.blue_hover
        )

        self.create_button(
            controls,
            "Enregistrer le dessin",
            self.save_drawing,
            self.blue_night,
            self.blue_hover
        )

        self.create_button(
            controls,
            "Reconnaître l'objet",
            self.recognize_drawing,
            self.purple,
            self.purple_hover
        )

        # Carte du résultat
        result_card = ctk.CTkFrame(
            controls,
            fg_color="#101020",
            corner_radius=14
        )
        result_card.pack(fill="x", padx=12, pady=(20, 10))

        ctk.CTkLabel(
            result_card,
            text="RÉSULTAT",
            font=("Arial", 11, "bold"),
            text_color=self.secondary_text
        ).pack(anchor="w", padx=12, pady=(12, 5))

        self.result_label = ctk.CTkLabel(
            result_card,
            text="Aucun résultat",
            font=("Arial", 14, "bold"),
            text_color=self.text_color,
            wraplength=200
        )
        self.result_label.pack(anchor="w", padx=12, pady=(0, 5))

        self.confidence_label = ctk.CTkLabel(
            result_card,
            text="Confiance : --",
            font=("Arial", 11),
            text_color=self.secondary_text
        )
        self.confidence_label.pack(anchor="w", padx=12, pady=(0, 12))

        # Bouton de réinitialisation du résultat
        self.create_button(
            controls,
            "Réinitialiser le résultat",
            self.reset_result,
            "#302044",
            "#482D66"
        )

    # Création d'un bouton arrondi
    def create_button(self, parent, text, command, color, hover):
        button = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            height=44,
            corner_radius=14,
            border_width=0,
            fg_color=color,
            hover_color=hover,
            text_color="#FFFFFF",
            font=("Arial", 12, "bold")
        )
        button.pack(fill="x", padx=15, pady=6)

    # Début du dessin
    def start_drawing(self, event):
        self.last_x = event.x
        self.last_y = event.y
        self.is_drawing = True

        # Affiche un point même si l'utilisateur ne déplace pas la souris
        radius = self.brush_size / 2

        self.canvas.create_oval(
            event.x - radius,
            event.y - radius,
            event.x + radius,
            event.y + radius,
            fill="black",
            outline="black"
        )

        self.image_draw.ellipse(
            [
                event.x - radius,
                event.y - radius,
                event.x + radius,
                event.y + radius
            ],
            fill="black"
        )

    # Tracé à la souris
    def draw(self, event):
        if not self.is_drawing or self.last_x is None:
            return

        self.canvas.create_line(
            self.last_x,
            self.last_y,
            event.x,
            event.y,
            fill="black",
            width=self.brush_size,
            capstyle="round",
            smooth=True
        )

        self.image_draw.line(
            [
                self.last_x,
                self.last_y,
                event.x,
                event.y
            ],
            fill="black",
            width=self.brush_size
        )

        # Arrondit les extrémités des traits
        radius = self.brush_size / 2
        self.image_draw.ellipse(
            [
                event.x - radius,
                event.y - radius,
                event.x + radius,
                event.y + radius
            ],
            fill="black"
        )

        self.last_x = event.x
        self.last_y = event.y

    # Fin du tracé
    def stop_drawing(self, event):
        self.is_drawing = False
        self.last_x = None
        self.last_y = None

    # Modification de l'épaisseur
    def change_brush_size(self, value):
        self.brush_size = int(float(value))
        self.brush_label.configure(text=f"{self.brush_size} px")

    # Effacer le dessin
    def clear_canvas(self):
        self.canvas.delete("all")

        self.image = Image.new("RGB", (600, 450), "white")
        self.image_draw = ImageDraw.Draw(self.image)

        self.reset_result()

    # Enregistrer le dessin
    def save_drawing(self):
        os.makedirs("captures", exist_ok=True)

        file_path = os.path.join("captures", "dessin.png")

        try:
            # Enregistre l'image avec Pillow
            self.image.save(file_path)

            messagebox.showinfo(
                "Enregistrement réussi",
                f"Le dessin a été enregistré ici :\n{os.path.abspath(file_path)}"
            )

        except Exception as error:
            messagebox.showerror(
                "Erreur",
                f"Impossible d'enregistrer le dessin.\n{error}"
            )

    # Reconnaissance du dessin
    def recognize_drawing(self):
        # À connecter au modèle de reconnaissance du projet
        self.result_label.configure(
            text="Modèle non connecté",
            text_color="#C4B5FD"
        )

        self.confidence_label.configure(
            text="Confiance : indisponible"
        )

        messagebox.showinfo(
            "Reconnaissance",
            "L'interface est prête. Il reste à connecter "
            "cette fonction au modèle de reconnaissance."
        )

    # Réinitialiser le résultat affiché
    def reset_result(self):
        self.result_label.configure(
            text="Aucun résultat",
            text_color=self.text_color
        )

        self.confidence_label.configure(
            text="Confiance : --"
        )

# Lance l'application avec le thème sombre.
def launch_app():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Crée la fenêtre principale.
    app = DrawingInterface()

    # Lance la boucle principale de l'interface.
    app.mainloop()


# Vérifie que le fichier est exécuté directement.
if __name__ == "__main__":
    launch_app()