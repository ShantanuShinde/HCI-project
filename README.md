# Content Moderation Tester
## Running Backend Server
1. Install the latest version of python.
2. Install all the required dependencies from the **requirements.txt** using the command:
> pip install -r requirements.txt
3. Install and run **Docker Desktop**.
4. Create and start the docker container with ollama server running the command in the **backend** directory:
> docker-compose up -d
5. Pull the **llama3.2** model by running the following command:
> docker exec ollama ollama pull llama3.2:3b
6. Start the backend server by running the command:
> python server.py

## Running Frontend
1. Install Node.js.
2. Run following command in the **frontend** directory:
> npm install
3. Start the frontend by running the command:
> npm run dev
