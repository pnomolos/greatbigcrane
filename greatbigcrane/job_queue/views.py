from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseServerError
from django.template import RequestContext
from project.models import Project
from job_queue.jobs import queue_job
from job_queue.forms import StartAppForm

def schedule_buildout(request, project_id):
    return schedule_project_command(request, project_id, "BUILDOUT",
            "Successfully queued buildout")

def schedule_bootstrap(request, project_id):
    return schedule_project_command(request, project_id, "BOOTSTRAP",
            "Successfully queued bootstrap")

def schedule_test(request, project_id):
    return schedule_project_command(request, project_id, "TEST",
            "Successfully queued test")

def schedule_pull(request, project_id):
    return schedule_project_command(request, project_id, "GITPULL",
            "Successfully queued git pull")

def schedule_syncdb(request, project_id):
    return schedule_project_command(request, project_id, "SYNCDB",
            "Successfully queued syncdb")

def schedule_migrate(request, project_id):
    return schedule_project_command(request, project_id, "MIGRATE",
            "Successfully queued south migrate")

def startapp(request, project_id):
    # I feel like this belongs elsewhere
    project = get_object_or_404(Project, id=project_id)
    form = StartAppForm(request.POST or None)
    if form.is_valid():
        queue_job("STARTAPP", project_id=project_id, app_name=form.cleaned_data['app_name'])
        return redirect(project.get_absolute_url())
    return render_to_response("form.html", RequestContext(
        request, {'form': form}))

def edit_buildout(request, project_id):
    return schedule_project_command(request, project_id, "EDIT",
            "Successfully edited")


def schedule_project_command(request, project_id, command, success_message):
    project = get_object_or_404(Project, id=project_id)
    try:
        queue_job(command, project_id=project.id)
        return HttpResponse(success_message)
    except Exception as e:
        return HttpResponseServerError("Error: " + str(e))
