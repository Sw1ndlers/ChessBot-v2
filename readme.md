# Chess Bot v2

### A recreation of my old [Chess Bot](https://github.com/Sw1ndlers/ChessBot)


## The project is split into 2 parts:

### Chess Bot Display  
A wip user interface for the chess bot.  
Planned to be implemented in **rust** using the native windows api.  
Running the model trained in `Chess Bot Training`

### Chess Bot Training
A python project that scrapes chess pieces.  
Generates a chess board dataset.  
Trains a YOLOv8 model to detect the board.  
Sends the model to be used in `Chess Bot Display`.  


#### Current Model Results:

![Result 1](https://github.com/user-attachments/assets/802149c9-bb6a-405f-b0b9-028ec510afc9)
![Result 2](https://github.com/user-attachments/assets/a846574c-3cf1-41e5-a377-92162ace7cda)
![Result 3](https://github.com/user-attachments/assets/8b41357f-ddef-4d85-9f4d-a4d6fb88a717)
