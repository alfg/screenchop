/*
 * Annotations.js
 *
 * Loads iamge tagging jquery.annotate.js with given parameters.
 * getUrl - Call to tags.json file with postfilename variable from template.
 * saveUrl/deleteUrl - Controller calls to save/delete tag.
 * editable - tagable true/false variable passed from template.
 *
 */
 
$(window).load(function() {
				$("#toAnnotate").annotateImage({
					getUrl: "/api/public/tags.json?filename=" + postfilename,
					saveUrl: "/tags/save",
					deleteUrl: "/tags/delete",
					editable: tagable
				});
				$('#image-annotate-add').appendTo('#add-tag-button');
			});
