function slugify(string) {
  return string.replace(/\s+/g,'-').replace(/[^a-zA-Z0-9\-]/g,'').toLowerCase();
}

function ajaxHandler(data) {
  if (data.update) {
    $.each(data.update,function(k,v){
      $(k).html(v);
    });
  }
}

function dismiss_notification(notification_id) {
  $.get("/notifications/dismiss/" + notification_id + "/", {},
    function(data, textStatus, xhr) {
      $("#notification-" + notification_id).slideUp(function(){$(this).remove()});
  });
}

function load_recipe_template(project_id) {
  return (function(node) {
    if ($('#available_recipes').val() != "") {
      $("#recipe_template_container").load("/recipes/" + project_id +
        "/recipe_template/" +
        $('#available_recipes').val() + '/',function(){
          $("#id_eggs, #id_extra_paths").lineeditor();
        });
    }
  })
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

jQuery(function($){
  $('.autosubmit').change(function(){
    $(this).parents('form').first().submit();
  });
  
  $('.projects li').live('click', function(e){
    if ( e.isPropagationStopped() ) { return; }
    e.preventDefault();
    e.stopPropagation();
    var href = $(this).find('a.settings').attr('href');
    window.location = href;
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
  $('.actions .ajax').live('click',queue_button('closest', 'section'))
  $('.confirm').live('click',function(ev){
    ev.preventDefault();
    if ( confirm("Are you sure you want to do this?") ) {
      $('<form action="' + $(this).attr('href') + '" method="post"></form>').submit();
    } else {
      ev.preventDefault();
    }
  });
  

  $('div.dashboard .tests').ekko({url: '/notifications/ajax/'},
    function(data) {
      $(data).each(function(_,n){
        if ( n.id && $("#"+n.id).size() == 0 ) {
          $(n).css('display','none').prependTo($('div.dashboard ul.tests')).slideDown();
        }
      })
      $('div.dashboard ul.tests li:nth-child(11n)').slideUp(function(){$(this).remove()});
  });
  
  $('div.project .tests').ekko({url: '/project/' + $('#project').attr('id').replace(/\D/,'') + '/notifications/'},
    function(data) {
    $('div.dashboard ul.tests').empty().html(data);
  });
  
  $("#id_eggs, #id_extra_paths").lineeditor();
});

