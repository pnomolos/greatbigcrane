(function($) {
  jQuery.fn.lineeditor = function () {
    return this.each(function () {
      if ( this.liveeditor ) {
        return this.liveeditor;
      }
      
      this.liveeditor = function() {
        if (this.nodeName.toLowerCase() != 'textarea') { return; }
        
        var el = {};
        $el = $(this);
        
        el.addLine = function(value) {
          value = (value && value.target ? value.preventDefault() && '' : value);
          var input = $('<input type="text">').val(value?value.toString():'').change(el.processValues).keyup(el.processValues).keypress(el.processValues);
          var input_container = $('<span class="input"></span>');
          el.container.find('a:last').before(input_container.append(input).append(el.buttons.clone(true)));
          el.processValues();
          el.calculatePositioning();
          return input;
        }
      
        el.removeLine = function(ev) {
          ev.preventDefault();
          $(this).closest('.input').remove();
          el.processValues();
        }
      
        el.move = function(direction) {
          return (function(ev) {
            ev.preventDefault();
            var target = $(this).closest('.input');
            if (direction == 'down') {
              target.insertAfter(target.next('.input'));
            } else if ( direction == 'up' ) {
              target.insertBefore(target.prev('.input'));
            }
            el.calculatePositioning();
          })
        }
      
        el.processValues = function(e) {
          if (e && e.keyCode == 9) {
            e.preventDefault();
            target = $(e.target).closest('.input');
            if (!e.shiftKey) {
              target.nextAll('.input:first').find('input[type=text]:first').focus().size() || el.addLine().focus(); 
            } else {
              target.prevAll('.input:first').find('input[type=text]').focus();
            } 
            return;
          }
          el.hidden.val(
            el.container.find('input[type=text]').map(function(){
              return $(this).val();
            }).toArray().join("\n").trim()
          );
        }
      
        el.calculatePositioning = function() {
          el.container.find('.input').each(function(){
            if ( $(this).prev('.input').size() ) {
              $(this).find('.moveup').size() || $(this).find('.buttons').append(el.buttons.find('.moveup').clone(true));
            } else {
              $(this).find('.moveup').remove();
            }
          
            if ( $(this).next('.input').size() ) {
               $(this).find('.movedown').size() || $(this).find('.buttons').append(el.buttons.find('.movedown').clone(true));
            } else {
              $(this).find('.movedown').remove();
            }
          
            $(this).width($(this).find('input[type=text]').outerWidth());
          })
        }
        
        el.$el = $el;
        
        el.hidden = $('<input type="hidden">').attr('id', this.id).attr('name',this.name).val($el.val());
        el.container = $('<div class="lineeditor"></div>');
        el.val = $el.val();
      
        el.buttons = $('<span class="buttons"></span>');
        $.each({
          'delete': el.removeLine,
          'moveup': el.move('up'),
          'movedown': el.move('down')
        },function(k,v){
          var node = $('<a href="#' + k + '" class="' + k + '">' + k + '</a>').click(v);
          el.buttons.append(node);
        });
        
        el.hidden.val(el.val);
        el.container.append(el.hidden);
        
        el.container.append($('<a href="#add-line">Add Line</a>').click(el.addLine));
        $.each(el.val.split("\n"),function(){
          el.addLine(this);
        });
        
        $el.replaceWith(el.container);
        el.calculatePositioning();
        
      }
      return this.liveeditor();
    })
  }
})(jQuery);