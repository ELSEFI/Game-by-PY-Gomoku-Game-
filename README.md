# 🧠 Gomoku AI Game (15x15 Board)

A Python-based Gomoku game with an AI opponent using the Minimax algorithm with Alpha-Beta pruning. Built with Pygame for a clean graphical interface and interactive gameplay.

---

## 🎮 Game Modes

- 🆚 Human vs Human
- 🤖 Human vs AI (Minimax algorithm with evaluation heuristics)

---

## 🧠 AI Features

- **Minimax Algorithm** with Alpha-Beta pruning.
- **Dynamic depth adjustment** based on game progress.
- **Move ordering** to prioritize central and strategic cells.
- Evaluation function that considers:
  - Threat levels
  - Open-ended sequences
  - Board positioning

---

## 📁 Project Structure

| File              | Description                                       |
| ----------------- | ------------------------------------------------- |
| `main.py`         | Entry point – runs the game loop using asyncio    |
| `gomoku_board.py` | Core logic of the board + AI player class         |
| `game_manager.py` | Handles game flow, turns, and AI behavior         |
| `game_ui.py`      | Responsible for drawing the board and UI elements |

---

## 🚀 How to Run

Make sure you have Python 3 installed, then run:

```bash
pip install pygame
python main.py

---

## 👨‍💻 Team Members & Contributions

| Name            | GitHub         | Contribution                     |
|--------------   |----------------|----------------------------------|
| Mohamed Elsayed | @ELSEFI        | `gomoku_board.py,Project_Report` |
| Zeyad Ibrahim   | @ziad-ibrahim1 | `gomoku_board.py`                |
| Amr Elsayed     | @amrelsaid4    | `game_manager.py`                |
| Kareem hany     | @kareemhany111 | `game_manager.py`                |
| Mohamed Selsem  | @mohamed123-ui | `game_ui,Main.py,README.md`      |
| Mohamed Ahmed   | @mohamed333-ah | `game_manager.py`                |

---

## 📷 Screenshots

![Game Board](screenshots/Mainscreen.png.png)
![Game Board](screenshots/Gui.png.png.png)
![Game Board](screenshots/Ph2.png.png.png)

---

## ❤️ Made with Python + Pygame
```
