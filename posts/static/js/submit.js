/**
   Setup qeditor
 */
/*
    Function validation the inputs of form
 */
var validateForm = function(){
    return true;
};

$("#body").qeditor({});

$("#submit").click(function(e){
    // TODO: validation of the form

    if(!validateForm()){
        e.preventDefault();
        return false;
    }else{
        var title = $("#title").val();
        var source = $("#source").val();
        var body = $("#body").val();

        console.log(title+"\n"+source+"\n"+body);
        return true;
    }
});

/*
    switch for the source info input of the original post
 */
$("#is_original").change(function(){
   if($(this).is(":checked")){  // post is origin, hide source info input
        $("#source_name").parent(".form-group").hide();
        $("#source_url").parent(".form-group").hide();
   }else{                       // post is not origin, show source info input
        $("#source_name").parent(".form-group").show();
        $("#source_url").parent(".form-group").show();
   }
});

/*
    category form listener
 */
$("input[type=radio][name=category]").change(function(e){
    var category = $(e.target).val();   // get category code

    // assign category class
    var className = 'article';
    if(category == 2){
        className = 'image';
    }else if(category == 3){
        className = 'video';
    }else if(category == 4){
        className = 'stuff'
    }

    // update form class
    $('#post-form')
        .removeClass('article image video stuff')
        .addClass(className);
});

/* ------------------------
    Image form control
 * ------------------------ */
var addImgInput = function(){
    var img_num = $("#img-section").find('input[type=file]').length;    // number of img input exist
    console.log(img_num);
    var imgInput = $('<input>')    // input tag
        .attr({
            "type": "file",
            "id": "img-"+img_num,
            "name": "img-"+img_num
        });
    var imgPre = $('<img>')         // img preview tag
        .attr({
            "id": "img-"+img_num+"-preview",
            "src": "#"
        });
    var imgDel = $('<div>')
        .attr({
            "id":"img-"+img_num+"-delete",
            "class":"img-delete"
        })
        .append('<i class="fa fa-times"></i>');

    // inputWrapper = <div> <input> <img> <div></div> </div>
    var inputWrapper = $('<div>')   // container of the image input and preview
        .attr({
            'id':"img-"+img_num+"-wrapper",
            "class":"img-placeholder"
        })
        .append(imgInput)
        .append(imgPre)
        .append(imgDel);

    inputWrapper.insertBefore($("#add-img")); // insert to DOM

    $(imgInput).change(function(){  // add change event listener
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            var preId = $(this).attr('id')+"-preview";

            reader.onload = function(){
                var src = reader.result;    // get local uploaded url
                $("#"+preId).attr('src', src);
            };
            console.log("change, file name: "+this.files[0].name);
            reader.readAsDataURL(this.files[0]);
        }
    });

    $(imgDel).click(function(){     // remove the image input wrapper
        $(inputWrapper).remove();
    });

    return imgInput;    // return the object for further action
};

$("#add-img").click(function(e){

    // loop through existing imgInput and find available/empty input tag to open file dialog
    var imgInputs = $("#img-section").find('input[type=file]');
    var imgInput = null;
    for(var i=0; i<imgInputs.length; i++){
        if(imgInputs[i].files.length <= 0){ // found empty file input tag
            imgInput = imgInputs[i];
        }
    }

    if(imgInput == null){   // no empty file input tag
        imgInput = addImgInput();  // add another image upload tag
    }
    $(imgInput).trigger('click');

    e.preventDefault();
    return false;
});
