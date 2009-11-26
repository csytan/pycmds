// License: MIT (MIT-LICENSE.txt)
jQuery.fn.pyCommandLine = function(settings) {
	var inputDiv = $(this);
	var input = $('<input id="hidden_input" type="text"/>')
	.css({position: 'fixed', top: '0px', left: '-500px'})
	.appendTo(document.body)[0];
	var caret = '<b id="caret">_</b>';
	var suggestDiv = $('<div id="suggestions"></div>').appendTo(document.body).hide();
	var suggestCache = {};
	var suggestTimer;
	var inputHistory = [];
	
	var KEY = {
		UP: 38, DOWN: 40, LEFT: 37, RIGHT: 39, DEL: 46, TAB: 9,
		RETURN: 13,	ESC: 27, PAGEUP: 33, PAGEDOWN: 34, BACKSPACE: 8
	};	
	
	settings = $.extend({
		suggestUrl: '/commands?action=suggest',
		dispatchUrl: '/commands?action=dispatch',
		delay: 200,
		cache: true
	}, settings);
	
	function syncText() {
		var text = input.value;
		var caretPosition = input.selectionEnd;
		var startText = text.substring(0, caretPosition);
		var endText = text.substring(caretPosition);
		
		inputDiv.html(startText + caret + endText);
		
		if (text !== inputHistory[inputHistory.length - 1]) {
			inputHistory.push(text);
		}
		if (endText) inputHistory = [];
	}

	function showSuggestions() {
		var suggestions = suggestCache[input.value];
		if (!suggestions || !suggestions.length) return false;
		
		var html = '';
		for (var i = 0, suggestion; suggestion = suggestions[i]; i++) {
			html += '<div class="suggestion">' + suggestion + '</div>';
		}
		suggestDiv.html(html);
		
		// Position suggestions after the caret, unless they are too large
		var docWidth = $(document).width();
		var suggDivWidth = suggestDiv.width();
		var left = $("#caret").offset().left;
		var space =  docWidth - left;
		
		if (space < suggDivWidth) {
			left = docWidth - suggDivWidth;
		}

		suggestDiv.css({
			left: left,
			bottom: $("#footer").outerHeight()
		});
		
		// Add click events to suggestions
		suggestDiv.children(".suggestion")
		.click(function(event) {
			$(this).removeClass("selected");
			autoComplete($(this).text());
			$(input).focus();
			return false;
		})
		.eq(0).addClass("selected");
		
		suggestDiv.show();
		return true;
	}
	
	function suggest() {
		if (!settings.cache) suggestCache = [];
		if (showSuggestions()) return;
		suggestDiv.hide();
		var prefix = input.value;
		
		window.clearTimeout(suggestTimer);
		suggestTimer = window.setTimeout(function () {
			$.getJSON(settings.suggestUrl, {'prefix': prefix},
				function(data) {
					var suggestions = [];
					for (var i = 0, suggestion; suggestion = data[i]; i++) {
						suggestion = suggestion.substring(prefix.length);
						if (suggestion)	suggestions.push(suggestion);
					}
					suggestCache[prefix] = suggestions;
					showSuggestions();
				}
			);
		}, settings.delay);
	}
	
	function autoComplete(suggestion) {
		for (var i = 0, c; c = suggestion.charAt(i); i++) {
			input.value += c;
			if (c === '[') break;
		}
		syncText();
		suggest();
	}	
	
	function dispatch(cmd) {
		var content = $('<div class="content"><h2><a href="#' + cmd + '">' + cmd + '</a></h2></div>');
		$(document.body).append(content);
		
		$.get(settings.dispatchUrl, {'cmd': cmd}, 
		function(data) {
			content[0].innerHTML += data;
			content[0].scrollIntoView();
			location.hash = cmd;
		});
	}
	
	function keyReturn() {
		var selected = suggestDiv.children(".selected:first");
		if (selected.length && suggestDiv.is(":visible")) {
			selected.removeClass("selected");
			autoComplete(selected.text());
		} else if (input.value) {
			dispatch(input.value);
			inputHistory = [];
			input.value = '';
			syncText();
			suggestDiv.hide();
		}
	}
	
	function scrollSuggestion(selected) {
		// Safari can't use scrollIntoView because it scrolls the whole window and not just the suggestions box
		var offset = 0;
		selected.prevAll().each(function() {
			offset += $(this).outerHeight();
		});
		suggestDiv.scrollTop(offset);
	}
	
	function keyUp() {
		var selected = suggestDiv.children(".selected");
		if (selected.length) {
			selected = selected.removeClass("selected")
			.prev().addClass("selected");
		} else {
			selected = suggestDiv.children(".suggestion:last")
			.addClass("selected");
		}
		scrollSuggestion(selected);
	}
	
	function keyDown() {
		var selected = suggestDiv.children(".selected");
		if (selected.length) {
			selected = selected.removeClass("selected")
			.next().addClass("selected");
		} else {
			selected = suggestDiv.children(".suggestion:first")
			.addClass("selected");
		}
		scrollSuggestion(selected);
	}
	
	
	/*--- Events  ---*/
	$('#footer').click(function() {
		$(input).focus();
		$("#caret").show();
		syncText();
		suggest();
		return false;
	});
	
	// Can't use $(input).blur(fn())  because it fires before  .suggestion's click or mousedown events in IE
	$(document).click(function() {
		$(input).blur();
		$("#caret").hide();
		suggestDiv.hide();
	});
	
	$(input)
	.bind(($.browser.opera ? "keypress" : "keydown"), function(event) {
		// Opera 9: keypress works. keydown & keyup don't
		// Safari 3: keydown works, keypress doesn't
		switch(event.keyCode) {
			case KEY.RETURN:
				keyReturn();
				return;
			case KEY.UP:
				keyUp();
				return false;
			case KEY.DOWN:
				keyDown();
				return false;
			case KEY.BACKSPACE:
				inputHistory.pop();
				var prevText = inputHistory.pop();
				
				if (prevText) {
					input.value = prevText;
					syncText();
					showSuggestions();
					return false;
				}				
		}
	})
	.keyup(function(event) {
		switch(event.keyCode) {
			case KEY.RETURN:
				return;
			case KEY.UP:
				return false;
			case KEY.DOWN:
				return false;
		}
		syncText();
		suggest();
	})
	.focus();
	
	$(document).ready(function() {
		if (location.hash) {
			var hash = location.hash.substring(1);
			dispatch(decodeURIComponent(hash));
		}
	});	
	
	
	/*--- Alerts  ---*/
	$('<div class="alert">Loading...</div>')
	.appendTo(document.body)
	.ajaxStart(function() {
		$(this).fadeIn("slow");
	})
	.ajaxStop(function() {
		$(this).fadeOut("slow");
	});
	
	$('<div class="alert">Problem Connecting</div>')
	.appendTo(document.body)
	.ajaxError(function(event, request, settings) {
		if (request.status !== 500)
			$(this).fadeIn("slow").fadeOut(5000);
	});
	
	$('<div class="alert">Server error</div>')
	.appendTo(document.body)
	.ajaxError(function(event, request, settings) {
		if (request.status === 500)
			$(this).fadeIn("slow").fadeOut(5000);
	});
	
	$('<div class="alert">Server too busy, please try again later</div>')
	.appendTo(document.body)
	.ajaxError(function(event, request, settings) {
		if (request.status === 403)
			$(this).fadeIn("slow").fadeOut(5000);
	});
	
	
	/*--- Browser Hacks --- */
	if ($.browser.opera) {
		// Opera tries to scroll to the offscreen hidden input when typing in it
		// this is a workaround
		$(input).css({
			left: 0,
			width: 0,
			opacity: 0
		});
	} else if ($.browser.msie) {
		// Wraps syncText to set selectionEnd
		var oldSyncText = syncText;
		var syncText = function() {
			// Code from: http://www.bazon.net/mishoo/articles.epl?art_id=1292
			var range = document.selection.createRange();
			var isCollapsed = range.compareEndPoints("StartToEnd", range) == 0;
			if (!isCollapsed)
				range.collapse(false);
			var b = range.getBookmark();
			input.selectionEnd = b.charCodeAt(2) - 2;
			oldSyncText();
		}
		
		// IE puts the caret at the start of the input when refocused,  
		// instead of remembering the previous caret position
		// this puts it at the end of the input
		$(input).focus(function() {
			var position = input.value.length;
			var range = input.createTextRange();
			range.collapse(true);
			range.moveStart("character", position);
			range.moveEnd("character", position);
			range.select();
		});
	}
};

