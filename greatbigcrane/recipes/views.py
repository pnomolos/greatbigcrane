from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.http import require_POST

from recipes.forms import recipe_form_map
from project.models import Project
import buildout_manage

def add_recipe(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render_to_response("project/add_recipe.html", 
            RequestContext(request, {
                'project': project,
                'available_recipes': sorted(buildout_manage.recipes)}))

def edit_recipe(request, project_id, recipe_name):
    #FIXME: rename recipe_name to section_name to avoid confusion
    # and recipe_type to recipe_name
    project = get_object_or_404(Project, id=project_id)
    buildout=project.buildout()
    section=buildout[recipe_name]
    recipe_type = section['recipe']
    recipe = buildout_manage.recipes[recipe_type](buildout, recipe_name)

    form = recipe_form_map[recipe_type](project, initial=recipe.dict())
    return render_to_response("project/edit_recipe.html", RequestContext(
        request, {'form': form,
            'template_name': "project/recipe_templates/%s.html" % recipe_type,
            'recipe_name': recipe_type,
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


