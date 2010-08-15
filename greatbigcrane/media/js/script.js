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

function load_recipe_template() {
    $("#recipe_template_container").load("/projects/recipe_template/" +
            $('#available_recipes').val() + '/');
}

jQuery(function($){
  $('.autosubmit').change(function(){
    $(this).parents('form').first().submit();
  });
  
  $('div.projects .favourite').live('click', function(e){
    e.preventDefault();
    $.post( $(this).attr('href'), { update: '{"#project-list":"projects"}' }, ajaxHandler );
  });

  $('#available_recipes').change(load_recipe_template);
  
  $('div.dashboard .projects .favourite').live('click', function(e){
    e.preventDefault();
    $.post( $(this).attr('href'), { 
      update: '{"#project-list":"home-projects","#favourite-project-list":"favourite-projects"}' 
    }, ajaxHandler );
  })
  
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

