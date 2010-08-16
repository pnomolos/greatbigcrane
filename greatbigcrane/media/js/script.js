function dismiss_notification(notification_id) {
  $.get("/notifications/dismiss/" + notification_id + "/", {},
    function(data, textStatus, xhr) {
      $("#notification-" + notification_id).slideUp(function(){$(this).remove()});
  });
}

function slugify(string) {
  return string.replace(/\s+/g,'-').replace(/[^a-zA-Z0-9\-]/g,'').toLowerCase();
}

function load_recipe_template(project_id) {
  return (function(node) {
    if ($('#available_recipes').val() != "") {
      $("#recipe_template_container").load("/recipes/" + project_id +
        "/recipe_template/" +
        $('#available_recipes').val() + '/',function(){
          $("#id_eggs, #id_extra_paths").lineeditor();
        }
      );
    }
  })
}

jQuery(function($){
  function ajaxHandler(data) {
    if (data.update) {
      $.each(data.update,function(k,v){
        $(k).html(v);
      });
    }
  }

  function queue_button(node_or_function_string,selector) {
    return (function(ev) {
      if ( typeof node_or_function_string == 'string' ) {
        node = $(this)[node_or_function_string](selector);
      } else {
        node = node_or_function_string;
      }
      ev.preventDefault(); ev.stopPropagation();
      $.ajax({
        url: $(this).attr('href'),
        success: show_queuing_response(node),
        error: show_queuing_response(node)
      });
    });
  }

  function show_queuing_response(node) {
    return (function(data_or_xhr, textStatus) {
      var to_append = '';
      switch (textStatus) {
        case null:
        case 'timeout':
        case 'error':
        case 'notmodified':
        case 'parsererror':
          to_append = '<span class="error notice">' + data_or_xhr.responseText + '</span>';
          break;
        default:
          to_append = '<span class="success notice">' + data_or_xhr + '</span>';
          break;
      }
      to_append = $(to_append).css('display','none');
      $(to_append).appendTo(node).slideDown().delay(2000).slideUp(function(){$(this).remove()});
    });
  }

  function ajax_update(params) {
    if ( !params ) {
      params = [];
      if ( $('div.project').size() ) {
        params.push( '"#project-list":"projects"' )
      } else {
        params.push( '"#project-list":"home-projects"' )
      }
      params.push( '"#favourite-project-list":"favourite-projects"' );
      params = '{' + params.join(',') + '}'
    }
    $.post('/projects/ajax', { 
      update: params
    }, ajaxHandler);
  }

  function update_notifications(data) {
    var $el = $(this);
    var number_to_remove = $el.find('li').size()-10;
    $(data).each(function(_,n){
      if ( n.id && $("#"+n.id).size() == 0 ) {
        var id = parseInt(n.id.replace(/\D*/,''));
        var node_after = added = null;
        $('.tests li').each(function(){
          if ( added ) { return false; }
          if ( parseInt(this.id.replace(/\D*/,'')) > id ) {
            node_after = this;
          } else {
            $(n).css('display','none').insertBefore($(this)).slideDown();
            number_to_remove++;
            added = true;
          }
        })
        if ( node_after && !added ) {
          $(n).css('display','none').insertAfter($(node_after)).slideDown();
          number_to_remove++;
          added = true;
        } else if ( !node_after && !added ) {
          $(n).css('display','none').appendTo($el).slideDown();
          number_to_remove++;
          added = true;
        }
        if ( added ) {
          notification_handler($(n));
        }
      }
    });
    while ( number_to_remove-- > 0 ) {
      $el.find('li:last').remove();
    }
    // Update the testing button on the project detail page
    if ( $('#sidebar .project').size() ) {
      if ( $el.find('li[rel*=TEST]:first').hasClass('success') ) {
        $('#sidebar .project .actions .tests').addClass('success')
      } else {
        $('#sidebar .project .actions .tests').removeClass('success').addClass('error');
      }
    }
    ajax_update();
  }
  
  function notification_handler(node) {
    if ( node.attr('rel') == 'GITCLONE' && node.hasClass('success') ) {
      confirm("The git clone has completed.  Would you like to refresh the page?") && window.location.reload();
    }
  }

  $('.autosubmit').change(function(){
    $(this).parents('form').first().submit();
  });
  
  $('.projects li').live('click', function(e){
    if ( e.isPropagationStopped() ) { return; }
    e.preventDefault();
    e.stopPropagation();
    var id = $(this).attr('id');
    id = id.match(/project-(\d+)/)[1];
    var href = "/projects/" + id + "/view/";
    window.location = href;
  });
  
  $('ul.projects .edit').live('click', function(e){
    e.stopPropagation();
  });

  $('div.projects .favourite').live('click', function(e){
    e.preventDefault();
    e.stopPropagation();
    var href = $(this).attr('href') + '?' + $(this).parents('form').serialize();
    $.post(href, {update: '{"#project-list":"projects"}'}, ajaxHandler);
  });
  
  $('div.dashboard .projects .favourite').live('click', function(e){
    e.preventDefault();
    e.stopPropagation();
    $.post($(this).attr('href'), { 
      update: '{"#project-list":"home-projects","#favourite-project-list":"favourite-projects"}' 
    }, ajaxHandler);
  });
  
  $('.projects .buildout, .projects .tests').live('click',queue_button('closest', 'li'));
  $('.actions .ajax').live('click',queue_button('closest', 'div.project > section'));
  $('.confirm').live('click',function(e){
    e.preventDefault();
    if ( confirm("Are you sure you want to do this?") ) {
      $('<form action="' + $(this).attr('href') + '" method="post"></form>').submit();
    } else {
      e.preventDefault();
    }
  });
  
  $('div.dashboard ul.tests:first').ekko(
    {
      url: '/notifications/ajax/',
      minTimeout: 500,
      maxTimeout: 5000
    },
  update_notifications);
  
  if ( $('#content .project:first').size() ) {
    $('div.project .tests.live:first').ekko(
      {
        url: '/projects/' + $('#content .project:first').attr('id').replace(/\D*/,'') + '/notifications/',
        minTimeout: 500,
        maxTimeout: 5000
      },update_notifications);
  }
  
  $("#recipe_form").submit(function() {
    if ($("#available_recipes").val() == "") {
      alert("Must select a recipe");
      return false;
    }
    return true;
  });
});

