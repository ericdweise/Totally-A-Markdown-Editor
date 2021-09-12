var mdfile = 'README.md'

$.fn.loadSiteDir = function() {
	var form = new FormData();
	form.append('action', 'site-directory');

	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function() {
		if (xhr.readyState == XMLHttpRequest.DONE) {
			$("#directory").html(xhr.responseText);
		}
	}

	xhr.open( 'post', '/htbin/ajax.py', true);
	xhr.overrideMimeType('text/x-python');
	xhr.send(form);
};

$.fn.loadNote = function(path) {
	mdfile = path;

	var titleForm = new FormData();
	titleForm.append('action', 'get-title');
	titleForm.append('note-path', mdfile);

	var titleXhr = new XMLHttpRequest();
	titleXhr.onreadystatechange = function() {
		if (titleXhr.readyState == XMLHttpRequest.DONE) {
			$("#site-title").html(titleXhr.responseText);
		}
	}

	titleXhr.open( 'post', '/htbin/ajax.py', true);
	titleXhr.overrideMimeType('text/x-python');
	titleXhr.send(titleForm);

	var contentForm = new FormData();
	contentForm.append('action', 'load-note');
	contentForm.append('note-path', mdfile);

	var contentXhr = new XMLHttpRequest();
	contentXhr.onreadystatechange = function() {
		if (contentXhr.readyState == XMLHttpRequest.DONE) {
			$("#viewer").html(contentXhr.responseText);
		}
	}

	contentXhr.open( 'post', '/htbin/ajax.py', true);
	contentXhr.overrideMimeType('text/x-python');
	contentXhr.send(contentForm);
};

$(document).ready(function(){
	// Load site map
	$.fn.loadSiteDir();

	// Load homepage
	$.fn.loadNote(mdfile)

	/*** BUTTONS ***/
	// Edit Button
	$('#edit').click(function() {
		$('#edit-menu').removeClass('hidden');
		$('#editor').removeClass('hidden');
		$('#view-menu').addClass('hidden');
		$('#viewer').addClass('hidden');

		console.log("Editing Markdown: " + mdfile);
		$.get(mdfile, function (data) {
			$("#editor").html(data);
		});
	});

	// Add Note Button
	$('#file').click(function() {
		// Prompt user for new file
		var target = prompt('Name of new note','');
		if (target == null || target =='') {
			alert('ERROR: Invalid target file');
		}

		// Add directory and extension
		if (!target.startsWith('markdown/')) {
			target = 'markdown/' + target;
		}
		if (!target.endsWith('.md')) {
			target = target + '.md';
		}
		console.log('New note target: ' + target);

		// Send AJAX
		var form = new FormData();
		form.append('action', 'new-note');
		form.append('target', target);

		var xhr = new XMLHttpRequest();
		xhr.onreadystatechange = function() {
			if (xhr.readyState == XMLHttpRequest.DONE) {
				$.fn.loadSiteDir();
				$.fn.loadNote(target);
			}
		}

		xhr.open( 'post', '/htbin/ajax.py', true);
		xhr.overrideMimeType('text/x-python');
		xhr.send(form);

		// Reload site-dir
		$.fn.loadSiteDir();
	});

	// Save Button
	$('#save').click(function() {
		// Save editor content
		var form = new FormData();
		var data = $('#editor').text();
		form.append('action', 'save')
		form.append("data", data);
		form.append("target", mdfile);
		console.log('Save note target: ' + mdfile)

		var xhr = new XMLHttpRequest();
		xhr.onreadystatechange = function() {
			if (xhr.readyState == XMLHttpRequest.DONE) {
				$('#edit-menu').addClass('hidden');
				$('#editor').addClass('hidden');
				$('#view-menu').removeClass('hidden');
				$('#viewer').removeClass('hidden');
				$.fn.loadNote(mdfile);
			}
		}

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
