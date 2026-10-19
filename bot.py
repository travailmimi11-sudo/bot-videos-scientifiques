
import os
import random
import subprocess
import textwrap
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from moviepy import AudioFileClip, ImageClip

DOSSIER = Path("videos")
DOSSIER.mkdir(exist_ok=True)

FAITS = [
    {
        "titre": "L'espace est silencieux",
        "texte": (
            "Dans l'espace, le son ne se propage pas comme sur Terre. "
            "Il faut un milieu, comme l'air, pour transmettre les vibrations. "
            "C'est pour cela qu'une explosion dans le vide ne s'entendrait pas "
            "comme dans les films."
        ),
        "image": "space stars universe"
    },
    {
        "titre": "Les pieuvres ont trois cœurs",
        "texte": (
            "La pieuvre possède trois cœurs. Deux font circuler le sang "
            "vers les branchies, et le troisième l'envoie vers le reste "
            "du corps. La nature est parfois plus surprenante que la fiction."
        ),
        "image": "octopus underwater ocean"
    },
    {
        "titre": "La lumière du Soleil est ancienne",
        "texte": (
            "La lumière du Soleil met environ huit minutes et vingt secondes "
            "pour atteindre la Terre. Quand tu regardes le Soleil, tu le vois "
            "donc tel qu'il était quelques minutes auparavant."
        ),
        "image": "sun solar surface space"
    }
]


def creer_image(fait, chemin):
    largeur, hauteur = 1080, 1920
    image = Image.new("RGB", (largeur, hauteur), (12, 25, 48))
    dessin = ImageDraw.Draw(image)

    try:
        titre_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 72)
        texte_font = ImageFont.truetype("DejaVuSans.ttf", 43)
    except OSError:
        titre_font = ImageFont.load_default()
        texte_font = ImageFont.load_default()

    dessin.text(
        (70, 300),
        textwrap.fill(fait["titre"], width=22),
        font=titre_font,
        fill="white",
        spacing=18
    )

    dessin.rounded_rectangle(
        (60, 650, 1020, 1450),
        radius=35,
        fill=(25, 48, 78)
    )

    dessin.multiline_text(
        (105, 730),
        textwrap.fill(fait["texte"], width=34),
        font=texte_font,
        fill=(230, 240, 255),
        spacing=24
    )

    dessin.text(
        (70, 1650),
        "SCIENCE ÉTONNANTE",
        font=titre_font,
        fill=(100, 220, 190)
    )

    image.save(chemin)


def creer_video(fait):
    image_path = DOSSIER / "fond.png"
    audio_path = DOSSIER / "voix.mp3"
    video_path = DOSSIER / "video_science.mp4"

    creer_image(fait, image_path)

    gTTS(text=fait["titre"] + ". " + fait["texte"],
         lang="fr").save(str(audio_path))

    audio = AudioFileClip(str(audio_path))
    clip = ImageClip(str(image_path)).with_duration(audio.duration)
    clip = clip.with_audio(audio)

    clip.write_videofile(
        str(video_path),
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    clip.close()
    audio.close()
    print(f"Vidéo créée : {video_path}")


if __name__ == "__main__":
    fait = random.choice(FAITS)
    creer_video(fait)
