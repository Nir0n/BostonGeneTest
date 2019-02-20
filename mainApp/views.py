import os
from django.views import View
from django.http import StreamingHttpResponse,HttpResponse
from mainApp.models import Task
from django.core.files import File
from os.path import basename
from urllib.request import urlretrieve, urlcleanup
from urllib.parse import urlsplit
import hashlib

class Submit(View):
    def post(self, request):
        try:
            url = request.GET["url"]
            task = Task.objects.create(url=url,state="task in progress")
            if request.GET["email"]:
                task.email=request.GET["email"]
            downloadFile(task)
            task.md5=getMd5(task.data)
            task.state="complete"
            sendEmail(task)
        except Exception as exc:
            task.state="task failed"
        task.save()
        return HttpResponse(task.id)

def downloadFile(task):
    try:
        tempname, _ = urlretrieve(task.url)
        task.data.save(basename(urlsplit(task.url).path), File(open(tempname, 'rb')))
    finally:
        urlcleanup()

    # file_full_path = "/tmp/{0}".format(filename)
    # response = StreamingHttpResponse((line for line in open(file_full_path, 'r')))
    # response['Content-Disposition'] = "attachment; filename={0}".format(filename)
    # response['Content-Length'] = os.path.getsize(file_full_path)
    # return response
    # req = requests.get(task.url, stream=True)
    # if req.status_code == 200:
    #     with open(path, 'wb') as f:
    #         for chunk in req.iter_content(chunk):
    #             f.write(chunk)
    #         f.close()
    #     return path
    # raise Exception('Given url is return status code:{}'.format(req.status_code))

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
            task=Task.objects.filter(id=task_id)
            if task.state=="complete":
                return HttpResponse(task.state,task.md5,task.url)
        except:
            raise Exception("Such id doesn't exist in the system")
        return HttpResponse(task.state)