import os
from django.views import View
from django.http import StreamingHttpResponse,HttpResponse
from mainApp.models import Task
from django.core.files import File
from os.path import basename
from urllib.request import urlretrieve, urlcleanup
from urllib.parse import urlsplit
import hashlib
from django.core.mail import EmailMessage

class Submit(View):
    def post(self, request):
        try:
            url = request.GET["url"]
            task = Task.objects.create(url=url,state="task in progress")
            try:
                task.email=request.GET["email"]
            except:
                pass

            downloadFile(task)
            task.md5=getMd5(task.data)
            task.state="complete"
            if task.email:
                email = EmailMessage(task.url, task.md5, to=[task.email])
                email.send()
        except Exception as exc:
            task.state="task failed"
        task.save()
        param=[" id: ",task.id]
        return HttpResponse(param,status=200)

def downloadFile(task):
    try:
        tempname, _ = urlretrieve(task.url)
        task.data.save(basename(urlsplit(task.url).path), File(open(tempname, 'rb')))
    finally:
        urlcleanup()

def getMd5(file):
    md5=hashlib.md5()
    with file as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    return md5.hexdigest()

class Check(View):
    def get(self, request):
        try:
            task_id= request.GET["id"]
            task=Task.objects.filter(pk=task_id).first()
            if task.state=="complete":
                param=[" state: ",task.state,", md5: ",task.md5,", url: ",task.url]
                return HttpResponse(param,status=200)
        except:
            return HttpResponse("Such id doesn't exist in the system",status=404)
        param=[" state: ",task.state]
        return HttpResponse(param,status=200)