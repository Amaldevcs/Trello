from django.shortcuts import render
import datetime
import requests
# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import auth,User


# completed_list = []
# failed_list = []

def  home(request):
	return render(request,'home.html',{'name':'Amal'})

def  complete(request):
	global completed_list
	uploaded_list = completed_list
	# completed_list = []
	return render(request,'complete.html',{'uploaded_list':uploaded_list})

def  success(request):
	global completed_list
	uploaded_list = completed_list
	# completed_list = []
	return render(request,'success.html',{'uploaded_list':uploaded_list})

def  wrong(request):
	return render(request,'wrong.html',{'name':""})


def  failed(request):
	
	global failed_list
	failes = failed_list
	# failed_list = []
	return render(request,'failed.html',{'failed_list':failes})


def  uploadlist(request):

	global failed_list,completed_list
	completed_list = []
	failed_list = []
	if request.method == 'POST':
		request.session['failed']= []
		request.session['sucess']=[]
		try:
			content = request.FILES['file']
			alldata = content.read().decode("utf-8") 
			content_list = alldata.splitlines()
			content.close()
			content_list = list(filter(None, content_list))
			list_name = str(request.POST["listname"])
			# list_id = str(request.POST["listid"])
			shortlink = str(request.POST["shortlink"])
			board_id = getboard_id(shortlink)
			list_id = getlist_id(board_id,list_name)
			for i in content_list:

				board_id = getboard_id(i)
				postresp = postlist(board_id,list_name,list_id)
				if postresp.status_code != 200 :
					failed_list = [x for x in content_list if x not in completed_list]
					request.session['failed']=failed_list;
				if postresp.status_code ==200:
					completed_list.append(i)
					failed_list = [x for x in content_list if x not in completed_list]
					request.session['failed']=failed_list;

			request.session['sucess']=completed_list;
			return redirect("/uploadlist")
		except:
			return HttpResponseRedirect("/wrong")
	if request.method =='GET':
		failes=request.session.get('failed',False)
		sucess=request.session.get('sucess',False)
		if failes:
			return render(request,'failed.html',{'failed_list':failes})
		elif sucess:
			return render(request,'complete.html',{'uploaded_list':sucess})
		else:
			return HttpResponseRedirect("/upload_listform")
	


def  uploadcard(request):
	global failed_list,completed_list
	completed_list = []
	failed_list = []
	if request.method == 'POST':
		request.session['failed']= []
		request.session['sucess']=[]
		try:
			content = request.FILES['file']
			alldata = content.read().decode("utf-8") 
			content_list = alldata.splitlines()
			content.close()
			list_name = str(request.POST["listname"])
			shortlink = str(request.POST["shortlink"])
			card_name = str(request.POST["cardname"])
			# card_id = str(request.POST["cardid"])
			content_list = list(filter(None, content_list))
			board_id = getboard_id(shortlink)
			list_id = getlist_id(board_id,list_name)
			card_id = getcard_id(list_id,card_name)
			if card_id:
				for i in content_list:
					board_id = getboard_id(i)
					listidp = getlist_id(board_id,list_name)
					if listidp:
						cardresp = postcard(board_id,listidp,card_id)
						if cardresp.status_code != 200 :
							failed_list = [x for x in content_list if x not in completed_list]
							request.session['failed']=failed_list;
						if cardresp.status_code ==200:
							completed_list.append(i)
							failed_list = [x for x in content_list if x not in completed_list]
							request.session['failed']=failed_list;
						request.session['sucess']=completed_list;	
					else:
						pass
					
				return redirect(request.path)
			else:
				return HttpResponseRedirect("/wrong")
		except:
			return HttpResponseRedirect("/wrong")
	if request.method =='GET':
		failes=request.session.get('failed',False)
		sucess=request.session.get('sucess',False)
		if failes:
			return render(request,'failed.html',{'failed_list':failes})
		elif sucess:
			return render(request,'complete.html',{'uploaded_list':sucess})
		else:
			return HttpResponseRedirect("/uploadcard")

def  deletelist(request):
	global failed_list,completed_list
	completed_list = []
	failed_list = []
	if request.method == 'POST':
		request.session['failed']= []
		request.session['sucess']=[]
		try:
			content = request.FILES['file']
			alldata = content.read().decode("utf-8") 
			content_list = alldata.splitlines()
			content.close()
			list_name = str(request.POST["listname"])
			content_list = list(filter(None, content_list))
			# list_id = str(request.POST["listid"])
			for i in content_list:
				
				board_id = getboard_id(i)
				listiddel = getlist_id(board_id,list_name)
				if listiddel:
					url = "https://api.trello.com/1/lists/"+str(listiddel)+"/closed"
					querystring = {"key":"6f4a1f510eb5f2f66917c8d322ec3cb8","token":"8ed88f5844ec6a137a8614f9aa88994e5da4c146495275ee87ac1ead818c1a1f","value":"true"}
					response = requests.request("PUT",url,params=querystring)
					if response.status_code != 200 :
						failed_list = [x for x in content_list if x not in completed_list]
						request.session['failed']=failed_list;
					if response.status_code == 200 :
						completed_list.append(i)
						failed_list = [x for x in content_list if x not in completed_list]
						request.session['failed']=failed_list;
				else:
					pass
				request.session['sucess']=completed_list;
			if len(request.session['sucess']) == 0:
				return HttpResponseRedirect("/wrong")
			else:
				return redirect(request.path)
		except:
			return HttpResponseRedirect("/wrong")
	if request.method =='GET':
		failes=request.session.get('failed',False)
		sucess=request.session.get('sucess',False)
		if failes:
			return render(request,'failed.html',{'failed_list':failes})
		elif sucess:
			return render(request,'success.html',{'uploaded_list':sucess})
		else:
			return HttpResponseRedirect("/deletelist")


def  deletecard(request):
	global failed_list,completed_list
	completed_list = []
	failed_list = []
	if request.method == 'POST':
		request.session['failed']= []
		request.session['sucess']=[]
		try:
			content = request.FILES['file']
			alldata = content.read().decode("utf-8") 
			content_list = alldata.splitlines()
			content.close()
			list_name = str(request.POST["listname"])
			card_name = str(request.POST["cardname"])
			# list_id = str(request.POST["listid"])
			content_list = list(filter(None, content_list))
			for i in content_list:
				
				board_id = getboard_id(i)
				listiddel = getlist_id(board_id,list_name)
				if listiddel == None:
					pass
				else:
					card_id = getcard_id(listiddel,card_name)
					if card_id:
						querystring = {"key":"6f4a1f510eb5f2f66917c8d322ec3cb8","token":"8ed88f5844ec6a137a8614f9aa88994e5da4c146495275ee87ac1ead818c1a1f"}
						url = "https://api.trello.com/1/cards/" + card_id
						response = requests.request("DELETE",url,params=querystring)
						if response.status_code != 200 :
							failed_list = [x for x in content_list if x not in completed_list]
							request.session['failed']=failed_list;
						if response.status_code == 200 :
							completed_list.append(i)
							failed_list = [x for x in content_list if x not in completed_list]
							request.session['failed']=failed_list;
						request.session['sucess']=completed_list;
					else:
						pass
			if len(request.session['sucess']) == 0:
				return HttpResponseRedirect("/wrong")
			else:
				return redirect(request.path)
		except:
			return HttpResponseRedirect("/wrong")
	if request.method =='GET':
		failes=request.session.get('failed',False)
		sucess=request.session.get('sucess',False)
		if failes:
			return render(request,'failed.html',{'failed_list':failes})
		elif sucess:
			return render(request,'success.html',{'uploaded_list':sucess})
		else:
			return HttpResponseRedirect("/deletecard")




def  uploadlistform(request):
	if request.user.is_authenticated:
		for group in request.user.groups.all():
			if str(group) == 'Trello':
				return render(request,'listupload.html',{'name':''})
			
	else:
		return HttpResponseRedirect("/login")
		

def  uploadcardform(request):
	if request.user.is_authenticated:
		for group in request.user.groups.all():
			if str(group) == 'Trello':
				return render(request,'cardupload.html',{'name':''})
	else:
		return HttpResponseRedirect("/login")

		

def  deletelistform(request):
	if request.user.is_authenticated:
		for group in request.user.groups.all():
			if str(group) == 'Trello':
				return render(request,'listdelete.html',{'name':''})
	else:
		return HttpResponseRedirect("/login")

	

def  deletecardform(request):
	if request.user.is_authenticated:
		for group in request.user.groups.all():
			if str(group) == 'Trello' and request.user.is_authenticated:
				return render(request,'carddelete.html',{'name':''})
			else:
				return HttpResponseRedirect("/login")
	else:
		return HttpResponseRedirect("/login")

	


def getboard_id(shortlink):
    urlshrt = "https://trello.com/b/" + shortlink + ".json"
    querystring = {"key":"6f4a1f510eb5f2f66917c8d322ec3cb8","token":"8ed88f5844ec6a137a8614f9aa88994e5da4c146495275ee87ac1ead818c1a1f"}
    # response = requests.request("GET", urlshrt, params=querystring)
    try:
    	response = requests.request("GET", urlshrt, params=querystring)
    	return response.json()["id"]
    except:
    	return "123123"
 
def postlist(boardid,list_name,list_id):
    url = "https://api.trello.com/1/lists?name="+ str(list_name) +"&idBoard="+ boardid +"&idListSource="+ list_id +"&pos=top"
    # url = "https://api.trello.com/1/lists/"+ str(list_id) +"/idBoard"
    querystring = {"fields":"all","key":"6f4a1f510eb5f2f66917c8d322ec3cb8","token":"8ed88f5844ec6a137a8614f9aa88994e5da4c146495275ee87ac1ead818c1a1f"}
    # querystring = {"key":"6f4a1f510eb5f2f66917c8d322ec3cb8","token":"8ed88f5844ec6a137a8614f9aa88994e5da4c146495275ee87ac1ead818c1a1f","value":str(boardid)}
    response = requests.request("POST", url, params=querystring)
    # response = requests.request("PUT", url, params=querystring)
    return response

def getlist_id(lst,list_name):
	url = "https://api.trello.com/1/boards/"+lst+"/lists"
	querystring = {"fields":"all","key":"6f4a1f510eb5f2f66917c8d322ec3cb8","token":"8ed88f5844ec6a137a8614f9aa88994e5da4c146495275ee87ac1ead818c1a1f"}
	response = requests.request("GET", url, params=querystring)
	res = (response.json())
	for lis in res:
		lis_name = (lis["name"])
		if lis_name == list_name:
			target_list = (lis["id"])
			return(target_list)
		else:
			pass
def postcard(board_id,listidp,card_id):
    url = "https://api.trello.com/1/cards?idList="+str(listidp)+"&idBoard="+str(board_id)+"&idCardSource="+str(card_id)+"&pos=top"
    querystring = {"fields":"all","key":"6f4a1f510eb5f2f66917c8d322ec3cb8","token":"8ed88f5844ec6a137a8614f9aa88994e5da4c146495275ee87ac1ead818c1a1f"}
    response = requests.request("POST", url, params=querystring)
    return response

def getcard_id(list_id,card_name):
	url = "https://api.trello.com/1/lists/"+list_id+"/cards"
	querystring = {"key":"6f4a1f510eb5f2f66917c8d322ec3cb8","token":"8ed88f5844ec6a137a8614f9aa88994e5da4c146495275ee87ac1ead818c1a1f"}
	response = requests.request("GET", url, params=querystring)
	res = (response.json())
	for lis in res:
		if card_name == lis["name"]:
			target_list = (lis["id"])
			return(target_list)
		else:
			pass

def  urllist(request):
	url = "http://peuat.mihyar.com:9090/ords/wsmhprd/koj/list/"
	response = requests.request("GET", url)
	resp = (response.json())
	for i in resp['items']:
		i['ly']="http://koj.biz/"+str(i['ly'])
		i['delete'] = i ['id']
	return render(request,'urllist.html',{'resp':resp['items']})

def  createurl(request):
	if request.user.is_authenticated:
		for group in request.user.groups.all():
			if str(group) == 'Short URL':
				return render(request,'createurl.html',{'resp':''})
			
	else:
		return HttpResponseRedirect("/login")
	

def  posturl(request):
	url = "http://peuat.mihyar.com:9090/ords/wsmhprd/koj/add"
	shorturl = str(request.POST["shorturl"])
	longurl = str(request.POST["longurl"])
	createdby = str(request.POST["createdby"])
	# dt = datetime.datetime.now()
	# seq = int(dt.strftime("%Y%m%d%H%M%S"))
	querystring = {"ly":shorturl,"url":longurl,"created_by":createdby,"updated_by":createdby}
	response = requests.request("POST", url, params=querystring)
	return HttpResponseRedirect("/urllist")

def  login(request):
	if request.method == 'POST':
		username = request.POST["username"]
		password = request.POST["password"]
		user = auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request,user)
			return HttpResponseRedirect("/")
		else:
			messages.info(request,'Invalid Credentials')
			return HttpResponseRedirect("/login")
	else:
		return render(request,'login.html',{'resp':''})

def  logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/")
