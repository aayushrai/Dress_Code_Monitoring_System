from django.urls import path

from . import views
urlpatterns =[
    path("userdata",views.userData,name="userData"),
    path("productdata",views.productData,name="productData"),
    path("video",views.videoStream,name="videoStream"),
    path("loaddata",views.loadData,name="loadData"),
    path("placeorder",views.PlaceOrder,name="placeOrder"),
    path("adduser",views.AddUser,name="adduser"),
    path("order/<str:order_id>",views.orderInfo,name="orderInformation"),
    path("applydiscount",views.applyDiscount,name="applyDiscount"),
    path("detectedface",views.imagePublish,name="imagePublisher"),
    path("sendbill",views.SendBill,name="sendbill"),
    path("screenshot",views.ScreenShot,name="screenshot")
]
