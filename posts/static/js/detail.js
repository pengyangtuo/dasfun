/**
 * Detail page functions
 */

/**
 * Image post gallery
 */
if($(".df-gallery").length){    // double check the type of post is image
    $(".timg").click(function(e){
        // active the thumbnail image
        $(".timg").removeClass('active');   // reset previous actived thumbnail
        $(this).addClass('active');         // activate this thumbnail image

        // get the url of actived thumbnail
        var img_url = $(this).find("img").attr("src");

        // update big img
        $('#detail-full-img').attr('src', img_url);
    });
}