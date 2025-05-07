import requests
import os
from multiprocessing import Pool
import git
import shutil
import os
import stat
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from io import BytesIO
import cairosvg

baseUrl = "https://images.chesscomfiles.com/chess-themes/pieces"
outputDir = "./pieces"

colors = ["w", "b"]
pieces = ["k", "q", "r", "b", "n", "p"]

chesscom_piece_styles = [
    "neo",
    "game_room",
    "wood",
    "glass",
    "gothic",
    "classic",
    "metal",
    "bases",
    "neo_wood",
    "icy_sea",
    "club",
    "ocean",
    "newspaper",
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

lichess_piece_styles = [
    "adventurer",
    "adventurer_berry",
    "adventurer_brown",
    "adventurer_grass",
    "alfarishy",
    "alfarishy_berry",
    "alfarishy_blue",
    "alfarishy_pink",
    "alfonso-x",
    "alfonso-x_brown",
    "alfonso-x_grape",
    "alfonso-x_toy",
    "alpha",
    "alpha_ink",
    "alpha_mint",
    "alpha_wood",
    "anarchy",
    "anarchy-plug",
    "anarchy-plug_candy",
    "anarchy-plug_fresh",
    "anarchy-plug_sepia",
    "anarchy_candy",
    "anarchy_fresh",
    "anarchy_halloween",
    "anarchy_sepia",
    "berlin",
    "berlin_blue",
    "berlin_loulou",
    "berlin_maroon",
    "caliente",
    "caliente_blue",
    "caliente_pink",
    "caliente_wood",
    "california",
    "california_brown",
    "california_green",
    "california_red",
    "cardinal",
    "cardinal_blue",
    "cardinal_brown",
    "cardinal_green",
    "cases",
    "cases_cocoa",
    "cases_forest",
    "cases_gray",
    "cburnett",
    "cburnett_blue",
    "cburnett_brown",
    "cburnett_purple",
    "checkers",
    "checkers_cute",
    "checkers_grape",
    "checkers_wood",
    "chess7",
    "chess7_calm",
    "chess7_pink",
    "chess7_yellow",
    "chessnut",
    "chessnut_blue",
    "chessnut_brown",
    "chessnut_burgundy",
    "companion",
    "companion_cyan",
    "companion_eggplant",
    "companion_red",
    "condal",
    "condal_cold",
    "condal_halloween",
    "condal_mustard",
    "condal_warm",
    "dmuysi",
    "dmuysi_cotton",
    "dmuysi_kournikova",
    "dmuysi_marzipan",
    "dubrovny",
    "dubrovny_brown",
    "dubrovny_bw",
    "dubrovny_green",
    "echiquier",
    "echiquier_flesh",
    "echiquier_grape",
    "echiquier_ink",
    "fantasy",
    "fantasy_calm",
    "fantasy_cold",
    "fantasy_warm",
    "fly-or-dream",
    "fly-or-dream_fire",
    "fly-or-dream_magic",
    "fly-or-dream_rainbow",
    "fresca",
    "fresca_camelot",
    "fresca_matisse",
    "fresca_zucchini",
    "gioco",
    "gioco_metal",
    "gioco_purple",
    "gioco_wood",
    "governor",
    "governor_bw",
    "governor_patina",
    "governor_purple",
    "harlequin",
    "harlequin_gold",
    "harlequin_neon",
    "harlequin_peach",
    "horsey",
    "horsey_blue",
    "horsey_pink",
    "horsey_purple",
    "icon54",
    "icon54_brown",
    "icon54_gray",
    "icon54_neon",
    "icpieces",
    "icpieces_blue",
    "icpieces_brown",
    "icpieces_maroon",
    "kingdom",
    "kingdom_blue",
    "kingdom_brown",
    "kingdom_sulu",
    "kosal",
    "kosal_blue",
    "kosal_red",
    "kosal_violet",
    "leipzig",
    "leipzig_berry",
    "leipzig_nature",
    "leipzig_niagara",
    "letters",
    "letters_cold",
    "letters_dim",
    "letters_warm",
    "libra",
    "libra_plum",
    "libra_sea",
    "libra_wood",
    "line",
    "line_berry",
    "line_purple",
    "line_toy",
    "lucena",
    "lucena_blue",
    "lucena_brown",
    "lucena_pink",
    "maestro",
    "maestro_blue",
    "maestro_brown",
    "maestro_pink",
    "magnetic",
    "magnetic_brown",
    "magnetic_lila",
    "magnetic_orange",
    "mark",
    "mark_brown",
    "mark_grape",
    "mark_green",
    "marroquin",
    "marroquin_eggplant",
    "marroquin_rajah",
    "marroquin_toy",
    "maya",
    "maya_brown",
    "maya_cold",
    "maya_warm",
    "mediaeval",
    "mediaeval_brown",
    "mediaeval_green",
    "mediaeval_orange",
    "merida",
    "merida_cyan",
    "merida_ink",
    "merida_traffic",
    "millennia",
    "millennia_blue",
    "millennia_green",
    "millennia_sand",
    "motif",
    "motif_green",
    "motif_maroon",
    "motif_purple",
    "oldstyle",
    "oldstyle_bondi",
    "oldstyle_brown",
    "oldstyle_gossip",
    "pirat",
    "pirat_maroon",
    "pirat_peach",
    "pirat_sea",
    "pirouetti",
    "pirouetti_border",
    "pirouetti_border_coral",
    "pirouetti_border_grass",
    "pirouetti_border_winter",
    "pirouetti_dream",
    "pirouetti_mint",
    "pirouetti_summer",
    "pixel",
    "pixel_juicy",
    "pixel_neon",
    "pixel_spring",
    "qootee",
    "qootee_grape",
    "qootee_pink",
    "qootee_summer",
    "regular",
    "regular_green",
    "regular_ink",
    "regular_purple",
    "reillycraig",
    "reillycraig_dixie",
    "reillycraig_lawn",
    "reillycraig_tamarind",
    "riohacha",
    "riohacha_cute",
    "riohacha_spring",
    "riohacha_winter",
    "saakyan",
    "saakyan_blue",
    "saakyan_coco",
    "saakyan_grape",
    "shapes",
    "shapes_blue",
    "shapes_brown",
    "shapes_cute",
    "smart",
]


def download_image(url, save_path):
    response = requests.get(url, stream=True)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "wb") as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)


def download_chesscom_piece(set, color, piece):
    url = f"{baseUrl}/{set}/150/{color}{piece}.png"
    save_path = f"{outputDir}/{set}/{color}{piece}.png"

    download_image(url, save_path)


def on_rm_error(func, path, exc_info):
    # Change the file to be writable and retry
    os.chmod(path, stat.S_IWRITE)
    func(path)


def download_lichess_pieces():
    repo_url = "https://github.com/sharechess/sharechess.git"
    repo_dir = "temp_sharechess_repo"
    target_subfolder = "public/pieces"
    output_folder = "pieces"

    # Remove existing repo directory if it exists
    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir, onerror=on_rm_error)

    git.Repo.clone_from(repo_url, repo_dir) # Cloning the repo
    source_path = os.path.join(repo_dir, target_subfolder) # temp_sharechess_repo/public/pieces

    # Walk through SVGs and convert to PNGs
    for root, dirs, files in os.walk(source_path):
        for file in files:
            if file.lower().endswith(".svg"):
                rel_dir = os.path.relpath(root, source_path)
                output_dir = os.path.join(output_folder, rel_dir)
                os.makedirs(output_dir, exist_ok=True)

                svg_path = os.path.join(root, file)
                png_path = os.path.join(output_dir, os.path.splitext(file)[0] + ".png")

                cairosvg.svg2png(url=svg_path, write_to=png_path)

    shutil.rmtree(repo_dir, onerror=on_rm_error)


def download_chesscom_pieces():
    pool = Pool(processes=4)
    for set in chesscom_piece_styles:
        for color in colors:
            for piece in pieces:
                pool.apply_async(download_chesscom_piece, args=(set, color, piece))

    pool.close()
    pool.join()


if __name__ == "__main__":
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    download_chesscom_pieces();
    download_lichess_pieces()
