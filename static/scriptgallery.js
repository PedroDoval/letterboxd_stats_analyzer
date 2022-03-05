
var folder = "https://html5-templates.com/images/";	//change the image folder
/*
Name the image files 1.jpg, 2.jpg.... or adjust the script accordingly
*/
var counter = 3;
var loadingol = 0;
var kepid = "Kep;"
function preload(arrayOfImages) {
    $(arrayOfImages).each(function(){
        $('<img/>')[0].src = this;
    });
}

$(window).on("scroll", function() {
	var scrollHeight = $(document).height();
	var scrollPosition = $(window).height() + $(window).scrollTop();
	if ((scrollHeight - scrollPosition) / scrollHeight === 0) {		// elerte az aljat
		loadImage(1);	
	}
});


 /*Scroll to top when arrow up clicked END*/
