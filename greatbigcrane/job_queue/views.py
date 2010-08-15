from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseServerError
from project.models import Project
from job_queue.jobs import queue_job

def schedule_buildout(request, project_id):
    return schedule_project_command(request, project_id, "BUILDOUT",
            "Successuflly queued buildout")

def schedule_test(request, project_id):
    return schedule_project_command(request, project_id, "TEST",
            "Successuflly queued test")

def schedule_pull(request, project_id):
    return schedule_project_command(request, project_id, "GITPULL",
            "Successuflly queued git pull")

def schedule_syncdb(request, project_id):
    return schedule_project_command(request, project_id, "SYNCDB",
            "Successuflly queued syncdb")

def schedule_project_command(request, project_id, command, success_message):
    project = get_object_or_404(Project, id=project_id)
    try:
        queue_job(command, project_id=project.id)
        return HttpResponse(success_message)
    except Exception as e:
        return HttpResponseServerError("Error: " + str(e))
