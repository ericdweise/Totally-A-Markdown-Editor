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

			document.getElementById('note-toc').appendChild(par);
		}

		if (item.localName != null && item.localName.length == 2 && item.localName.charAt(0) == 'h' && item.localName.charAt(1) >= '1' && item.localName.charAt(1) <= '6') {
			add_toc_item(item, item.localName.charAt(1));
		}
	}

    let targetDiv = document.getElementById('note-toc');

    // Clear current ToC
    targetDiv.innerHTML = "";

    // Add new ToC
	var hdr = document.createElement("p");
    hdr.classList.add("sec-title");
	hdr.textContent = "Contents";
	targetDiv.appendChild(hdr);

	const vwr = $('#note-rendered');
	vwr[0].childNodes.forEach(build_toc);
};


$.fn.editNote = function() {
    let url = new URL(window.location.href);
    url.pathname = 'edit';
    window.location.replace(url.href);
};

$.fn.getRawNote = function() {
	const url = new URL(window.location.href);
	var path = url.searchParams.get('note');

    // Get raw note contents
	var contentXhr = new XMLHttpRequest();
	contentXhr.onreadystatechange = function() {
		if (contentXhr.readyState == XMLHttpRequest.DONE) {
			$("#editor").html(contentXhr.responseText);
		}
	}

	contentXhr.open( 'GET', '/load-raw?note=' + path, true);
	contentXhr.send();
};

$.fn.newNote = function() {
    // TODO: Add this to "on-click" of the "New Note" button

    // Prompt user for new file
    var note = prompt('Name of new note','');
    console.log('New note: ' + note);

    // Send AJAX, wait for response
    // TODO: Write the "new-note" POST endpoint
    var form = new FormData();
    form.append('note', note);
    form.append('field2', 'field2_data');

    var xhr = new XMLHttpRequest();
    xhr.onloadend = function() {
        if (xhr.status == 201) {
            // Open new note in Edit mode
            window.location.replace("/edit?note=" + note);
        } else {
            alert("Failed to create new note at " + note);
        }
    }

    // TODO: is this right?
    xhr.open('post', '/new-note', true);
    xhr.send(form);
};

$.fn.saveNote = function() {
	const url = new URL(window.location.href);
	var path = url.searchParams.get('note');

    let raw_data = document.getElementById("editor").value;

    var form = new FormData();
    form.append('note', path);
    form.append('raw', raw_data);

	var xhr = new XMLHttpRequest();
	xhr.onloadend = function() {
		if (xhr.status == 201) {
            let url = new URL(window.location.href);
            url.pathname = 'view';
            window.location.replace(url.href);
		} else {
            alert("Save was unsuccessful.");
        }
	}

    xhr.open('post', '/save', true);
    xhr.send(form);
};

$.fn.abortEdit = function() {
    let url = new URL(window.location.href);
    url.pathname = 'view';
    window.location.replace(url.href);
};

// Do when new page loads
$(document).ready(function() {
    if (document.location.pathname == '/view') {
        $.fn.loadSiteDir();
        $.fn.buildTOC();
    } else if (document.location.pathname == '/edit') {
        $.fn.getRawNote();
    }
})
