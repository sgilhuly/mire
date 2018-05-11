from flask import render_template, request

from app import socketio

# @socketio.on('message')
# def handle_message(message):
# 	print('broadcasting message: ' + message)
# 	socketio.send(message, broadcast=True)

# @socketio.on('json')
# def handle_json(json):
# 	print('received json: ' + str(json))

# @socketio.on('my event')
# def handle_my_custom_event(json):
# 	print('received custom event json: ' + str(json))

@socketio.on('connect')
def handle_connect():
	socketio.send('A cloaked figure emerges from the mist.\nHe beckons you closer, whispering:\n"Welcome to MIRE, traveller. What is your name?"')

@socketio.on('message')
def handle_message(message):
	socketio.send(message)
