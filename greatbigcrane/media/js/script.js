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

jQuery(function($){
  $('.autosubmit').change(function(){
    $(this).parents('form').first().submit();
  });
  
  $('.buttons .favourite').live('click', function(e){
    e.preventDefault();
    $.post( $(this).attr('href'), { update: '#project-list' }, ajaxHandler );
  });
});

