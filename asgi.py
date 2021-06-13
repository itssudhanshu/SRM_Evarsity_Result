import uvicorn
from main.app import main

if __name__ == '__main__':
    uvicorn.run(main.app)