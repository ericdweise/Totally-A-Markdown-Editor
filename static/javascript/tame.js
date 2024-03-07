// TODO: only reload when cache is off
$.fn.loadSiteDir = function() {

	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function() {
		if (xhr.readyState == XMLHttpRequest.DONE) {
			$("#directory").html(xhr.responseText);
		}
	}

	xhr.open( 'GET', '/site-directory', true);
	xhr.send();
};

$.fn.generateTableOfContents = function() {
	var toc_arr = [];

	function build_toc(item) {
		function add_toc_item(header_item, depth) {
			let url = new URL('#' + header_item.id, window.location);
			var link = document.createElement("a");
			link.href = url.toString();
			link.text = header_item.innerText;

			var par = document.createElement("p");
			par.className = 'toc-item';
			par.appendChild(link);

			if (depth > 1) {
				par.style.marginLeft = depth-1 + 'ch';
			}

			document.getElementById('tame-table-of-contents').appendChild(par);
		}

		if (item.localName != null && item.localName.length == 2 && item.localName.charAt(0) == 'h' && item.localName.charAt(1) >= '1' && item.localName.charAt(1) <= '6') {
			add_toc_item(item, item.localName.charAt(1));
		}
	}

	var hdr = document.createElement("h1");
	hdr.textContent = "Contents";
	document.getElementById('tame-table-of-contents').appendChild(hdr);

	const vwr = $('#tame-file-contents');
	vwr[0].childNodes.forEach(build_toc);
};

$.fn.loadMarkdown = function(mdfile) {
    console.log("LOAD MDFILE: " + mdfile);
    // Update history with new note
    let stateObj = { id: "100" };
    window.history.pushState(
        stateObj,
        "",
        "/?note=" + mdfile
    );

	var titleXhr = new XMLHttpRequest();
	titleXhr.onreadystatechange = function() {
		if (titleXhr.readyState == XMLHttpRequest.DONE) {
			$("#site-title").html(titleXhr.responseText);
		}
	}

	titleXhr.open( 'GET', '/get-title?note=' + mdfile, true);
	titleXhr.send();

	var contentXhr = new XMLHttpRequest();
	contentXhr.onreadystatechange = function() {
		if (contentXhr.readyState == XMLHttpRequest.DONE) {
			$("#tame-file-contents").html(contentXhr.responseText);
		}
	}

	contentXhr.open( 'GET', '/load-note?note=' + mdfile, true);
	contentXhr.send();

	contentXhr.onload = $.fn.generateTableOfContents;
};

// Do when new page loads
$(document).ready(function(){
	// Get markdown path from url.search
	const url = new URL(window.location.href);
    console.log("URL Search params: " + url.searchParams);
	var path = url.searchParams.get('note');

    console.log();
	// Default path
	if (path == null) {
        console.log();
		path = 'README.md';
	}

	// Load site map
	$.fn.loadSiteDir();

	// Load Markdown
	$.fn.loadMarkdown(path)

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
				$.fn.loadMarkdown(target);
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
		console.log('Save note target: ' + mdfile);

		var xhr = new XMLHttpRequest();
		xhr.onreadystatechange = function() {
			if (xhr.readyState == XMLHttpRequest.DONE) {
				$('#edit-menu').addClass('hidden');
				$('#editor').addClass('hidden');
				$('#view-menu').removeClass('hidden');
				$('#viewer').removeClass('hidden');
				$.fn.loadMarkdown(mdfile);
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
