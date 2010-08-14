function slugify(string) {
    return string.replace(/\s+/g,'-').replace(/[^a-zA-Z0-9\-]/g,'').toLowerCase();
}

jQuery(function($){
  $('.autosubmit').change(function(){
    $(this).parents('form').first().submit();
  })
});