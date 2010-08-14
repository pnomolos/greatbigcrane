function slugify(string) {
    return string.replace(/\s+/g,'-').replace(/[^a-zA-Z0-9\-]/g,'').toLowerCase();
}

function ajaxRequest( url, _data ) {
  callback = _data['update'] ? function(data) { $(_data['update']).html(data.html) } : $.noop;
  $.post( url, data, callback );
}

jQuery(function($){
  $('.autosubmit').change(function(){
    $(this).parents('form').first().submit();
  });
  
  $('.buttons .favourite').click(function(e){
    e.preventDefault();
    ajaxRequest( $(this).attr('href'), { update: '#project-list' } );
  });
});

