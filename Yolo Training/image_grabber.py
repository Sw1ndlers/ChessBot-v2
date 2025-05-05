import requests
import os
from multiprocessing import Pool

baseUrl = "https://images.chesscomfiles.com/chess-themes/pieces"
outputDir = "./pieces"

colors = ["w", "b"]
pieces = ["k", "q", "r", "b", "n", "p"]

piece_styles = [
    "neo",
    "gameroom",
    "wood",
    "glass",
    "gothic",
    "classic",
    "metal",
    "bases",
    "neo_wood",
    "icysea",
    "club",
    "ocean",
    "newspaper",
    "blindfold",
    "space",
    "cases",
    "condal",
    "3d_chesskid",
    "8_bit",
    "marble",
    "book",
    "alpha",
    "bubblegum",
    "dash",
    "graffiti",
    "light",
    "lolz",
    "luca",
    "maya",
    "modern",
    "nature",
    "neon",
    "sky",
    "tigers",
    "tournament",
    "vintage",
    "3d_wood",
    "3d_staunton",
    "3d_plastic",
]

def download_image(url, save_path):
    response = requests.get(url, stream=True)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "wb") as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)

def download_piece(set, color, piece, style):
    url = f"{baseUrl}/{set}/150/{color}{piece}.png"
    save_path = f"{outputDir}/{set}/{color}{piece}.png"

    download_image(url, save_path)

# Download all

# for set in piece_styles:
#     for color in colors:
#         for piece in pieces:
#             download_piece(set, color, piece, set)

# Multiprocessing

if __name__ == "__main__":
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    pool = Pool(processes=4)
    for set in piece_styles:
        for color in colors:
            for piece in pieces:
                pool.apply_async(download_piece, args=(set, color, piece, set))

    pool.close()
    pool.join()
