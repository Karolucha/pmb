// initialise editor

$('textarea').summernote({
        onImageUpload: function(files, editor, welEditable) {
            sendFile(files[0], editor, welEditable);
        }
});

// send the file

function sendFile(file, editor, welEditable) {
        data = new FormData();
        data.append("file", file);
        $.ajax({
            data: data,
            type: 'POST',
            xhr: function() {
                var myXhr = $.ajaxSettings.xhr();
                if (myXhr.upload) myXhr.upload.addEventListener('progress',progressHandlingFunction, false);
                return myXhr;
            },
            url: root + '/upload_image',
            cache: false,
            contentType: false,
            processData: false,
            success: function(url) {
                console.log('what is success', url)
                //editor.insertImage(welEditable, url);
            }
        });
}


// update progress bar

function progressHandlingFunction(e){
    if(e.lengthComputable){
        $('progress').attr({value:e.loaded, max:e.total});
        // reset progress on complete
        if (e.loaded == e.total) {
            $('progress').attr('value','0.0');
        }
    }
}
//  $(function() {
//    $('textarea')
//      .froalaEditor({
//        // Set the image upload parameter.
//        //     imageUploadParam: 'image_param',
//        // Set the image upload URL.
//        imageUploadURL: '/upload_image',
//        // Additional upload params.
//        imageUploadParams: {'csrfmiddlewaretoken': document.getElementById('csrf-token')},
//        // Set request type.
//        imageUploadMethod: 'POST',
//        imageManagerLoadURL: "/load_images",
//        // Set the load images request type.
//        imageManagerLoadMethod: "GET",
//        // Set max image size to 5MB.
//        //   imageMaxSize: 5 * 1024 * 1024,
//        // Allow to upload PNG and JPG.
//        imageAllowedTypes: ['jpeg', 'jpg', 'png']
//      })
//      .on('froalaEditor.image.beforeUpload', function (e, editor, images) {
//        console.log('IMAGE will be upload')
//        // Return false if you want to stop the image upload.
//      })
//      .on('froalaEditor.image.uploaded', function (e, editor, response) {
//        // Image was uploaded to the server.
//      })
//      .on('froalaEditor.image.inserted', function (e, editor, $img, response) {
//        // Image was inserted in the editor.
//      })
//      .on('froalaEditor.image.replaced', function (e, editor, $img, response) {
//        // Image was replaced in the editor.
//      })
//      .on('froalaEditor.image.error', function (e, editor, error, response) {
//        // Bad link.
//        console.log(e)
//        console.log(editor)
//        console.log(error)
//        console.log(response)
//        if (error.code == 1) { console.log('badlink') }
//
//        // No link in upload response.
//        else if (error.code == 2) { console.log(' No link in upload response.') }
//
//        // Error during image upload.
//        else if (error.code == 3) { console.log(' Error during image upload.')
//         console.log(error)}
//
//        // Parsing response failed.
//        else if (error.code == 4) { console.log('Parsing response failed.') }
//
//        // Image too text-large.
//        else if (error.code == 5) { console.log(' Image too text-large') }
//
//        // Invalid image type.
//        else if (error.code == 6) { console.log(' Invalid image type.') }
//
//        // Image can be uploaded only to same domain in IE 8 and IE 9.
//        else if (error.code == 7) { console.log('badlink') }
//
//        // Response contains the original server response to the request if available.
//      });
//  });