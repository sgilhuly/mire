import sys

from app import app, socketio

if __name__ == "__main__":
	if len(sys.argv) > 1:
		port = int(sys.argv[1])
	else:
		port=5000
	socketio.run(app, host="0.0.0.0", port=port)