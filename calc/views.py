from django.shortcuts import render
import datetime
import requests,cx_Oracle,json
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

def  oracle(request):
	cx_Oracle.init_oracle_client(lib_dir=r'C:\Amal\instantclient_19_9')
	dsn_tns = cx_Oracle.makedsn('omsprod.c7cgvrmwurll.me-south-1.rds.amazonaws.com', '1521', service_name='omsprod')
	conn = cx_Oracle.connect(user='kojuser', password='koj$U$er#107',dsn=dsn_tns)
	c = conn.cursor()
	# c.execute('select 1 from dual') # use triple quotes if you want to spread your query across multiple lines
	c.execute("select * from omsproduser.koj_oms_custord oh, omsproduser.koj_oms_custord_item oi where oh.oms_order_id = oi.oms_order_id and oh.order_id in ('1252031558')");
	for row in c:
    		return render(request,'oracle.html',{'name':row})	

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
    	print("GDFHFHGFHGHGFHGHGHGF")
    	response = requests.request("GET", urlshrt, params=querystring)
    	print(response)
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
	url = "http://ords.kojtechservices.com:9090/ords/wsdigital/koj/list/"
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
	url = "http://ords.kojtechservices.com:9090/ords/wsdigital/koj/add/"
	shorturl = str(request.POST["shorturl"])
	longurl = str(request.POST["longurl"])
	createdby = str(request.POST["createdby"])
	# dt = datetime.datetime.now()
	# seq = int(dt.strftime("%Y%m%d%H%M%S"))
	querystring = {"ly":shorturl,"url":longurl,"created_by":createdby,"updated_by":createdby}
	headers = {'content-type': 'application/json'}
	response = requests.post(url, data=json.dumps(querystring),headers=headers)
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


def  cmsdata(request):
	output = naycmsdata(request)
	if output == 'sucess':
		missing = omsmissed(request)
	return render(request,'cmsdata.html',{'resp':missing})

def  naycmsdata(request):
	from_date = (datetime.datetime.now() - datetime.timedelta(hours = 24)).strftime("%d%m%Y")
	to_date = datetime.datetime.now().strftime("%d%m%Y")
	todate_mik = datetime.date.today()
	fromdate_mik = todate_mik - datetime.timedelta(days=1)
	cmslist = {
				"NAY" : ["https://cms.nayomi.com/index.php/rest/V1/app/dataextractionnew/orderlist?from="+from_date+"&to="+to_date,"q7fhtd4w5ysvzbsg8v86ydf6epnyhf2m","NAY"],
				"MHR" : ["https://cms.mihyar.com/index.php/rest//V1/app/dataextractionnew/orderlist/?from="+from_date+"&to="+to_date,"ij6yeko9mb9gv5u2wt4o0wqnuuhf6m0k","MHR"],
				"TBS" : ["https://cms-west.thebodyshop.com.sa/rest/V1/app/dataextractionnew/orderlist?from="+from_date+"&to="+to_date,"vbv8ehbgxp0lw9ocn0sleivythovkqvu","TBS"],
				"ELC" : ["https://cms.elctoys.com/index.php/rest/V1/app/dataextractionnew/orderlist/?from="+from_date+"&to="+to_date,"exn50dak2a5iahy02hawo5il0y6j25ct","ELC"],
				"MIK" : ["https://mikyajy.com/rest/V1/orderlist/?from="+str(fromdate_mik)+"&to="+str(todate_mik),"xat43fwtpxy11wjhns1tufevdb6tmfjc","MIK"]
				}
	for i in cmslist:
		try:
			headers = {'content-type': 'application/json',"Authorization": 'Bearer '+cmslist[i][1]}
			response = requests.get(cmslist[i][0],headers=headers)
			exstatus = ["ecom_cancelled","canceled","payment_pending","payfort_fort_failed"]
			orders = {key:val for key, val in response.json()[0].items() if val not in  exstatus}
			if response.json() :
				posturl = "http://ords.kojtechservices.com:9090/ords/wsdigital/cms/add/"
				querystring =  {  "line":str(tuple(orders.keys())),
								  "brand":cmslist[i][2]
							   }
				postresponse = requests.post(posturl, data=json.dumps(querystring),headers=headers)
		except:
			continue
	return "sucess"

def omsmissed(request):
	try:
		url = "http://ords.kojtechservices.com:9090/ords/wsdigital/cms/missed"
		headers = {'content-type': 'application/json'}
		missedresp= requests.get(url,headers=headers)
		missed = missedresp.json()["items"]
	except:
		return render(request,'cmsdata.html',{'resp':"Failed"})
	return missed


def  omsreport(request):
	dates = []
	from_date = (datetime.datetime.now()).strftime("%Y-%m-%d")
	to_date = datetime.datetime.now().strftime("%Y-%m-%d")
	if request.method =='GET':
		if 'startdate' in request.GET:
			from_date = request.GET['startdate']
			to_date = request.GET['todate']
			from_date_arr = str(request.GET['startdate']).split('-')
			to_date_arr = str(request.GET['todate']).split('-')
			from_date_qury = (datetime.datetime(int(from_date_arr[0]), int(from_date_arr[1]), int(from_date_arr[2]))).strftime('%d-%b-%Y')
			to_date_qury = (datetime.datetime(int(to_date_arr[0]), int(to_date_arr[1]), int(to_date_arr[2]))).strftime('%d-%b-%Y')
		else:
			from_date = (datetime.datetime.now()).strftime("%Y-%m-%d")
			to_date = datetime.datetime.now().strftime("%Y-%m-%d")
			from_date_qury = datetime.datetime.now().strftime('%d-%b-%Y')
			to_date_qury = from_date_qury
	dates.append(from_date)
	dates.append(to_date)
	try:
		# url = "http://ords.kojtechservices.com:9090/ords/wsdigital/cms/status"
		url = "http://ords.kojtechservices.com:9090/ords/wsdigital/cms/stat/"+str(from_date_qury)+"/"+str(to_date_qury)
		headers = {'content-type': 'application/json'}
		reportresp = requests.get(url,headers=headers)
		report = reportresp.json()["items"]
		status_codes = []
		outreport = []
		for i in report:
			if i["status_desc"] not in status_codes:
				status_codes.append(i["status_desc"])
				outreport.append({i["status_desc"] : [{"ELC":0},{"MHR":0},{"NAY":0},{"TBS":0},{"MIK":0}]})
		# for j in status_codes:
		for k in report:
			# if k["status_desc"] == j:
			for m in outreport:
				for key in m:
					if key == k["status_desc"]:
						for n in m[key]:
							for key in n:
								if key == k["brand_code"]:
									n[key] = k["count(order_id)"]
		dispreport = []
		for i in outreport:
				stausarr = []
				total = 0
				for p in i:
					stausarr.append(p)
					for k in i[p]:
						for m in k:
							stausarr.append(str(k[m]))
							total = total+k[m] 
					stausarr.append(str(total))
				dispreport.append(stausarr)
		grant_total = ['OMS ORDER COUNT',0,0,0,0,0,0]
		for arr in dispreport:
			for t in range(len(arr)):
				if t !=0:
					grant_total[t]= grant_total[t] + int(arr[t])
		# dispreport.insert(0, grant_total)
		dispreport.append(grant_total)
		dispreport.append(dates)
				
	except:
		return render(request,'cmsdata.html',{'resp':"failed"})
	return render(request,'omsreport.html',context={"resp": json.dumps(dispreport)})
