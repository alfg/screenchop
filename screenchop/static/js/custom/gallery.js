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

var jg = new JGlance({
        container: $('#results'),
        maxPerRow: 4,
        photoErrorCallback: function (photo, img) {
            img.attr( 'src', 'http://placehold.it/350x150' ).addClass( 'broken-image' );
        }
    });
// we pass the photos via 'push' method
jg.push( photos );

