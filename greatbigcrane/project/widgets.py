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

class LineEditorChoiceWidget(LineEditorWidget):

    def __init__(self, choices, *args, **kwargs):
        super(LineEditorChoiceWidget, self).__init__(*args, **kwargs)
        self.choices = choices

    def render(self, name, value, attrs=None):
        print("rendering...")
        rendered = super(LineEditorChoiceWidget, self).render(name, value, attrs)
        options = "".join(["<option value='%s'>%s</option>" % (c[0], c[1]) for c in self.choices])
        script = """<script type="text/javascript">
        $("#id_%(name)s_button").click(
            function() {
                $("#id_%(name)s").val($("#id_%(name)s").val() + "\\n" + $("#id_%(name)s_select").val());
            }
        );
</script>""" % {'name': name}
        return mark_safe("<select id='id_%(name)s_select'>%(options)s</select><button id='id_%(name)s_button' type='button'>insert</button>%(lineeditor)s%(script)s" % {
            'name': name,
            'options': options,
            'lineeditor': rendered,
            'script': script
            })
