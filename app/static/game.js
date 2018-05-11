$(function() {
	var messageBox = $("#messageBox");
	var textInput = $("#textInput");

	messageBox.val("");

	textInput.keypress(function(e) {
		// Enter pressed?
		if(e.which == 10 || e.which == 13) {
			socket.send(name + ": " + textInput.val());
			textInput.val("");
		}
	});

	var socket = io.connect("http://" + document.domain + ":" + location.port);

	socket.on("message", function(message) {
		if(messageBox.val()) {
			messageBox.val(messageBox.val() + "\n" + message);
		} else {
			messageBox.val(message);
		}
		messageBox.scrollTop(messageBox[0].scrollHeight);
	});
});