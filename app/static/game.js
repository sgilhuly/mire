$(function() {
	var messageBox = $("#messageBox");
	var textInput = $("#textInput");

	messageBox.val("");

	textInput.keypress(function(e) {
		// Enter pressed?
		if(e.which == 10 || e.which == 13) {
			socket.send(textInput.val());
			textInput.val("");
		}
	});

	function writeMessage(message) {
		if(messageBox.val()) {
			messageBox.val(messageBox.val() + "\n\n" + message);
		} else {
			messageBox.val(message);
		}
		messageBox.scrollTop(messageBox[0].scrollHeight);
	}

	var socket = io.connect("http://" + document.domain + ":" + location.port);

	socket.on("disconnect", function() {
		socket.close();
		writeMessage("\nYou were disconnected...");
	});

	socket.on("message", writeMessage);
});