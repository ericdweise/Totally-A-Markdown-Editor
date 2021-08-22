$(document).ready(function(){

	/*** BUTTONS ***/
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

	// Add Note Button
	$('#file').click(function() {
		// Prompt user for new file
		var target = prompt('Enter absolute path to new note','');
		if (target == null || target =='') {
			alert('ERROR: Invalid target file');
		}
		if (!target.endsWith('.md')) {target += '.md';}
		console.log('New note target: ' + target);

		// Send AJAX
		var form = new FormData();
		form.append('action', 'new-note');
		form.append('target', target);
		var xhr = (window.XMLHttpRequest) ? new XMLHttpRequest() : new activeXObject("Microsoft.XMLHTTP");
		xhr.open( 'post', '/htbin/ajax.py', true);
		xhr.overrideMimeType('text/x-python');
		xhr.send(form);
	});

	// Save Button
	$('#save').click(function() {
		// Save editor content
		var target = window.location.pathname.replace(/\.html$/, '.md');
		var form = new FormData();
		var data = $('#editor').text();
		form.append('action', 'save')
		form.append("data", data); // $('#editor').text().replace(/\n/g, '<br>'));
		form.append("target", target);
		console.log('Save note target: ' + target)
		var xhr = (window.XMLHttpRequest) ? new XMLHttpRequest() : new activeXObject("Microsoft.XMLHTTP");
		xhr.open( 'post', '/htbin/ajax.py', true );
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

	/*** IMPLICIT BEHAVIOR ***/
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
})
