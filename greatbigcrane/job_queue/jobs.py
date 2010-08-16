"""
Copyright 2010 Jason Chu, Dusty Phillips, and Phil Schalm

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os.path
import zmq
import json
import subprocess
from project.models import Project
from notifications.models import Notification
from buildout_manage.parser import buildout_parse

addr = 'tcp://127.0.0.1:5555'

# FIXME: I have no idea if this is threadsafe
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(addr)

def queue_job(command, **kwargs):
    '''Run the given command on the job queue, passing it any arguments as kwargs.'''
    assert command in command_map
    kwargs.update(command=command)
    serialized = json.dumps(kwargs)
    socket.send(serialized)
    assert socket.recv() == "ACK"

def command(command_name):
    "Decorator that marks a function as a queuable command."
    def wrap(function):
        command_map[command_name] = function
        return function
    return wrap

command_map = {}

# Create the actual commands here. Use command decorator to keep the map up to date
@command("BOOTSTRAP")
def bootstrap(project_id):
    '''Run the bootstrap process inside the given project's base directory.'''
    project = Project.objects.get(id=project_id)
    print("running bootstrap %s" % project.name)
    process = subprocess.Popen("python bootstrap.py", cwd=project.base_directory,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    response = process.communicate()[0]

    Notification.objects.create(status="success" if not process.returncode else "error",
            summary="Bootstrapping '%s' %s" % (
                project.name, "success" if not process.returncode else "error"),
            message=response,
            project=project)

@command("BUILDOUT")
def buildout(project_id):
    """Run the buildout process in the given project's base directory."""
    project = Project.objects.get(id=project_id)
    print("running buildout %s" % project.name)
    process = subprocess.Popen("bin/buildout", cwd=project.base_directory,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    response = process.communicate()[0]

    Notification.objects.create(status="success" if not process.returncode else "error",
            summary="Buildouting '%s' %s" % (
                project.name, "success" if not process.returncode else "error"),
            message=response,
            project=project)

@command("TEST")
def test_buildout(project_id):
    """Run the test command in the buildout project's base directory.
    Tries to do some intelligent guessing about how tests should be run."""
    project = Project.objects.get(id=project_id)
    print("running tests for %s" % project.name)

    bc = buildout_parse(project.buildout_filename())

    test_binaries = []

    parts = bc['buildout']['parts']
    if not isinstance(parts, list):
        parts = [parts]

    # We get to do some detection in this one
    # First look for django test
    for section, values in bc.iteritems():
        if section in parts:
            if values.get('recipe') == 'djangorecipe':
                # Django, we know what's going on
                if 'test' in values:
                    test_script = 'test'
                    if 'testrunner' in values:
                        test_script = values['testrunner']
                    test_binaries.append('bin/' + test_script)
                else:
                    test_script = section
                    if 'control-script' in values:
                        test_script = values['control-script']
                    test_binaries.append('bin/' + test_script + ' test')
            elif values.get('recipe') == 'zc.recipe.testrunner':
                test_script = section
                if 'script' in values:
                    test_script = values['control-script']
                test_binaries.append('bin/' + test_script)

    errors = False
    responses = []
    for binary in test_binaries:
        process = subprocess.Popen(binary, cwd=project.base_directory,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        responses.append(process.communicate()[0])
        errors = errors or process.returncode != 0

    # Make the output a little nicer when you run multiple test suites

    message = []
    for binary, response in zip(test_binaries, responses):
        test_command = ' '.join(binary)
        com_length = len(test_command)+1
        response_set = []
        response_set.append('='*com_length)
        response_set.append('\n')
        response_set.append(test_command)
        response_set.append(':')
        response_set.append('\n')
        response_set.append('='*com_length)
        response_set.append('\n')
        response_set.append(response)
        message.append(''.join(response_set))

    Notification.objects.create(status="success" if not errors else "error",
            summary="Testing '%s' %s" % (
                project.name, "success" if not errors else "error"),
            message=('\n\n'+'*'*50+'\n\n').join(message),
            project=project)
    project.test_status = not errors
    project.save()

@command("GITCLONE")
def clone_repo(project_id):
    """clone a git repo into the directory if it does not exist."""
    from greatbigcrane.job_queue.jobs import queue_job
    project = Project.objects.get(id=project_id)
    print("cloning repo for %s" % project.name)

    if os.path.exists(project.base_directory):
        Notification.objects.create(status="general",
                summary="Cloning '%s' %s" % (
                    project.name, "not necessary"),
                message="Repo not cloned because directory already exists",
                project=project)
    else:
        process = subprocess.Popen('git clone "%s" "%s"' % (project.git_repo, project.base_directory), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        response = process.communicate()[0]

        Notification.objects.create(status="success" if not process.returncode else "error",
                summary="Cloning '%s' %s" % (
                    project.name, "success" if not process.returncode else "error"),
                message=response,
                project=project)

    queue_job('BOOTSTRAP', project_id=project_id)

@command("GITPULL")
def pull_repo(project_id):
    """Run git pull in the base directory to update from the default origin"""
    project = Project.objects.get(id=project_id)
    print("pulling repo for %s" % project.name)

    process = subprocess.Popen('git pull', cwd=project.base_directory,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    response = process.communicate()[0]

    Notification.objects.create(status="success" if not process.returncode else "error",
            summary="Pulling '%s' %s" % (
                project.name, "success" if not process.returncode else "error"),
            message=response,
            project=project)

# Django commands
@command("SYNCDB")
def syncdb(project_id):
    """run django syncdb in the project directory"""
    project = Project.objects.get(id=project_id)
    print("running syncdb for %s" % project.name)

    process = subprocess.Popen('bin/django syncdb --noinput', cwd=project.base_directory,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    response = process.communicate()[0]

    Notification.objects.create(status="success" if not process.returncode else "error",
            summary="Syncdb '%s' %s" % (
                project.name, "success" if not process.returncode else "error"),
            message=response,
            project=project)

@command("STARTAPP")
def startapp(project_id, app_name):
    """Start a new app in the django project"""
    project = Project.objects.get(id=project_id)
    print("running startapp %s for %s" % (app_name, project.name))

    process = subprocess.Popen('bin/django startapp %s' % app_name,
            cwd=project.base_directory, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, shell=True)

    response = process.communicate()[0]

    Notification.objects.create(status="success" if not process.returncode else "error",
            summary="Startapp %s '%s' %s" % (
                app_name, project.name, "success" if not process.returncode else "error"),
            message=response,
            project=project)

@command("MIGRATE")
def migrate(project_id):
    """Run south migrate in the project directory."""
    project = Project.objects.get(id=project_id)
    print("running migrate for %s" % project.name)

    process = subprocess.Popen('bin/django migrate', cwd=project.base_directory,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    response = process.communicate()[0]

    Notification.objects.create(status="success" if not process.returncode else "error",
            summary="Migrate '%s' %s" % (
                project.name, "success" if not process.returncode else "error"),
            message=response,
            project=project)
