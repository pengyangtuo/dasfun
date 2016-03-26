/**
 * Upload image during the editing of qeditor
 */
/*
    Global setups
 */
var imgUploader = imgUploader || {};

/*
    create a invisible form that contains the file input tag

    id - id of the form
 */
imgUploader.init = function(){
    // create input file tag
    imgUploader.fileInput = $('<input>')
        .attr({
            type: 'file',
            id: 'img-upload-input',
        });

    // create form tag
    imgUploader.imgForm = $('<form>')
        .attr({
            enctype: 'multipart/form-data',
            id: 'img-upload-form'
        })
        .css({
            'position':'absolute',
            'left':-999
        })
        .append(imgUploader.fileInput);

    $('body').append(imgUploader.imgForm);

    // event listener
    imgUploader.fileInput.change(function(){
        imgUploader.imgForm.submit();
    });

    imgUploader.imgForm.submit(function(e){
        e.preventDefault();  // stop normal submit

        var formData = new FormData(); // get form dataimg
        var imgFile = $('#img-upload-input').get(0).files[0];
        formData.append('article-img', imgFile);
        var csrftoken = getCookie('csrftoken');
        formData.append('csrfmiddlewaretoken', csrftoken);

        // send ajax request
        $.ajax({
            url: '/upload_img/',
            type: 'POST',
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            success: function(data){
                if(data['success'] == 1){
                    console.log('insert img: ' +data['url']);
                    QEditor.action(imgUploader.el, imgUploader.action, data['url']);
                }else{
                    console.log('error\n' + JSON.stringify(data));
                }
            },
            error: function(xhr, status, err){
                console.log(status+'\n'+err);
            }
        });
    });
}

/*
    open the file Browser
 */
imgUploader.openFileBrowser = function(el, action){
    // set element and action for further use
    imgUploader.el = el;
    imgUploader.action = action;

    // open file browser
    imgUploader.fileInput.trigger('click');
}

/*
    Start imgUploader
 */
imgUploader.init();