# Chess Bot v2

## Coding Process:

### 5/5

- Trained on yolo base model
- Generated chess board using pillow for image manipulation:
  - Scraped chess.com for piece images
- Tried 100 epochs with 1800 samples got bad results.
- Figured it was due to not enough epoches / not enough training data

### 5/6

- Implement lichess piece sets and then trained again:
  - 10k samples with 250 epochs
- Got better results but still had mismatches, assumed it was due to pieces on the board overlapping with the bounding box of the piece:
  - Tried removing the coordinates and had good results
  - Was not satisified with results, attempted to make instance segmentation

## Pieces Style Sources

`piece_grabber.py` Sources From:

- Chess.com: <https://www.chess.com/>  (Scraped)
- Lichess: <https://lichess.org/> (sourced from [Sharechess](https://github.com/sharechess/sharechess/tree/main/public/pieces))

## Image Gen Dependencies

Windows:  
<https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer>
<https://github.com/ultralytics/JSON2YOLO>

Linux:  

```bash
sudo apt install libcairo2 libcairo2-dev
```

Python Dependencies:  

```psh
pip insgall svglib chess 
```

<!-- https://docs.ultralytics.com/datasets/segment/coco8-seg/#sample-images-and-annotations -->