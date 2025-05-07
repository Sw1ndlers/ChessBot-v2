from PIL import Image
import random
import os
import math
from PIL import Image, ImageDraw
import time

# from modified_chess 

# Parameters

num_images = 1800

# 80% training 20% validation
num_images_data = math.ceil(num_images * 0.8)
num_images_val = num_images - num_images_data

image_size = 800
square_size = image_size // 8  # 100
output_dir = "datasets/chess_yolo_dataset"

piece_classes = {
    "K": 0,
    "Q": 1,
    "R": 2,
    "B": 3,
    "N": 4,
    "P": 5,
    "k": 6,
    "q": 7,
    "r": 8,
    "b": 9,
    "n": 10,
    "p": 11,
    "board": 12,
}

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

piece_styles = chesscom_piece_styles + lichess_piece_styles

# Generate random board
def generate_random_chessboard():
    pieces = list(piece_classes.keys())[:-1]  # exclude 'board'
    chessboard = {f"{file}{rank}": "." for rank in range(1, 9) for file in "abcdefgh"}
    positions = random.sample(sorted(chessboard.keys()), 24)
    for pos in positions:
        chessboard[pos] = random.choice(pieces)
    return chessboard

def random_hex_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


# Get square center in normalized coordinates
def square_to_yolo_coords(file, rank):
    file_idx = ord(file) - ord("a")
    rank_idx = 8 - rank  # rank 8 is top
    x_center = (file_idx + 0.5) * square_size / image_size
    y_center = (rank_idx + 0.5) * square_size / image_size
    width = height = square_size / image_size
    return x_center, y_center, width, height


def render_chessboard(chessboard, pieceSet):
    # board = chess.Board(generate_fen(chessboard))

    lightSquareColor = random_hex_color()
    darkSquareColor = random_hex_color()

    chessboard_image = Image.new("RGB", (image_size, image_size), "white")
    draw = ImageDraw.Draw(chessboard_image)

    for row in range(8):
        for col in range(8):
            top_left = (col * square_size, row * square_size)
            bottom_right = ((col + 1) * square_size, (row + 1) * square_size)
        
            if (row + col) % 2 == 1: # Dark Square
                draw.rectangle([top_left, bottom_right], fill=darkSquareColor)

            else:
                draw.rectangle([top_left, bottom_right], fill=lightSquareColor)

    for pos, piece in chessboard.items():
        if piece == ".":
            continue

        file, rank = pos[0], int(pos[1])

        x = (ord(file) - ord("a")) * square_size
        y = (8 - rank) * square_size  # Invert rank for image coordinates

        piece_color = 'w' if piece.isupper() else 'b'

        piece_image = Image.open(f"pieces/{pieceSet}/{piece_color + piece.lower()}.png").convert("RGBA")
        piece_image = piece_image.resize((square_size, square_size), resample=Image.Resampling.LANCZOS)

        chessboard_image.paste(piece_image, (x, y), piece_image)

    return chessboard_image


def createYoloDataset(output_dir, num_images):
    images_dir = os.path.join(output_dir, "images")
    labels_dir = os.path.join(output_dir, "labels")

    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)

    with open(os.path.join(output_dir, "classes.txt"), "w") as f:
        for piece in piece_classes:
            f.write(f"{piece}\n")

    for i in range(num_images):
        chessboard = generate_random_chessboard()
        drawing = render_chessboard(chessboard, random.choice(piece_styles))

        image_file = os.path.join(images_dir, f"output_{i}.png")
        drawing.save(image_file, "PNG")

        # Generate label file
        label_lines = []

        # Add the board as a whole (class_id 12)
        label_lines.append(f"{piece_classes['board']} 0.5 0.5 1.0 1.0")

        # Add each piece
        for pos, piece in chessboard.items():
            if piece == ".":
                continue
            class_id = piece_classes[piece]
            file, rank = pos[0], int(pos[1])
            x, y, w, h = square_to_yolo_coords(file, rank)
            label_lines.append(f"{class_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}")

        with open(os.path.join(labels_dir, f"output_{i}.txt"), "w") as label_file:
            label_file.write("\n".join(label_lines))


start = time.time()

createYoloDataset(os.path.join(output_dir, "train"), num_images_data)
createYoloDataset(os.path.join(output_dir, "val"), num_images_val)

end = time.time()
print(f"Generated {num_images_data} chess boards in {end - start:.2f} seconds.")

# board = generate_random_chessboard()
# render = render_chessboard(board, 'classic')

# render.show()


# svg = modified_chess.board(board, size=image_size, svgSetName=PIECE_SET_NAMES[random.randrange(0, len(PIECE_SET_NAMES) - 1)], coordinates=False)
# print(svg)

# drawing = svg2rlg(BytesIO(svg.encode("utf-8")))
# renderPM.drawToFile(drawing, "output.png", fmt="PNG")


# print(f"Generated {num_images} images and YOLO labels with board and pieces.")
