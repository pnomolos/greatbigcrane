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
      $("#recipe_template_container").load("/projects/" + project_id +
        "/recipe_template/" +
        $('#available_recipes').val() + '/',function(){
          $("#id_eggs, #id_extra_paths").lineeditor();
        });
    }
  })
}


function show_buildout_result(node) {
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
    $(to_append).appendTo(node.parents('li')).slideDown().delay(2000).slideUp(function(){$(this).remove()});
  });
}

jQuery(function($){
  $('.autosubmit').change(function(){
    $(this).parents('form').first().submit();
  });
  
  $('.projects li').live('click', function(e){
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

  $('div.dashboard .projects .buildout, div.dashboard .projects .tests').live('click', function(e){
    e.preventDefault();
    $.ajax({
      url: $(this).attr('href'),
      success: show_buildout_result($(this)),
      error: show_buildout_result($(this))
    });
  })

  $('div.dashboard .tests').ekko({url: '/notifications/ajax/'},
    function(data) {
      $(data).each(function(_,n){
        if ( n.id && $("#"+n.id).size() == 0 ) {
          $(n).css('display','none').prependTo($('div.dashboard ul.tests')).slideDown();
        }
      })
      $('div.dashboard ul.tests li:nth-child(11n)').slideUp(function(){$(this).remove()});
  });
  
  $("#id_eggs, #id_extra_paths").lineeditor();
});

