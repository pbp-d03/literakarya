function showPost(){
    $.get("./json/all-posts", function(item){
      if(item.length == 0){
        $("#posts").append(
          '<h3 id="nopost" class="my-5" style="text-align: center">Belum ada topik pembicaraan</h3>'
        )
      }
      else{
        for(let i=0; i<item.length; i++) {
          putPost(item[i]);
          putReplyPost(item[i]);
        }
      }
    })
  }
  
  function putPost(post){
    // put post
    let user_username = JSON.parse(document.getElementById('user_username').textContent);
    let deleteOption = (user_username === post.fields.user.username)
                      ?`<h5 class="bi bi-three-dots-vertical" role="button" id="dropdownMenuLink" data-bs-toggle="dropdown" aria-expanded="false" style="float:right"></h5>
                      <ul class="dropdown-menu" aria-labelledby="dropdownMenuLink">
                        <li>
                          <a class="dropdown-item" id="delete-post-${post.pk}" href="delete-post/${post.pk}">
                            Delete Post
                          </a>
                        </li>
                      </ul>` 
                      : '';
    let replyOption = (!user_username) 
                      ? '' 
                      : `<a data-bs-toggle="collapse" href="#reply-${post.pk}" role="button" aria-expanded="false" aria-controls="collapseExample">
                          <i class="icon bi bi-reply" style="color:#000"></i>
                        </a>`;
  
    $("#posts").prepend(
      `\n<div class="flex-grow-1 py-2 my-4 mx-3 card">
        <div id="post-${post.pk}">
          <div class="card-body px-4 pt-3 pb-3">
            <div>
              ${deleteOption}
              <h6>${post.fields.user.name} <small class="text-muted"><i>  —  ${post.fields.user.role}</i></small></h6>
            </div>
            <h3 class="card-title pt-2">
              ${post.fields.title}<br>
              <small class="date-info text-muted">${post.fields.date}</small>
            </h3>
            <p class="card-text pt-2">${post.fields.body}</p>
          </div>
        
          <div class="icon-group mb-2">
            ${replyOption}
  
            <a data-bs-toggle="collapse" href="#comment-post-${post.pk}" role="button" aria-expanded="false" class="collapsed mx-5">
              <i class="icon bi bi-eye if-collapsed" style="color:#000"></i>
              <i class="icon bi bi-eye-slash if-not-collapsed" style="color:#000"></i>
            </a>
          </div>
  
          <div class="collapse mt-2 mx-4" id="reply-${post.pk}">
            <form method="POST" id="add-comment-${post.pk}">
              <textarea type="text" name="comment-body-${post.pk}" id="comment-body-${post.pk}" class="form-control" required></textarea>
              <button class="btn btn-dark" type="submit" style="margin-top: 10px"> add comment </button>
            </form>
          </div>
        </div>
  
        <div id="comment-post-${post.pk}" class="collapse">
          <!--- comment replies will be appended through ajax --->
        </div>
      </div>`
    );
    
    $.get(`./json/all-comments/${post.pk}`, function(comments){
      if(comments.length == 0){
        $(`#comment-post-${post.pk}`).append(
          `<h6 id="nocomment-${post.pk}" class="pt-3" style="text-align: center">No comments yet..</h6>`
        )
      }
      else{
          for(let j=0; j<comments.length; j++){
            putReply(comments[j]);
          }
        }
    })
  }
  
  function putReply(comment){
    // removing the "No Comments Yet.." text from DOM
    $(`#nocomment-${comment.fields.post}`).remove();
  
    // put reply
    let user_username = JSON.parse(document.getElementById('user_username').textContent);
    let deleteOption = (user_username === comment.fields.user.username)
                      ?`<h5 class="bi bi-three-dots-vertical" role="button" id="dropdownMenuLink" data-bs-toggle="dropdown" aria-expanded="false" style="float:right"></h5>
                        <ul class="dropdown-menu" aria-labelledby="dropdownMenuLink">
                          <li>
                            <a class="dropdown-item" id="delete-comment-${comment.pk}" href="delete-comment/${comment.pk}")">
                              Delete comment
                            </a>
                          </li>
                        </ul>` 
                      : '';
    $(`#comment-post-${comment.fields.post}`).append(
      `<div class="card-body mt-2 px-3 pt-3 border-top" id="comment-${comment.pk}">
        <div class="mx-4">
          ${deleteOption}
          <h6>${comment.fields.user.name} <small class="text-muted"><i>  —  ${comment.fields.user.role}</i></small></h6>
          <small class="date-info text-muted">${comment.fields.date}</small>
          <p class="pt-2">${comment.fields.body}</p>
          </div>
      </div>`
    );
  }
  
  function putReplyPost(post){
    $(`#add-comment-${post.pk}`).submit(function(event){
      event.preventDefault();
      $.post(`add-comment/${post.pk}`, {
        body : $(`#comment-body-${post.pk}`).val()
      }).done(function(data){
        // action on form
        $(`#add-comment-${post.pk}`)[0].reset();
        $(`#add-comment-${post.pk}`).collapse('hide');
        
        // putting the reply
        putReply(data);
        
        // redirect to comment
        $(`#comment-post-${post.pk}`).collapse('show');
        location.href = "#";
        location.href = `#comment-${data.pk}`;
      })
    })
  }
  
  function addPost(){
    $.post("add-post/", {
      title : $("#title").val(),
      body  : $("#body").val(),
    }).done(function(data){
      // action on form
      $("#add-post")[0].reset();
      
      // putting the post
      putPost(data);
      
      // redirect to post
      location.href = "#";
      location.href = `#post-${data.pk}`;
    })
  }
  
  // <!-- ajax setup below is for csrf -->
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  
  $.ajaxSetup({ 
    beforeSend: function(xhr, settings) {
      if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      }
    } 
  });
  
  $(document).ready(function(){
    showPost();
  
    $(`#add-post`).submit(function(event){
      event.preventDefault();
      addPost();
    });
  })