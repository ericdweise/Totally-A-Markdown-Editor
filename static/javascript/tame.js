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

$.fn.buildTOC = function() {
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

    let targetDiv = document.getElementById('tame-table-of-contents');

    // Clear current ToC
    targetDiv.innerHTML = "";

    // Add new ToC
	var hdr = document.createElement("h1");
	hdr.textContent = "Contents";
	targetDiv.appendChild(hdr);

	const vwr = $('#tame-file-contents');
	vwr[0].childNodes.forEach(build_toc);
};


$.fn.changeNote = function(path) {
    // Update history with new note
    let stateObj = { id: "100" };
    window.history.pushState(
        stateObj,
        "",
        "/view?note=" + path
    );
    $.fn.viewNote();
};

$.fn.viewNote = function() {
	// Get markdown path from url.search
	const url = new URL(window.location.href);
	var path = url.searchParams.get('note');

    // Get note's title
	var titleXhr = new XMLHttpRequest();
	titleXhr.onreadystatechange = function() {
		if (titleXhr.readyState == XMLHttpRequest.DONE) {
			$("#site-title").html(titleXhr.responseText);
		}
	}

	titleXhr.open( 'GET', '/get-title?note=' + path, true);
	titleXhr.send();

    // Get note contents
	var contentXhr = new XMLHttpRequest();
	contentXhr.onreadystatechange = function() {
		if (contentXhr.readyState == XMLHttpRequest.DONE) {
			$("#tame-file-contents").html(contentXhr.responseText);
		}
	}

	contentXhr.open( 'GET', '/load-note?note=' + path, true);
	contentXhr.send();

    // Generate Table of Contents for note
	contentXhr.onload = $.fn.buildTOC;
};

$.fn.editNote = function() {
    // TODO: Add this to "on-click" of the "Edit Note" button
    alert('Edit Note button click...');
};

$.fn.newNote = function() {
    // TODO: Add this to "on-click" of the "New Note" button

    // Prompt user for new file
    var target = prompt('Name of new note','');
    console.log('New note target: ' + target);

    // Send AJAX, wait for response
    // TODO: Write the "new-note" POST endpoint
    var form = new FormData();
    form.append('target', target);

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            // Reload site directory so it includes new file
            $.fn.loadSiteDir();

            // View new note (will be empty)
            $.fn.viewNote();

            // Open the editor
            $.fn.editNote();
        } else {
            alert("Failed to create new note at " + target);
        }
    }

    // TODO: is this right?
    xhr.open('post', '/new-note', true);
    xhr.send(form);
};

$.fn.saveNote = function() {
    // TODO: this...
    alert('Save Note button click...');
};

$.fn.abortEdit = function() {
    // TODO: this...
    alert('Abort Edit button click...');
};

// Do when new page loads
$(document).ready(function() {
    if (document.location.pathname == '/view') {
        $.fn.loadSiteDir();
        $.fn.viewNote();
    } else if (document.location.pathname == '/edit') {
        $.fn.prepareEditNotePage();
    }
})
