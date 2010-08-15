from django.forms.widgets import Textarea
from django.utils.safestring import mark_safe

class LineEditorWidget(Textarea):
    class Media:
        js = ('js/jquery-1.4.2.min.js' ,'js/jquery.lineeditor.js')

    def render(self, name, value, attrs=None):
        if isinstance(value,list):
            value = "\n".join(value)
        rendered = super(LineEditorWidget, self).render(name, value, attrs)
        return rendered + mark_safe(u'''<script type="text/javascript" defer="defer">
            $(function() {
                $("#id_%s").lineeditor();
            }
            );
            </script>''' % (name))
