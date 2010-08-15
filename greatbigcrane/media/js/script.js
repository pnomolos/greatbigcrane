function slugify(string) {
  return string.replace(/\s+/g,'-').replace(/[^a-zA-Z0-9\-]/g,'').toLowerCase();
}

function ajaxHandler( data ) {
  if ( data.update ) {
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
          "recipe_template/" + '/' +
          $('#available_recipes').val() + '/');
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
    $(to_append).appendTo(node.parents('li')).slideDown().delay(2000).slideUp(function(){$(this).remove();});
  });
}

jQuery(function($){
  $('.autosubmit').change(function(){
    $(this).parents('form').first().submit();
  });
  
  $('div.projects .favourite').live('click', function(e){
    e.preventDefault();
    var href = $(this).attr('href') + '?' + $(this).parents('form').serialize();
    $.post( href, { update: '{"#project-list":"projects"}' }, ajaxHandler );
  });

  $('div.dashboard .projects .favourite').live('click', function(e){
    e.preventDefault();
    $.post( $(this).attr('href'), { 
      update: '{"#project-list":"home-projects","#favourite-project-list":"favourite-projects"}' 
    }, ajaxHandler );
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
  
  // if ($('.notifications').size()) {
  //   var paper = Raphael(
  //     $(".notifications .svg").get(0),
  //     100,
  //     Math.max($('.successes').height(), $('.errors').height())
  //   );
  //   var $paper = $(".notifications .svg").first();
  //   var first_success = parseInt($('.successes li').first().attr('id').replace(/\D*/,''));
  //   var first_error = parseInt($('.errors li').first().attr('id').replace(/\D*/,''));
  //   
  //   var cur_id = Math.max(first_success, first_error);
  //   do {
  //     var node = $('#notification-' + cur_id);
  //     var prev_node = $('#notification-' + (cur_id + 1));
  //     if ( node.size() && prev_node.size() && node.attr('class') != prev_node.attr('class')) {
  //       var line = paper.path("M{0},{1} L{2},{3}",
  //         prev_node.hasClass('error')?100:0, prev_node.position().top - $paper.position().top + (prev_node.height()/2),
  //         node.hasClass('error')?100:0, node.position().top - $paper.position().top + (node.height()/2)
  //       ).attr('stroke', prev_node.children('a').css('background-color')).attr('stroke-width', 2);
  //     }
  //     cur_id--;
  //   } while ( node.size() )
  // }
});

