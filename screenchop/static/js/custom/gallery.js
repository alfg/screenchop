/* Loads JGlance Photos as a gallery */

// Requests json data for gallery images
var photos = (function () {
    var photos = null;
    $.ajax({
        'async': false,
        'global': false,
        'url': 'api/public/images.json',
        'dataType': "json",
        'success': function (data) {
            photos = data.images;
        }
    });
    return photos;
})(); 

var inLightBox = function(photo) {
    if ( !photo.caption ) { return; }
    return $('<div />').addClass( 'lightbox-caption' ).html( photo.caption );
};

var hovered = function(photo) {
    return $('<div />')
                .addClass( 'hovered' )
                .html( 'Filename: ' + photo.filename + ' | Dimensions: ' + photo.width + ' x ' + photo.height );
};

var click = function(photo) {
    return window.location.href = "/chop/" + photo.filename;
};

var jg = new JGlance({
        container: $('#results'),
        maxPerRow: maxPerRow,
        enableLightBox: false,
        lightBoxInfoCallback: inLightBox,
        photoClickCallback: click,
        enableHoverInfo: true,
        hoverInfoCallback: hovered,
        photoErrorCallback: function (photo, img) {
            img.attr( 'src', 'http://placehold.it/350x150' ).addClass( 'broken-image' );
        }
    });
// we pass the photos via 'push' method
jg.push( photos );

