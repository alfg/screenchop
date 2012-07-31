/* Loads JGlance Photos as a gallery */

// Requests json data for gallery images
var photos = (function () {
    var photos = null;
    $.ajax({
        'async': false,
        'global': false,
        'url': '/api/public/images.json?sort=' + sortType + '&user=' + user,
        'dataType': "json",
        'success': function (data) {
            photos = data.images;
        }
    });
    return photos;
})(); 

// Lightbox gallery. Currently disabled for Fancybox
var inLightBox = function(photo) {
    if ( !photo.caption ) { return; }
    return $('<div />').addClass( 'lightbox-caption' ).html( photo.caption );
};

// HTML overlay when images are hovered
var hovered = function(photo) {
    if ( !photo.caption ) {
    return $('<div />')
                .addClass( 'hovered' )
                .html( 
                
                '<span class="pull-left"></span>' + 
                '<span class="pull-right" style="margin-right: 5px;">' + photo.score + '</span>' +
                '<div style="font-size: 20px; "> \
                    <i class="icon-circle-arrow-up pull-right" style="margin-right: 5px;"></i> \
                    <i class="icon-circle-arrow-down pull-right" style="margin-right: 5px;"></i> \
                </div>' +
                '<div style="font-size: 20px; "> \
                    <a href="' + photo.large + '" class="fancybox" rel="gallery" data-fancybox-type="image"> \
                        <i class="icon-fullscreen pull-right" style="color: white; margin-right: 10px;" title="View Preview"></i> \
                    </a> \
                </div>' 
                
                ); }
                
    return $('<div />')
                .addClass( 'hovered' )
                .html( 
                
                '<i class="icon-comment pull-left" style="margin-right: 8px; margin-left: 4px;"></i> \
                <span class="pull-left">' + photo.caption + '</span>' + 
                '<span class="pull-right" style="margin-right: 5px;">' + photo.score + '</span>' +
                '<div style="font-size: 20px; "> \
                    <i class="icon-circle-arrow-up pull-right" style="margin-right: 5px;"></i> \
                    <i class="icon-circle-arrow-down pull-right" style="margin-right: 5px;"></i> \
                </div>' +
                '<div style="font-size: 20px; "> \
                    <a href="' + photo.large + '" class="fancybox" rel="gallery" data-fancybox-type="image"> \
                        <i class="icon-fullscreen pull-right" style="color: white; margin-right: 10px;" title="View Preview"></i> \
                    </a> \
                </div>' 
                
                );
};

// Actions when image is clicked. Currently goes to single photo page
var click = function(photo) {
    return window.location.href = "/c/" + photo.filename;
};

// Initialize JGlance with settings
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


/* Pagination stuff */

// Auto load imagePaginate when scrolling to bottom of page
$(window).scroll(function(){
    if ($(window).scrollTop() >= $(document).height() - $(window).height() - 10){
        imagePaginate();
        };
});

// Run imagePaginate when loadmore bar is clicked
$('#loadmore').click(function(){
imagePaginate();
});

//Loads paginated images. Amount defined in template.
function imagePaginate(){
    var photos = (function () {
            var photos = null;
            $.ajax({
                'async': false,
                'global': false,
                'url': '/api/public/images.json?sort=' + sortType + '&page=' + page + '&user=' + user,
                'dataType': "json",
                'success': function (data) {
                    photos = data.images;
                }
            });
            page = page + pageInc;
            return photos;
        })(); 
        jg.push( photos );
        };


