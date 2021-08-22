$(document).ready(function(){

	// Edit Button
	$('#edit').click(function() {
		$('#edit-menu').removeClass('hidden');
		$('#editor').removeClass('hidden');
		$('#view-menu').addClass('hidden');
		$('#viewer').addClass('hidden');

		var mdfile = window.location.pathname.replace(/\.html$/, '.md');
		console.log("Loading Markdown: " + mdfile);
		$.get(mdfile, function (data) {
			$("#editor").html(data); // .replace(/\n/g,'&#10;'));
		});
	});

	// var getSelection = function() {
	// 	if(window.getSelection) {
	// 		var sel = window.getSelection();
	// 		if(sel.rangeCount > 0) {
	// 			return sel.getRangeAt(0);
	// 		}
	// 	} else if(document.selection) {
	// 		return document.selection.createRange();
	// 	}
	// 	return null;
	// };

	// listen for <Enter>, insert "\n" instead of default behavior
	document.getElementById('editor').addEventListener('keypress', function(e) {
		if (e.which == 13) { // Listen for <Enter> key
			// Override default behavior of <Enter>
			e.preventDefault();

			var selection = window.getSelection();
			var range = selection.getRangeAt(0);
			var textNode = document.createTextNode('\n');

			// Replace text (if selected) and insert newline character
			range.deleteContents();
			range.collapse(false);
			range.insertNode(textNode);
			range.selectNodeContents(textNode);

			// Create a range storing the new cursor position
			var newRange = document.createRange();
			newRange.setStartAfter(textNode, 0);
			newRange.collapse(false);

			// Clear old range and add new range with cursor position
			selection.removeAllRanges();
			selection.addRange(newRange);
			this.focus();
		}
	});

	// Save Button
	$('#save').click(function() {
		// Save editor content
		var mdfile = window.location.pathname.replace(/\.html$/, '.md');
		var form = new FormData();
		var data = $('#editor').text();
		form.append("data", data); // $('#editor').text().replace(/\n/g, '<br>'));
		form.append("target", mdfile);
		var xhr = (window.XMLHttpRequest) ? new XMLHttpRequest() : new activeXObject("Microsoft.XMLHTTP");
		xhr.open( 'post', '/htbin/save.py', true );
		xhr.overrideMimeType('text/x-python');
		xhr.send(form);
	});

	// Abort Button
	$('#abort').click(function() {
		$('#edit-menu').addClass('hidden');
		$('#editor').addClass('hidden');
		$('#view-menu').removeClass('hidden');
		$('#viewer').removeClass('hidden');
	});
})
