from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.http import require_POST

from recipes.forms import recipe_form_map, BuildoutForm
from project.models import Project
import buildout_manage.parser
from cStringIO import StringIO

def add_recipe(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render_to_response("project/add_recipe.html", 
            RequestContext(request, {
                'project': project,
                'available_recipes': sorted(buildout_manage.recipes)}))

def edit_recipe(request, project_id, section_name):
    project = get_object_or_404(Project, id=project_id)
    buildout=project.buildout()
    section=buildout[section_name]
    if section_name == "buildout":
        return edit_buildout_section(request, project, buildout)
    recipe_name = section.get('recipe')
    recipe = buildout_manage.recipes[recipe_name](buildout, section_name)

    form = recipe_form_map[recipe_name](project, initial=recipe.dict())
    return render_to_response("project/edit_recipe.html", RequestContext(
        request, {'form': form,
            'template_name': "project/recipe_templates/%s.html" % recipe_name,
            'recipe_name': recipe_name,
            'project': project}))

def recipe_template(request, project_id, recipe_name):
    project = get_object_or_404(Project, id=project_id)
    form = recipe_form_map[recipe_name](project)
    return render_to_response("project/recipe_templates/%s.html" % recipe_name,
            {'form': form})

@require_POST
def save_recipe(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    recipe_name = request.POST['recipe_name']
    form = recipe_form_map[recipe_name](project, request.POST)
    if form.is_valid():
        buildout = project.buildout()
        form.save(buildout)
        return redirect(project.get_absolute_url())
    else:
        return render_to_response("project/recipe_templates/%s.html" % recipe_name,
                {'form': form})


def edit_buildout_section(request, project, buildout):
    new_buildout = buildout_manage.parser.BuildoutConfig()
    new_buildout['buildout'] = buildout['buildout']
    string = StringIO()
    buildout_manage.parser.buildout_write(string, new_buildout)

    initial = {'contents': string.getvalue()}
    form = BuildoutForm(request.POST or None, initial=initial)
    if form.is_valid():
        string = StringIO(form.cleaned_data['contents'])
        config = buildout_manage.parser.buildout_parse(string)
        buildout['buildout'] = config['buildout']
        buildout_write(self.project.buildout_filename(), buildout)
        return redirect(project.get_absolute_url())

    return render_to_response("recipes/edit_buildout.html", RequestContext(
        request, {'form': form, 'project': project}))
