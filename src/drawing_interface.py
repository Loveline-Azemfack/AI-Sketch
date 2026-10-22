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

        # Couleurs disponibles pour le pinceau
        self.brush_colors = {
            "Noir": "#000000",
            "Rouge": "#E53935",
            "Bleu": "#1E88E5",
            "Vert": "#43A047",
            "Jaune": "#FDD835",
            "Violet": "#8E24AA",
            "Orange": "#FB8C00",
            "Rose": "#EC407A",
        }

        # Couleur utilisée par défaut
        self.brush_color = self.brush_colors["Noir"]

        # Indique si la gomme est activée
        self.is_eraser = False

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

        # Réglage de l'épaisseur du pinceau
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
        self.brush_slider.pack(fill="x", padx=18, pady=(8, 14))

        # Choix de la couleur du pinceau
        ctk.CTkLabel(
            controls,
            text="Couleur du pinceau",
            font=("Arial", 12, "bold"),
            text_color=self.secondary_text
        ).pack(anchor="w", padx=18, pady=(0, 5))

        self.color_menu = ctk.CTkOptionMenu(
            controls,
            values=list(self.brush_colors.keys()),
            command=self.change_brush_color,
            fg_color=self.blue_night,
            button_color=self.purple,
            button_hover_color=self.purple_hover,
            dropdown_fg_color=self.card_color,
            dropdown_hover_color=self.blue_hover,
            text_color="#FFFFFF",
            font=("Arial", 11)
        )
        self.color_menu.set("Noir")
        self.color_menu.pack(fill="x", padx=15, pady=(0, 10))

        # Bouton pour activer ou désactiver la gomme
        self.eraser_button = self.create_button(
            controls,
            "Gomme : désactivée",
            self.toggle_eraser,
            "#302044",
            "#482D66"
        )

        # Bouton pour effacer tout le dessin
        self.create_button(
            controls,
            "Effacer le dessin",
            self.clear_canvas,
            self.blue_night,
            self.blue_hover
        )

        # Bouton pour enregistrer le dessin
        self.create_button(
            controls,
            "Enregistrer le dessin",
            self.save_drawing,
            self.blue_night,
            self.blue_hover
        )

        # Bouton pour lancer la reconnaissance
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

        # Bouton pour réinitialiser le résultat
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
        button.pack(fill="x", padx=15, pady=5)

        # Retourne le bouton pour pouvoir modifier son apparence.
        return button

    # Change la couleur du pinceau
    def change_brush_color(self, color_name):
        self.brush_color = self.brush_colors.get(
            color_name,
            "#000000"
        )

        # Le choix d'une couleur désactive automatiquement la gomme.
        self.is_eraser = False
        self.update_eraser_button()

    # Active ou désactive la gomme
    def toggle_eraser(self):
        self.is_eraser = not self.is_eraser
        self.update_eraser_button()

    # Actualise le bouton selon l'état de la gomme
    def update_eraser_button(self):
        if self.is_eraser:
            self.eraser_button.configure(
                text="Gomme : activée",
                fg_color="#9F3150",
                hover_color="#B83B60"
            )
        else:
            self.eraser_button.configure(
                text="Gomme : désactivée",
                fg_color="#302044",
                hover_color="#482D66"
            )

    # Retourne la couleur active du pinceau ou de la gomme
    def get_active_color(self):
        if self.is_eraser:
            return "#FFFFFF"

        return self.brush_color

    # Début du dessin
    def start_drawing(self, event):
        self.last_x = event.x
        self.last_y = event.y
        self.is_drawing = True

        # Calcule le rayon du point selon l'épaisseur choisie.
        radius = self.brush_size / 2

        # Récupère la couleur active.
        active_color = self.get_active_color()

        # Affiche un point même si la souris ne bouge pas.
        self.canvas.create_oval(
            event.x - radius,
            event.y - radius,
            event.x + radius,
            event.y + radius,
            fill=active_color,
            outline=active_color
        )

        # Enregistre aussi le point dans l'image destinée à la sauvegarde.
        self.image_draw.ellipse(
            [
                event.x - radius,
                event.y - radius,
                event.x + radius,
                event.y + radius
            ],
            fill=active_color
        )

    # Tracé à la souris
    def draw(self, event):
        # Ne fait rien si le dessin n'a pas commencé.
        if not self.is_drawing or self.last_x is None:
            return

        # Récupère la couleur du pinceau ou de la gomme.
        active_color = self.get_active_color()

        # Dessine le trait sur le canevas de l'interface.
        self.canvas.create_line(
            self.last_x,
            self.last_y,
            event.x,
            event.y,
            fill=active_color,
            width=self.brush_size,
            capstyle="round",
            smooth=True
        )

        # Reproduit le trait dans l'image qui sera enregistrée.
        self.image_draw.line(
            [
                self.last_x,
                self.last_y,
                event.x,
                event.y
            ],
            fill=active_color,
            width=self.brush_size
        )

        # Arrondit l'extrémité du trait dans l'image sauvegardée.
        radius = self.brush_size / 2

        self.image_draw.ellipse(
            [
                event.x - radius,
                event.y - radius,
                event.x + radius,
                event.y + radius
            ],
            fill=active_color
        )

        # Mémorise la nouvelle position de la souris.
        self.last_x = event.x
        self.last_y = event.y

    # Fin du tracé
    def stop_drawing(self, event):
        self.is_drawing = False
        self.last_x = None
        self.last_y = None

    # Modification de l'épaisseur du pinceau
    def change_brush_size(self, value):
        self.brush_size = int(float(value))

        # Affiche la nouvelle épaisseur.
        self.brush_label.configure(
            text=f"{self.brush_size} px"
        )

    # Effacer complètement le dessin
    def clear_canvas(self):
        # Supprime tous les traits affichés.
        self.canvas.delete("all")

        # Crée une nouvelle image blanche.
        self.image = Image.new("RGB", (600, 450), "white")
        self.image_draw = ImageDraw.Draw(self.image)

        # Réinitialise les résultats affichés.
        self.reset_result()

    # Enregistrer le dessin
    def save_drawing(self):
        # Crée le dossier des captures s'il n'existe pas.
        os.makedirs("captures", exist_ok=True)

        # Définit le chemin du fichier de sauvegarde.
        file_path = os.path.join("captures", "dessin.png")

        try:
            # Enregistre l'image avec Pillow.
            self.image.save(file_path)

            # Confirme que l'enregistrement a réussi.
            messagebox.showinfo(
                "Enregistrement réussi",
                f"Le dessin a été enregistré ici :\n"
                f"{os.path.abspath(file_path)}"
            )

        except Exception as error:
            # Affiche un message si l'enregistrement échoue.
            messagebox.showerror(
                "Erreur",
                f"Impossible d'enregistrer le dessin.\n{error}"
            )

    # Reconnaissance du dessin
    def recognize_drawing(self):
        # Cette partie doit encore être reliée au modèle de reconnaissance.
        self.result_label.configure(
            text="Modèle non connecté",
            text_color="#C4B5FD"
        )

        self.confidence_label.configure(
            text="Confiance : indisponible"
        )

        # Informe l'utilisateur que le modèle reste à intégrer.
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


# Lance l'application avec le thème sombre
def launch_app():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Crée la fenêtre principale.
    app = DrawingInterface()

    # Lance la boucle principale de l'interface.
    app.mainloop()


# Lance l'application uniquement si ce fichier est exécuté directement.
if __name__ == "__main__":
    launch_app()

