from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.http import require_POST

from recipes.forms import recipe_form_map, BuildoutForm
from project.models import Project
import buildout_manage.parser
from cStringIO import StringIO

def add_recipe(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render_to_response("recipes/add_recipe.html", 
            RequestContext(request, {
                'project': project,
                'available_recipes': sorted(buildout_manage.recipes)}))

def edit_recipe(request, project_id, section_name):
    project = get_object_or_404(Project, id=project_id)
    buildout=project.buildout()
    section=buildout[section_name]
    recipe_name = section.get('recipe')
    if recipe_name not in buildout_manage.recipes:
        return edit_buildout_section(request, project, buildout, section_name)
    recipe = buildout_manage.recipes[recipe_name](buildout, section_name)

    initial=recipe.dict()
    initial['name'] = section_name

    form = recipe_form_map[recipe_name](project, initial=initial)
    return render_to_response("recipes/edit_recipe.html", RequestContext(
        request, {'form': form,
            'template_name': "recipes/recipe_templates/%s.html" % recipe_name,
            'recipe_name': recipe_name,
            'project': project}))

def delete_recipe(request, project_id, section_name):
    project = get_object_or_404(Project, id=project_id)
    buildout = project.buildout()
    del buildout[section_name]
    buildout_manage.parser.buildout_write(project.buildout_filename(), buildout)
    return redirect(project.get_absolute_url())


def recipe_template(request, project_id, recipe_name):
    project = get_object_or_404(Project, id=project_id)
    form = recipe_form_map[recipe_name](project)
    return render_to_response("recipes/recipe_templates/%s.html" % recipe_name,
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
        return render_to_response("recipes/edit_recipe.html", RequestContext(
            request, {'form': form,
                'template_name': "recipes/recipe_templates/%s.html" % recipe_name,
                'recipe_name': recipe_name,
                'project': project}))

def edit_buildout_section(request, project, buildout, section_name):
    new_buildout = buildout_manage.parser.BuildoutConfig()
    new_buildout[section_name] = buildout[section_name]
    string = StringIO()
    buildout_manage.parser.buildout_write(string, new_buildout)

    initial = {'contents': string.getvalue()}
    form = BuildoutForm(request.POST or None, initial=initial)
    if form.is_valid():
        string = StringIO(str(form.cleaned_data['contents']))
        config = buildout_manage.parser.buildout_parse(string)
        buildout[section_name] = config[section_name]
        buildout_manage.parser.buildout_write(project.buildout_filename(), buildout)
        return redirect(project.get_absolute_url())

    return render_to_response("recipes/edit_buildout.html", RequestContext(
        request, {'form': form, 'project': project}))
