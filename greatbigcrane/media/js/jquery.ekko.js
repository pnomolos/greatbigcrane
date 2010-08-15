/**
* ekko - jQuery Plugin
*
* Version - 0.1.0
*
* Copyright (c) 2009 Terry M. Schmidt
*
* Dual licensed under the MIT and GPL licenses:
*   http://www.opensource.org/licenses/mit-license.php
*   http://www.gnu.org/licenses/gpl.html
*
* Based on the work done by John McCollum and the jQuery PeriodicalUpdater plugin.
* 
**/

(function(jQuery) {
	jQuery.fn.ekko = function (options, callback) {

		return this.each(function () {
			
			var elem	= this;
			var $elem	= jQuery(this);
			
			// Initial Settings
			elem.settings = jQuery.extend({
	            url			: '',
	            method		: 'get',
	            sendData	: '',
	            minTimeout	: 1000, // Default 1 second
	            maxTimeout	: ((1000 * 60) * 60), // Default 1 hour
	            multiplier	: 2,
	            type		: 'text'
	        }, options);
			
			elem.settings.ajaxMethod = /post/i.test(elem.settings.method) ? jQuery.post : jQuery.get;
			elem.settings.prevContent = '';
			elem.settings.originalMinTimeout = elem.settings.minTimeout;
			
			start();
			
			function start() {
				elem.settings.ajaxMethod(elem.settings.url, elem.settings.sendData, function (data) {
					if (elem.settings.prevContent != data) {
						elem.settings.prevContent = data;
						if (callback) {
							$.proxy(callback, elem)(data)
						}
						// reset minTimeout
						elem.settings.minTimeout = elem.settings.originalMinTimeout;
						elem.settings.periodicalUpdater = setTimeout(start, elem.settings.minTimeout);
					} else {
						if (elem.settings.minTimeout < elem.settings.maxTimeout) {
							elem.settings.minTimeout = elem.settings.minTimeout * elem.settings.multiplier
						}
						
						if (elem.settings.minTimeout > elem.settings.maxTimeout) {
							elem.settings.minTimeout = elem.settings.maxTimeout
						}
						
						elem.settings.periodicalUpdater = setTimeout(start, elem.settings.minTimeout);
					}
				}, elem.settings.type);
			} // start()
		});
		
	}; // jQuery.fn.ekko()
	
	jQuery.fn.ekkoStop = function () {
		return this.each(function () {
			var elem = this;
			clearTimeout(elem.settings.periodicalUpdater)
		});
	} // jQuery.fn.ekkoStop()
})(jQuery);