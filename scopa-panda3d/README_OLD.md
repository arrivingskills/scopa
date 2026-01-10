# Scopa Panda3D Example

Minimal example showing a Python Panda3D frontend communicating with a simple Java backend over TCP. This is a starting point to build a GUI that talks to a Java Scopa engine.

Files:

- Backend: [scopa-panda3d/backend/JavaBackend.java](scopa-panda3d/backend/JavaBackend.java)
- Frontend: [scopa-panda3d/frontend/main.py](scopa-panda3d/frontend/main.py)
- Frontend requirements: [scopa-panda3d/frontend/requirements.txt](scopa-panda3d/frontend/requirements.txt)

Quick start

1) Build and run the Java backend

```bash
cd scopa-panda3d/backend
javac JavaBackend.java
java JavaBackend
```

The backend listens on port 5000 and accepts simple newline-terminated commands like `HELLO`, `START`, `PLAY <something>`, and `QUIT`.

2) Run the Panda3D frontend

Install Panda3D (preferably in a virtualenv):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r ../frontend/requirements.txt
python ../frontend/main.py
```

Usage

- Click `Ping Backend` to send `HELLO` and show the backend response.
- Click `Start` to send `START`.
- Click `Play Random` to send a sample `PLAY CARD1` command.

Notes

- This example is intentionally small and meant to be extended. It doesn't implement Scopa rules or use the existing Java scopa code in the repository.
- For production or richer interactions consider using JSON over TCP, WebSockets, or an HTTP API (e.g., SparkJava) for clearer protocols and easier debugging.
