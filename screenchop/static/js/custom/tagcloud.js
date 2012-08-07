$(function() {

    //get tag feed
    $.getJSON("/api/public/tagcloud.json", function(data) {

	    //create list for tag links
	    $("<ul>").attr("id", "tagList").appendTo("#tagCloud");
	
	    //create tags
	    $.each(data.tags, function(i, val) {
		
		    //create item
		    var li = $("<li>");
		
		    //create link
		    $("<a>").text(val.tag).attr({title:"See all pages tagged with " + val.tag, href:"/tags/" + val.tag}).appendTo(li);
		
		    //set tag size
		    li.children().css("fontSize", (val.freq / 10 < 1) ? val.freq / 10 + 1 + "em": (val.freq / 10 > 2) ? "2em" : val.freq / 10 + "em");
		
		    //add to list
		    li.appendTo("#tagList");
		
	    });
    });
});

