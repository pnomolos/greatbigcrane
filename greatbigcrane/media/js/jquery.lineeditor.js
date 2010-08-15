(function($) {
  jQuery.fn.lineeditor = function (options, callback) {
    return this.each(function () {
      var el = this;
      var $el = $(this);
      
      if ( el.nodeName.toLowerCase() != 'textarea' ) { return; }
      
      var hidden = $('<input type="hidden"/>').attr('id', el.id).attr('name',el.name);      
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
        value = ( value && value.target ? value.preventDefault() && '' : value );
        var node = $('<input type="text"/>').val(value?value.toString():'').keydown(processValues);
        var delete_node = $('<a href="#delete" class="delete">Delete</a>').click(removeLine);
        container.find('a:last').before(node, delete_node);
        processValues();
        return node;
      }
      
      function removeLine(ev) {
        ev.preventDefault();
        $(this).prev().remove();
        $(this).remove();
        processValues();
      }
      
      function processValues(e) {
        if (e && e.keyCode == 9) {
          e.preventDefault();
          if ( !e.shiftKey ) {
            $(e.target).nextAll('input[type=text]:first').focus().size() || addLine().focus(); 
          } else {
            console.log($(e.target));
            $(e.target).prevAll('input[type=text]:first').focus();
          } 
          return;
        }
        hidden.val(
          container.find('input[type=text]').map(function(){
            return $(this).val();
          }).toArray().join("\n").trim()
        );
      }
      
    })
  }
})(jQuery);