/*
$(window).load(function() {
	$("#toAnnotate").annotateImage({
		editable: true,
		useAjax: false,
		notes: [ { "top": 100,
				   "left": 100,
				   "width": 52,
				   "height": 37,
				   "text": "Small people on the steps",
				   "id": "e69213d0-2eef-40fa-a04b-0ed998f9f1f5",
				   "editable": false },
				 { "top": 134,
				   "left": 179,
				   "width": 68,
				   "height": 74,
				   "text": "National Gallery Dome",
				   "id": "e7f44ac5-bcf2-412d-b440-6dbb8b19ffbe",
				   "editable": true } ]
	});
});
*/
var id = 'asdf'
$(window).load(function() {
				$("#toAnnotate").annotateImage({
					getUrl: "/api/public/tags.json",
					saveUrl: "/tags/save",
					deleteUrl: "delete.html",
					editable: true
				});
			});
