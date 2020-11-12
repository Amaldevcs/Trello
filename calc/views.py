from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def  home(request):
	return render(request,'home.html',{'name':'Amal'})

def  login(request):
	content = request.FILES['file']
	alldata = content.read().decode("utf-8") 
	content_list = alldata.splitlines()
	content.close()
	return render(request,'login.html',{'name': content_list})

def  uploadlist(request):

	return render(request,'list_upload.html',{'name':'Amal'})