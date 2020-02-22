window.addEventListener('load', function() {

    var csrftoken;
    var xhr;
    var allTodos;

    // function to get cookie using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    // function to rotate image (refresh button)
    function rotateImage() {
        var rotation = 0;
        var i = setInterval(function(){
            $("#refresh").css({'-webkit-transform' : 'rotate('+ rotation +'deg)',
                             '-moz-transform' : 'rotate('+ rotation +'deg)',
                             '-ms-transform' : 'rotate('+ rotation +'deg)',
                             'transform' : 'rotate('+ rotation +'deg)'});
            rotation += 60;
        if(rotation > 360) {
            clearInterval(i);
            rotation = 0;
        }
        }, 120);

    }
    // function to update todo note
    function refreshTodo(){
         // send request to save todos to database
        xhr = new XMLHttpRequest();
        if (!xhr) {
          return false;
        }
    //      get all current todo items
          allTodos = [];
          $("#todoItem li").each(function() {
            var item = {content: $(this).text().trim(), isCompleted: $(this).hasClass('completed') ? 1 : 0};
            allTodos.push(JSON.stringify(item));
            });
          allTodos.reverse();
    //      allTodos = JSON.stringify({ 'list': allTodos });

    //      Below code is to send POST request to updateTodos method using AJAX
          function csrfSafeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
          }
          $.ajax({
            url: 'updateTodos',
            data: {'allTodos[]': allTodos},
            beforeSend: function(xhr, settings) {
              if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
              }
            },
            dataType: "json",
            type: "POST",
    //        success: do something here which we dont need for now
          });

//          call function to rotate image
//          rotateImage();
     }


    csrftoken = getCookie('csrftoken');

    $("#todoItem").on("click","li", function(){
        $(this).toggleClass("completed");
        refreshTodo();
    })

    $("#todoItem").on("click",".delete", function(event){
        $(this).parent().fadeOut(300, function(){
            $(this).remove();
            refreshTodo();
        })
        event.stopPropagation();
    })

    $("input").on("keypress", function(event){
        var inputText = $(this).val();
        if(event.which === 13){
            $("#todoItem").prepend("<li><span class='delete'><i class='fa fa-minus-square-o' aria-hidden='true'></i></span>"+ inputText +" <i class='fa fa-star-o' aria-hidden='true'></i> <i class='fa fa-pencil' aria-hidden='true'></i></li>");
            $(this).val("");
            refreshTodo();
        }

    })

    // update once click refresh button
    $("#refresh").on("click", refreshTodo)


    $(".fa-plus-square-o").on("click", function(){
        $("#addNew").fadeToggle(300);
    })


//    // set interval for auto update
//    setInterval(refreshTodo, 60000);

//    // update when close window
//    $(window).on("beforeunload", refreshTodo)
//
//    $(window).hashchange(refreshTodo)

});
