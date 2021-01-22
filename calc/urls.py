from django.urls import path

from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('login', views.login,name="login"),
    path('logout', views.logout,name="logout"),
    path('uploadlist', views.uploadlist,name="uploadlist"),
    path('uploadcard', views.uploadcard,name="uploadcard"),
    path('deletelist', views.deletelist,name="deletelist"),
    path('deletecard', views.deletecard,name="deletecard"),
    path('complete', views.complete,name="complete"),
    path('success', views.success,name="success"),
    path('failed', views.failed,name="failed"),
    path('wrong', views.wrong,name="wrong"),
    path('upload_listform', views.uploadlistform,name="upload_listform"),
    path('upload_cardform', views.uploadcardform,name="upload_cardform"),
    path('delete_listform', views.deletelistform,name="delete_listform"),
    path('delete_cardform', views.deletecardform,name="delete_cardform"),
    path('urllist', views.urllist,name="urllist"),
    path('createurl', views.createurl,name="createurl"),
    path('posturl', views.posturl,name="posturl"),
    path('oracle', views.oracle,name="oracle"),
    path('cms', views.cmsdata,name="cms"),
    path('omsmissed', views.omsmissed,name="omsmissed"),
    path('omsreport', views.omsreport,name="omsreport")
]
