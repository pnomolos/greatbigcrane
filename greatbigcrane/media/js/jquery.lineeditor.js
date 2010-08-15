(function($) {
  jQuery.fn.lineeditor = function (options, callback) {
    return this.each(function () {
      var el = this;
      var $el = $(this);
      
      if ( el.nodeName.toLowerCase() != 'textarea' ) { return; }
      
      var hidden = $('<input type="hidden"/>').attr('id', el.id);      
      var container = $('<div class="lineeditor"></div>');
      var val = $el.val();
      
      hidden.val(val);
      container.append(hidden);
      
      container.append($('<a href="#add-line">Add Line</a>').click(addLine));
      $.each(val.split("\n"),function(){
        addLine(this);
      });
      

      $el.replaceWith(container);
      
      function addLine(value) {
        value = ( value.target ? value.preventDefault() && '' : value );
        var node = $('<input type="text"/>').val(value?value.toString():'');
        var delete_node = $('<a href="#delete" class="delete">Delete</a>').click(removeLine);
        container.find('a:last').before(node, delete_node);
      }
      
      function removeLine(ev) {
        ev.preventDefault();
        $(this).prev().remove();
        $(this).remove();
      }
      
    })
  }
})(jQuery);