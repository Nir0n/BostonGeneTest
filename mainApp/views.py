from django.views import View
from django.http import HttpResponse
from mainApp.models import Task
from django.core.files import File
from os.path import basename
from urllib.parse import urlsplit
import hashlib
from django.core.mail import EmailMessage
from threading import Thread
import requests
from tempfile import TemporaryFile

class Submit(View):
    def post(self, request):
        try:
            url = request.GET["url"]
            task = Task.objects.create(url=url,state="task in progress")
            try:
                task.email=request.GET["email"]
            except:
                pass
            thread=Thread(target=createTask,args=(task,))
            thread.daemon = True
            thread.start()
        except:
            task.state="task failed"
        task.save()
        param=[" id: ",task.id]
        return HttpResponse(param,status=200)

def createTask(task):
    try:
        downloadFile(task)
        task.md5 = getMd5(task.data)
        task.state = "complete"
        if task.email:
            email = EmailMessage(task.url, task.md5, to=[task.email])
            email.send()
    except:
        task.state="task failed"
    task.save()
    return 0

def downloadFile(task):
    with TemporaryFile() as tf:
        r = requests.get(task.url, stream=True)
        for chunk in r.iter_content(chunk_size=4096):
            tf.write(chunk)

        tf.seek(0)
        task.data.save(basename(urlsplit(task.url).path), File(tf))

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