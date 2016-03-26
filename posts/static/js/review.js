/**
 Review index page tab control
 */
$('#review-index-tab a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
})

/**
 Review detail page add new tag
 */
$("#review-detail-add-tag").click(function(){
    // get new tag name
    var new_tag = $("#review-detail-tag-input").val();
    if(new_tag.length <= 0){
        alert("新标签名称不能为空");
        return false;
    }

    // sent ajax call
    var data = {
        'new_tag': new_tag,
        'csrfmiddlewaretoken': getCookie('csrftoken')
    }

    $.ajax({
        url: '/newtag/',
        type: 'POST',
        data: data,
        success: function(data){
            if(data['success'] == 1){
                location.reload();  // refresh page
            }else{
                alert("出错啦");
            }
        },
        error: function(xhr, status, err){
            alert("出大错啦");
            console.log(status+'\n'+err);
        }
    });
});