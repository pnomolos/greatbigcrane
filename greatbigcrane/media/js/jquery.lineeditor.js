(function($) {
  jQuery.fn.lineeditor = function (options, callback) {
    return this.each(function () {
      var el = this;
      var $el = $(this);
      
      if (el.nodeName.toLowerCase() != 'textarea') { return; }
      
      var hidden = $('<input type="hidden">').attr('id', el.id).attr('name',el.name).val($el.val());
      var container = $('<div class="lineeditor"></div>');
      var val = $el.val();
      
      var buttons = $('<span class="buttons"></span>');
      $.each({
        'delete': removeLine,
        'moveup': move('up'),
        'movedown': move('down')
      },function(k,v){
        var node = $('<a href="#' + k + '" class="' + k + '">' + k + '</a>').click(v);
        buttons.append(node);
      });
      
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
        container.find('a:last').before(input_container.append(input).append(buttons.clone(true)));
        processValues();
        calculatePositioning();
        return input;
      }
      
      function removeLine(ev) {
        ev.preventDefault();
        $(this).closest('.input').remove();
        processValues();
      }
      
      function move(direction) {
        return (function(ev) {
          ev.preventDefault();
          var target = $(this).closest('.input');
          if (direction == 'down') {
            target.insertAfter(target.next('.input'));
          } else if ( direction == 'up' ) {
            target.insertBefore(target.prev('.input'));
          }
          calculatePositioning();
        })
      }
      
      function processValues(e) {
        if (e && e.keyCode == 9) {
          e.preventDefault();
          target = $(e.target).closest('.input');
          if (!e.shiftKey) {
            target.nextAll('.input:first').find('input[type=text]:first').focus().size() || addLine().focus(); 
          } else {
            target.prevAll('.input:first').find('input[type=text]').focus();
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
          if ( $(this).prev('.input').size() ) {
            $(this).find('.moveup').size() || $(this).find('.buttons').append(buttons.find('.moveup').clone(true));
          } else {
            $(this).find('.moveup').remove();
          }
          
          if ( $(this).next('.input').size() ) {
             $(this).find('.movedown').size() || $(this).find('.buttons').append(buttons.find('.movedown').clone(true));
          } else {
            $(this).find('.movedown').remove();
          }
          
          $(this).width($(this).find('input[type=text]').outerWidth());
        })
      }
      
    })
  }
})(jQuery);