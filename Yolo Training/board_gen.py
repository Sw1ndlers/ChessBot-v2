from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import random
import os
import math
from PIL import Image, ImageDraw
import time

# from modified_chess

# Parameters

num_images_total = 1000

# 80% training 20% validation
num_images_data = math.ceil(num_images_total * 0.8)
num_images_val = num_images_total - num_images_data

monitor_size = (1980, 1080)
board_size = 800

square_size = board_size // 8  # 100
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

def add_occlusions(image, num_occlusions=5):
    draw = ImageDraw.Draw(image)
    for _ in range(num_occlusions):
        x1 = random.randint(0, image.width)
        y1 = random.randint(0, image.height)
        x2 = x1 + random.randint(30, 100)
        y2 = y1 + random.randint(30, 100)
        color = random_hex_color()
        shape_type = random.choice(["rectangle", "ellipse"])
        if shape_type == "rectangle":
            draw.rectangle([x1, y1, x2, y2], fill=color)
        else:
            draw.ellipse([x1, y1, x2, y2], fill=color)

def generate_image_background(image_size, num_shapes=10, max_offset=100):
    background = Image.new("RGBA", image_size, "white")
    draw = ImageDraw.Draw(background)

    for _ in range(num_shapes):
        shape_type = random.choice(["ellipse", "rectangle", "polygon"])
        shape_color = random_hex_color()

        # Allow shapes to go off-screen by offsetting their coordinates
        x1 = random.randint(-max_offset, image_size[0] + max_offset)
        y1 = random.randint(-max_offset, image_size[1] + max_offset)
        x2 = random.randint(x1, x1 + image_size[0] + 2 * max_offset)
        y2 = random.randint(y1, y1 + image_size[1] + 2 * max_offset)

        if shape_type == "ellipse":
            draw.ellipse([x1, y1, x2, y2], fill=shape_color, outline=None)
        elif shape_type == "rectangle":
            draw.rectangle([x1, y1, x2, y2], fill=shape_color, outline=None)
        elif shape_type == "polygon":
            # Generate random number of points for the polygon
            num_points = random.randint(3, 6)
            points = [
                (
                    random.randint(-max_offset, image_size[0] + max_offset),
                    random.randint(-max_offset, image_size[1] + max_offset),
                )
                for _ in range(num_points)
            ]
            draw.polygon(points, fill=shape_color, outline=None)

    return background


def preload_piece_images(piece_styles, square_size):
    piece_images = {}
    total_loaded = 0

    for style in piece_styles:
        for color in ["w", "b"]:
            for piece in "kqrbnp":

                piece_key = f"{style}_{color}{piece}"
                path = f"pieces/{style}/{color}{piece}.png"

                try:
                    image = Image.open(path).convert("RGBA")
                    image = image.resize(
                        (square_size, square_size), resample=Image.Resampling.LANCZOS
                    )
                    piece_images[piece_key] = image
                    total_loaded += 1

                except FileNotFoundError:
                    print(f"Warning: Missing piece image at {path}")

    return piece_images


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
    x_center = (file_idx + 0.5) * square_size / board_size
    y_center = (rank_idx + 0.5) * square_size / board_size

    width = height = square_size / board_size
    return x_center, y_center, width, height


class ChessDatasetConfig:
    def __init__(self, piece_styles, piece_images, output_dir, background_images, num_images):
        self.piece_styles = piece_styles
        self.piece_images = piece_images
        self.output_dir = output_dir

        self.background_images = background_images
        self.num_images = num_images

        # Derive image and label directories
        self.images_dir = os.path.join(self.output_dir, "images")
        self.labels_dir = os.path.join(self.output_dir, "labels")

        # Create directories if they don't exist
        self.create_directories()

    def create_directories(self):
        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(self.labels_dir, exist_ok=True)


def render_chessboard(chessboard, config):
    lightSquareColor = random_hex_color()
    darkSquareColor = random_hex_color()

    background_image = random.choice(config.background_images).copy()

    chessboard_image = Image.new("RGBA", (board_size, board_size), "white")
    draw = ImageDraw.Draw(chessboard_image)

    piece_style = random.choice(config.piece_styles)

    # Calculate random position to paste the chessboard on the background
    max_x = background_image.width - board_size
    max_y = background_image.height - board_size

    random_x = random.randint(0, max_x)
    random_y = random.randint(0, max_y)

    label_lines = []

    for row in range(8):
        for col in range(8):
            top_left = (col * square_size, row * square_size)
            bottom_right = ((col + 1) * square_size, (row + 1) * square_size)

            if (row + col) % 2 == 1:  # Dark Square
                draw.rectangle([top_left, bottom_right], fill=darkSquareColor)

            else:
                draw.rectangle([top_left, bottom_right], fill=lightSquareColor)

    for pos, piece in chessboard.items():
        if piece == ".":
            continue

        file, rank = pos[0], int(pos[1])

        x = (ord(file) - ord("a")) * square_size
        y = (8 - rank) * square_size  # Invert rank for image coordinates

        piece_color = "w" if piece.isupper() else "b"
        piece_key = f"{piece_style}_{piece_color + piece.lower()}"

        piece_image = config.piece_images.get(piece_key)
        piece_image = piece_image.resize(
            (square_size, square_size), resample=Image.Resampling.LANCZOS
        )

        chessboard_image.paste(piece_image, (x, y), piece_image)

        # Calculate the position of the piece in the full image
        absolute_x = random_x + x + (square_size / 2)
        absolute_y = random_y + y + (square_size / 2)

        absolute_x /= 1980  # Normalize to the 1980x1080 image
        absolute_y /= 1080  # Normalize to the 1980x1080 image

        absolute_width = square_size / 1980
        absolute_height = square_size / 1080

        class_id = piece_classes[piece]

        label_lines.append(
            format_yolo_label(class_id, absolute_x, absolute_y, absolute_width, absolute_height)
        )

    label_lines.append(
        format_yolo_label(
            piece_classes["board"],
            (random_x + (board_size / 2)) / 1980,
            (random_y + (board_size / 2)) / 1080,
            board_size / 1980,
            board_size / 1080,
        )
    )

    # Paste the chessboard on the background
    background_image.paste(chessboard_image, (random_x, random_y), chessboard_image)

    return background_image, label_lines


def create_labeled_image(i, config):
    chessboard = generate_random_chessboard()

    chessboard_render, label_lines = render_chessboard(chessboard, config)
    add_occlusions(chessboard_render, num_occlusions=5)

    image_file = os.path.join(config.images_dir, f"output_{i}.png")
    chessboard_render.save(image_file, "PNG")

    label_file = os.path.join(config.labels_dir, f"output_{i}.txt")

    with open(label_file, "w") as label_f:
        label_f.write("\n".join(label_lines))


def format_yolo_label(class_id, x_center, y_center, width, height):
    return f"{class_id} {x_center:.8f} {y_center:.8f} {width:.8f} {height:.8f}"


def create_yolo_dataset(config):
    with open(os.path.join(config.output_dir, "classes.txt"), "w") as f:
        for piece in piece_classes:
            f.write(f"{piece}\n")

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(create_labeled_image, i, config) for i in range(config.num_images)
        ]
        for f in futures:
            f.result()  # Wait for all to complete (to catch any exceptions)


start = time.time()

print("Preloading piece images...")
piece_images = preload_piece_images(piece_styles, square_size)
print(f"Loaded piece images in {time.time() - start:.2f} seconds.\n")

print("Creating random backgrounds...")
background_images_train = [
    generate_image_background((monitor_size[0], monitor_size[1]), num_shapes=50)
    for _ in range(500)
]
background_images_val = [
    generate_image_background((monitor_size[0], monitor_size[1]), num_shapes=50)
    for _ in range(500)
]
print(f"Random backgrounds created in {time.time() - start:.2f} seconds.")

config = ChessDatasetConfig(
    piece_styles=piece_styles,
    piece_images=piece_images,
    output_dir="datasets/chess_yolo_dataset/train",
    background_images=background_images_train,
    num_images=num_images_data,
)

config_val = ChessDatasetConfig(
    piece_styles=piece_styles,
    piece_images=piece_images,
    output_dir="datasets/chess_yolo_dataset/val",
    background_images=background_images_val,
    num_images=num_images_val,
)

create_yolo_dataset(config)
create_yolo_dataset(config_val)

end = time.time()
print(f"Generated {num_images_total} chess boards in {end - start:.2f} seconds.")
