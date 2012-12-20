/*
 * gallery.js - Custom built js for displaying image jglance grid.
 *
 * Author: Alf
 *
 * Copyright (c) 2012 Screenchop
 * 
 * Licensed under the MIT license:
 *   http://www.opensource.org/licenses/mit-license.php
 *
 * Project home:
 *   http://www.github.com/alfg/screenchop
 */

// Requests json data for gallery images
var photos = (function () {
    var photos = null;
    $.ajax({
        'async': false,
        'global': false,
        'url': '/api/public/images.json?sort=' + sortType + '&user=' +
            user + '&tag=' + tag + '&t=' + time + '&showFollowing=' +
            showFollowing,
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
                </div>' +
                '<div style="font-size: 20px; "> \
                    <a href="' + photo.large + '" class="fancybox" rel="gallery" data-fancybox-type="image"> \
                        <i class="icon-fullscreen pull-right" style="color: white; margin-right: 10px;" title="View Preview"></i> \
                    </a> \
                </div>' +
                '<span class="pull-left" style="clear: left; font-size: 10px;"> \
                <i class="icon-user" style="color: white; margin-right: 5px;"></i> \
                Submitted by <a class="no-underline" href="/u/' + photo.submitter + '"><span class="label label-info">' + photo.submitter + '</span></a> \
                </span>' +
                '<a class="no-underline" href="/tags/' + photo.tags[0] + '"><span class="pull-right label label-success" style="margin-right:10px;">' + photo.tags[0] + '</span></a>' 
                
                ); }
                
    return $('<div />')
                .addClass( 'hovered' )
                .html( 
                
                '<i class="icon-comment pull-left" style="margin-right: 8px; margin-left: 4px;"></i> \
                <span class="pull-left"><h4>' + photo.caption + '</h4></span>' + 
                '<span class="pull-right" style="margin-right: 5px;">' + photo.score + '</span>' +
                '<div style="font-size: 20px; "> \
                    <i class="icon-circle-arrow-up pull-right" style="margin-right: 5px;"></i> \
                </div>' +
                '<div style="font-size: 20px; "> \
                    <a href="' + photo.large + '" class="fancybox" rel="gallery" data-fancybox-type="image"> \
                        <i class="icon-fullscreen pull-right" style="color: white; margin-right: 10px;" title="View Preview"></i> \
                    </a> \
                </div>' +
                '<span class="pull-left" style="clear: left; font-size: 10px;"> \
                <i class="icon-user" style="color: white; margin-right: 5px;"></i> \
                Submitted by <a class="no-underline" href="/u/' + photo.submitter + '"><span class="label label-info">' + photo.submitter + '</span></a> \
                </span>' +
                '<a class="no-underline" href="/tags/' + photo.tags[0] + '"><span class="pull-right label label-success">' + photo.tags[0] + '</span></a>' 
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
        photoClickCallback: null, // Disabled click so link acts as an anchor tag
        enableHoverInfo: true,
        hoverAnimateSpeed: 100,
        hoverInterval: 0,
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
            'url': '/api/public/images.json?sort=' + sortType + '&page=' + page +
                '&user=' + user  + '&tag=' + tag  + '&t=' + time +
                '&showFollowing=' + showFollowing,
            'dataType': "json",
            'success': function (data) {
                photos = data.images;
            }
        });
        page = page + pageInc;
        return photos;
    })(); 
    jg.push(photos);
};


