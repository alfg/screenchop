/*
 * Annotations functions
 * */

$(window).load(function() {
    $("#toAnnotate").annotateImage({
        getUrl: "/api/public/tags.json?filename=" + postfilename,
        saveUrl: "/tags/save",
        deleteUrl: "/tags/delete",
        editable: tagable
    });
    $('#image-annotate-add').appendTo('#add-tag-button');
});
