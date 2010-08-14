from django.shortcuts import render_to_response

def index(request):
    '''We should move this to a different app'''
    return render_to_response('index.html')
