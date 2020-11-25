from django.shortcuts import render
import time
import requests
# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect


completed_list = []
failed_list = []

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
	try:
		content = request.FILES['file']
		alldata = content.read().decode("utf-8") 
		content_list = alldata.splitlines()
		content.close()
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
				return HttpResponseRedirect("/failed")
			completed_list.append(i)
		return HttpResponseRedirect("/complete")
	except:
		return HttpResponseRedirect("/wrong")


def  uploadcard(request):
	global failed_list,completed_list
	completed_list = []
	failed_list = []
	try:
		content = request.FILES['file']
		alldata = content.read().decode("utf-8") 
		content_list = alldata.splitlines()
		content.close()
		list_name = str(request.POST["listname"])
		shortlink = str(request.POST["shortlink"])
		card_name = str(request.POST["cardname"])
		# card_id = str(request.POST["cardid"])
		board_id = getboard_id(shortlink)
		list_id = getlist_id(board_id,list_name)
		card_id = getcard_id(list_id,card_name)
		for i in content_list:
			board_id = getboard_id(i)
			listidp = getlist_id(board_id,list_name)
			if listidp:
				cardresp = postcard(board_id,listidp,card_id)
				if cardresp.status_code != 200 :
					failed_list = [x for x in content_list if x not in completed_list]
					return HttpResponseRedirect("/failed")
				completed_list.append(i)
			else:
				pass
			
		return HttpResponseRedirect("/complete")
	except:
		return HttpResponseRedirect("/wrong")

def  deletelist(request):
	global failed_list,completed_list
	completed_list = []
	failed_list = []
	try:
		content = request.FILES['file']
		alldata = content.read().decode("utf-8") 
		content_list = alldata.splitlines()
		content.close()
		list_name = str(request.POST["listname"])
		# list_id = str(request.POST["listid"])
		for i in content_list:
			
			board_id = getboard_id(i)
			listiddel = getlist_id(board_id,list_name)
			if listiddel == None:
				pass
			else:
				url = "https://api.trello.com/1/lists/"+str(listiddel)+"/closed"
				querystring = {"key":"6f4a1f510eb5f2f66917c8d322ec3cb8","token":"8ed88f5844ec6a137a8614f9aa88994e5da4c146495275ee87ac1ead818c1a1f","value":"true"}
				response = requests.request("PUT",url,params=querystring)
				if response.status_code != 200 :
					failed_list = [x for x in content_list if x not in completed_list]
					return HttpResponseRedirect("/failed")
				completed_list.append(i)
		return HttpResponseRedirect("/success")
	except:
		return HttpResponseRedirect("/wrong")

def  deletecard(request):
	global failed_list,completed_list
	completed_list = []
	failed_list = []
	try:
		content = request.FILES['file']
		alldata = content.read().decode("utf-8") 
		content_list = alldata.splitlines()
		content.close()
		list_name = str(request.POST["listname"])
		card_name = str(request.POST["cardname"])
		# list_id = str(request.POST["listid"])
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
						return HttpResponseRedirect("/failed")
					completed_list.append(i)
				else:
					pass
		return HttpResponseRedirect("/success")
	except:
		return HttpResponseRedirect("/wrong")



def  uploadlistform(request):
	return render(request,'listupload.html',{'name':''})

def  uploadcardform(request):
	return render(request,'cardupload.html',{'name':''})

def  deletelistform(request):
	return render(request,'listdelete.html',{'name':''})

def  deletecardform(request):
	return render(request,'carddelete.html',{'name':''})


def getboard_id(shortlink):
    urlshrt = "https://trello.com/b/" + shortlink + ".json"
    querystring = {"key":"6f4a1f510eb5f2f66917c8d322ec3cb8","token":"8ed88f5844ec6a137a8614f9aa88994e5da4c146495275ee87ac1ead818c1a1f"}
    response = requests.request("GET", urlshrt, params=querystring)
    return response.json()["id"]
 
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
	url = "http://peuat.mihyar.com:9090/ords/wsmhuat/collect/urls/"
	response = requests.request("GET", url)
	resp = (response.json())
	for i in resp['items']:
		i['ly']="http://koj.biz/"+str(i['ly'])
	return render(request,'urllist.html',{'resp':resp['items']})

def  createurl(request):
	url = "http://peuat.mihyar.com:9090/ords/wsmhuat/koj/urlshort"
	# response = requests.request("GET", url)
	# resp = (response.json())
	# for i in resp['items']:
	# 	i['ly']="http://koj.biz/"+str(i['ly'])
	return render(request,'createurl.html',{'resp':'AMAL'})
