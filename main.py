#Edited by @mohamed333-ah 

import asyncio
import platform
from game_manager import GameManager
async def main():
    game = GameManager()
    await game.run()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())