(function($) {
  jQuery.fn.lineeditor = function (options, callback) {
    return this.each(function () {
      var el = this;
      var $el = $(this);
      
      if (el.nodeName.toLowerCase() != 'textarea') { return; }
      
      var hidden = $('<input type="hidden">').attr('id', el.id).attr('name',el.name).val($el.val());      
      var container = $('<div class="lineeditor"></div>');
      var val = $el.val();
      
      hidden.val(val);
      container.append(hidden);
      
      container.append($('<a href="#add-line">Add Line</a>').click(addLine));
      $.each(val.split("\n"),function(){
        addLine(this);
      });
      

      $el.replaceWith(container);
      calculatePositioning();
      
      
      function addLine(value) {
        value = (value && value.target ? value.preventDefault() && '' : value);
        var input = $('<input type="text">').val(value?value.toString():'').keydown(processValues);
        var input_container = $('<span class="input"></span>');
        var button_container = $('<span class="buttons"></span>');
        var delete_button = $('<a href="#delete" class="delete">Delete</a>').click(removeLine);
        container.find('a:last').before(input_container.append(input, button_container.append(delete_button)));
        processValues();
        calculatePositioning()
        return input;
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
      
      function calculatePositioning() {
        container.find('.input').each(function(){
          $(this).width($(this).find('input[type=text]').outerWidth());
        })
      }
      
    })
  }
})(jQuery);