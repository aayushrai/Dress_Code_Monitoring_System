from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http.response import StreamingHttpResponse
from .models import User,UserSerializer,Product,ProductSerializer,Order,OrderSerializer,Discount
from rest_framework.parsers import JSONParser
import uuid
import time
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import face_recognition
from imutils.video import VideoStream
import cv2,os
from keras.models import load_model

model = load_model("Api/assets/version2.h5")
# datetime object containing current date and time
now = datetime.now()
Face = None
counter = 0
face_dis_flag = False
result = []

@api_view(["GET"])
def userData(request):
	global result,counter
	if face_dis_flag:
		result =[]
		for name,idd,dis in sorted(zip(known_names,known_id,distance), key=lambda item: item[2]):
			if dis < .6:
				result.append(User.objects.get(user_id=idd))
	serilizeResult = UserSerializer(result,many=True)
	user_data = serilizeResult.data
	if counter:
		user_data = [
		{
			"user_name": "Unknown",
			"user_id": "",
			"user_address": "Unknown",
			"user_phone": "Unknown",
			"user_image": "/detectedface",
			"user_email": "Unknown",
		}
		] + user_data
	return Response(user_data)
	
@api_view(["POST"])
def ScreenShot(request):
	cv2.imwrite("media/detectedFace/face1.jpg",Face)
	return Response({"saved":"True"})

@api_view(["GET"])
def productData(request):
	result = Product.objects.all()
	productResult = ProductSerializer(result,many=True)
	return Response(productResult.data)

@api_view(["GET"])
def applyDiscount(request):
	emailDis = {}
	for discount in Discount.objects.all():
		if not discount.emailed:
			userMailed = []
			users = Order.objects.filter(product=discount.product)
			for user in users:
				if user.user_id not in userMailed:
					if user.user.user_email not in emailDis:
						if user.user.user_email:
							emailDis[user.user.user_email] = [discount]
					else:
						emailDis[user.user.user_email].append(discount)
					userMailed.append(user.user_id)
	try:
		sendDiscountMail(emailDis)	
	except Exception as e:
		print("Error while Sending DiscountEmail, may be you are not connected to internet!!!!!!")	
		print(e)	
			
	return Response({"discount":"Emailed"})
def discountEmailTemplate(discounts):
	product = ""
	for dis in discounts:
		product += """<tr>
		            <td class="bg_light email-section" style="padding: 0; width: 100%;">
		            	<table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
		            		<tr>
                      <td valign="middle" width="50%">
                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                          <tr>
                            <td class="text-services" style="text-align: left; padding: 20px 30px;">
                            	<div class="heading-section">
								              	<h2 style="font-size: 22px;">Name:"""+ dis.product.title +"""</h2>
								              	<p> Description:"""+ dis.product.description +"""</p>
								              	<p> Discount:"""+ str(dis.percent) +"""% OFF</p>
												<p> Original Price:"""+ str(dis.product.price) +"""</p>
												<p> Discount Price:"""+ str(dis.product.price - ((dis.product.price)*(dis.percent/100))) +"""</p>
								            	</div>
                            </td>
                          </tr>
                        </table>
                      </td>
                      <td valign="middle" width="50%">
                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                          <tr>
                            <td>
                              <img src='"""+ dis.product.logo +"""' alt="" style="width: 100%; max-width: 600px; height: auto; margin: auto; display: block;">
                            </td>
                          </tr>
                        </table>
                      </td>
                    </tr>
		            	</table>
		            </td>
		          </tr>"""
		  
	html = '''
	<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
    <meta charset="utf-8"> <!-- utf-8 works for most cases -->
    <meta name="viewport" content="width=device-width"> <!-- Forcing initial-scale shouldn't be necessary -->
    <meta http-equiv="X-UA-Compatible" content="IE=edge"> <!-- Use the latest (edge) version of IE rendering engine -->
    <meta name="x-apple-disable-message-reformatting">  <!-- Disable auto-scale in iOS 10 Mail entirely -->
    <title></title> <!-- The title tag shows in email notifications, like Android 4.4. -->

    <link href="https://fonts.googleapis.com/css?family=Lato:300,400,700" rel="stylesheet">

    <!-- CSS Reset : BEGIN -->
    <style>

        /* What it does: Remove spaces around the email design added by some email clients. */
        /* Beware: It can remove the padding / margin and add a background color to the compose a reply window. */
        html,
body {
    margin: 0 auto !important;
    padding: 0 !important;
    height: 100% !important;
    width: 100% !important;
    background: #f1f1f1;
}

/* What it does: Stops email clients resizing small text. */
* {
    -ms-text-size-adjust: 100%;
    -webkit-text-size-adjust: 100%;
}

/* What it does: Centers email on Android 4.4 */
div[style*="margin: 16px 0"] {
    margin: 0 !important;
}

/* What it does: Stops Outlook from adding extra spacing to tables. */
table,
td {
    mso-table-lspace: 0pt !important;
    mso-table-rspace: 0pt !important;
}

/* What it does: Fixes webkit padding issue. */
table {
    border-spacing: 0 !important;
    border-collapse: collapse !important;
    table-layout: fixed !important;
    margin: 0 auto !important;
}

/* What it does: Uses a better rendering method when resizing images in IE. */
img {
    -ms-interpolation-mode:bicubic;
}

/* What it does: Prevents Windows 10 Mail from underlining links despite inline CSS. Styles for underlined links should be inline. */
a {
    text-decoration: none;
}

/* What it does: A work-around for email clients meddling in triggered links. */
*[x-apple-data-detectors],  /* iOS */
.unstyle-auto-detected-links *,
.aBn {
    border-bottom: 0 !important;
    cursor: default !important;
    color: inherit !important;
    text-decoration: none !important;
    font-size: inherit !important;
    font-family: inherit !important;
    font-weight: inherit !important;
    line-height: inherit !important;
}

/* What it does: Prevents Gmail from displaying a download button on large, non-linked images. */
.a6S {
    display: none !important;
    opacity: 0.01 !important;
}

/* What it does: Prevents Gmail from changing the text color in conversation threads. */
.im {
    color: inherit !important;
}

/* If the above doesn't work, add a .g-img class to any image in question. */
img.g-img + div {
    display: none !important;
}

/* What it does: Removes right gutter in Gmail iOS app: https://github.com/TedGoas/Cerberus/issues/89  */
/* Create one of these media queries for each additional viewport size you'd like to fix */

/* iPhone 4, 4S, 5, 5S, 5C, and 5SE */
@media only screen and (min-device-width: 320px) and (max-device-width: 374px) {
    u ~ div .email-container {
        min-width: 320px !important;
    }
}
/* iPhone 6, 6S, 7, 8, and X */
@media only screen and (min-device-width: 375px) and (max-device-width: 413px) {
    u ~ div .email-container {
        min-width: 375px !important;
    }
}
/* iPhone 6+, 7+, and 8+ */
@media only screen and (min-device-width: 414px) {
    u ~ div .email-container {
        min-width: 414px !important;
    }
}

    </style>

    <!-- CSS Reset : END -->

    <!-- Progressive Enhancements : BEGIN -->
    <style>

	    .primary{
	background: #f85e9f;
}
.bg_white{
	background: #ffffff;
}
.bg_light{
	background: #fafafa;
}
.bg_black{
	background: #000000;
}
.bg_dark{
	background: rgba(0,0,0,.8);
}
.email-section{
	padding:2.5em;
}


h1,h2,h3,h4,h5,h6{
	font-family: 'Lato', sans-serif;
	color: #000000;
	margin-top: 0;
	font-weight: 400;
}

body{
	font-family: 'Lato', sans-serif;
	font-weight: 400;
	font-size: 15px;
	line-height: 1.8;
	color: rgba(0,0,0,.4);
}

a{
	color: #f85e9f;
}

table{
}
/*LOGO*/

.logo h1{
	margin: 0;
}
.logo h1 a{
	color: #000000;
	font-size: 20px;
	font-weight: 700;
	text-transform: uppercase;
	font-family: 'Lato', sans-serif;
	border: 2px solid #000;
	padding: .2em 1em;
}

.hero{
	position: relative;
	z-index: 0;
}

.hero .text{
	color: rgba(0,0,0,.3);
}
.hero .text h2{
	color: #000;
	font-size: 30px;
	margin-bottom: 0;
	font-weight: 300;
}
.hero .text h2 span{
	font-weight: 600;
	color: #f85e9f;
}




ul.social{
	padding: 0;
}
ul.social li{
	display: inline-block;
	margin-right: 10px;
}


@media screen and (max-width: 500px) {


}


    </style>


</head>

<body width="100%" style="margin: 0; padding: 0 !important; mso-line-height-rule: exactly; background-color: #222222;">
	<center style="width: 100%; background-color: #f1f1f1;">
    <div style="display: none; font-size: 1px;max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all; font-family: sans-serif;">
      &zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;
    </div>
    <div style="max-width: 600px; margin: 0 auto;" class="email-container">
    	<!-- BEGIN BODY -->
      <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: auto;">
      	<tr>
          <td valign="top" class="bg_white" style="padding: 1em 2.5em 0 2.5em;">
          	<table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
          		<tr>
          			<td class="logo" style="text-align: center;">
			            <h1><a href="#">WE MEGA MART</a></h1>
			          </td>
          		</tr>
          	</table>
          </td>
	
				<tr>
          <td valign="middle" class="hero hero-2 bg_white" style="padding: 2em 0 4em 0;">
            <table>
            	<tr>
            		<td>
            			<div class="text" style="padding: 0 2.5em; text-align: center;">
            				<h2>Available Offers <span>Prices</span> &amp; <span>Discount</span></h2>
            			</div>
            		</td>
            	</tr>
            </table>
          </td>
	      </tr><!-- end tr -->
	      <tr>
		      <td class="bg_white">
		        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
		          '''+ product +'''
		       
		        </table>
		      </td>
		    </tr><!-- end:tr -->
      </table>

    </div>
  </center>
</body>
</html>
	'''
	return html


def sendDiscountMail(emailDis):
	sender_email = "dummy21072000@gmail.com"
	password = "fel!zSuen0"
	message = MIMEMultipart("alternative")
	message["Subject"] = "WE MEGA MART DISCOUNT"
	message["From"] = sender_email
	
	context = ssl.create_default_context()
	if len(emailDis)>0:
		with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
				print("Sending emails")
				for receiver_email in emailDis:
					try:
						text = "Discount"
						html = discountEmailTemplate(emailDis[receiver_email])
						part1 = MIMEText(text, "plain")
						part2 = MIMEText(html, "html")
						message.attach(part1)
						message.attach(part2)
						server.login(sender_email, password)
						message["To"] = receiver_email
						server.sendmail(sender_email, receiver_email, message.as_string())
					except Exception as e:
						print(e)
						print("Not able to send email to ",receiver_email)
				for discount in Discount.objects.all():
					discount.emailed = True
					discount.save()	
def emailTemplate(orderInfo,order_count):
	product = ""
	total = 0
	discount = 0
		
	for order in orderInfo:
		total += order.product.price * (order.product_quantity)
		product += """ <tr>
            <td class="service">{}</td>
            <td class="desc">{}</td>
            <td class="unit">{}</td>
            <td class="qty">{}</td>
            <td class="total">{}</td>
          </tr>""".format(order.product.title,order.product.description,order.product.price,order.product_quantity,order.product.price * (order.product_quantity))
	
	if order_count%10==0:
		discount = int(total*0.05)

	html = '''
	<!DOCTYPE html>
	<html lang="en">
    <head>
    <meta charset="utf-8">
    <title>Example 1</title>
    <link rel="stylesheet" href="style.css" media="all" />
	<style>
		a {
			color: #5D6975;
			text-decoration: underline;
		}

		body {
		position: relative;
		width: 21cm;  
		height: 29.7cm; 
		margin: 0 auto; 
		color: #001028;
		background: #FFFFFF; 
		font-family: Arial, sans-serif; 
		font-size: 12px; 
		font-family: Arial;
		}

		header {
		padding: 10px 0;
		margin-bottom: 30px;
		}

		#logo {
		text-align: center;
		margin-bottom: 10px;
		}

		#logo img {
		width: 90px;
		}

	h1 {
	border-top: 1px solid  #5D6975;
	border-bottom: 1px solid  #5D6975;
	color: #5D6975;
	font-size: 2.4em;
	line-height: 1.4em;
	font-weight: normal;
	text-align: center;
	margin: 0 0 20px 0;
	background: url(dimension.png);
	}

	#project {
	float: left;
	}

	#project span {
	color: #5D6975;
	text-align: right;
	width: 52px;
	margin-right: 10px;
	display: inline-block;
	font-size: 0.8em;
	}

	#company {
	float: right;
	text-align: right;
	}

	#project div,
	#company div {
	white-space: nowrap;        
	}

table {
  width: 100%;
  border-collapse: collapse;
  border-spacing: 0;
  margin-bottom: 20px;
}

table tr:nth-child(2n-1) td {
  background: #F5F5F5;
}

table th,table td {
  text-align: center;
}

table th {
  padding: 5px 20px;
  color: #5D6975;
  border-bottom: 1px solid #C1CED9;
  white-space: nowrap;        
  font-weight: normal;
}

table .service,table .desc {
  text-align: left;
}

table td {
  padding: 20px;
  text-align: right;
}

table td.service,
table td.desc {
  vertical-align: top;
}

table td.unit,table td.qty,table td.total {
  font-size: 1.2em;
}

table td.grand {
  border-top: 1px solid #5D6975;;
}

footer {
  color: #5D6975;
  width: 100%;
  height: 30px;
  position: absolute;
  bottom: 0;
  border-top: 1px solid #C1CED9;
  padding: 8px 0;
  text-align: center;
}
	</style>
  </head>
	<body>
		<header class="clearfix">
		<h1>INVOICE</h1>
		<div id="company" class="clearfix">
			<div>WE MEGA MART</div>
			<div><a href="dummy21072000@gmail.com">dummy21072000@gmail.com</a></div>
		</div>
		<div id="project">
			<div><span>Order ID </span>'''+ orderInfo[0].order_id+'''</div>
			<div><span>CLIENT</span> '''+orderInfo[0].user.user_name +'''</div>
			<div><span>ADDRESS</span> '''+orderInfo[0].user.user_address +'''</div>
			<div><span>EMAIL</span> '''+orderInfo[0].user.user_email +'''</div>
			<div><span>DATE</span>'''+ now.strftime("%d/%m/%Y %H:%M:%S") +'''</div>
		</div>
		</header>
		<main>
			<table>
				<thead>
					<tr>
						<th class="service">PRODUCT NAME</th>
						<th class="desc">DESCRIPTION</th>
						<th>PRICE</th>
						<th>QTY</th>
						<th>TOTAL</th>
					</tr>
				</thead>
				<tbody>
					'''+product+'''
					<tr>
						<td colspan="4" class="grand total">TOTAL</td>
						<td class="grand total"> '''+ str(total) +'''</td>
					</tr>
					<tr>
						<td colspan="4" class="grand total">DISCOUNT</td>
						<td class="grand total"> '''+ str(discount) +'''</td>
					</tr>
					<tr>
						<td colspan="4" class="grand total">GRAND TOTAL</td>
						<td class="grand total"> '''+ str(total-discount) +'''</td>
					</tr>
				</tbody>
			</table>
		</main>
		<footer>
		Invoice was created on a computer and is valid without the signature and seal.
		</footer>
	</body>
	</html>'''
	return html

#https://www.google.com/settings/security/lesssecureapps
def sendEmail(order_id):
	order_info = Order.objects.filter(order_id=order_id)
	user_info = order_info[0].user
	receiver_email = user_info.user_email
	sender_email = "dummy21072000@gmail.com"
	password = "fel!zSuen0"
	message = MIMEMultipart("alternative")
	message["Subject"] = "WE MEGA MART BILL"
	message["From"] = sender_email
	html = emailTemplate(order_info,user_info.order_count)
	text = "hloo"
	part1 = MIMEText(text, "plain")
	part2 = MIMEText(html, "html")

	message.attach(part1)
	message.attach(part2)
	context = ssl.create_default_context()
	if receiver_email:
		with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
				print("Sending emails")
				server.login(sender_email, password)
				message["To"] = receiver_email
				server.sendmail(sender_email, receiver_email, message.as_string())
	else:
		print("User has no email id in database!!!!!!!!!!")

@api_view(["POST"])
def PlaceOrder(request):
	order_details = request.data
	order_id = uuid.uuid4()
	orders = []
	for order in order_details:
		user = User.objects.get(user_id=order["user_id"])
		product = Product.objects.get(product_id=order["product_id"])
		#update quantity of product
		new_quantity = product.quantity - order["product_quantity"]
		if new_quantity < 0:
			product.quantity = 0
		else:
			product.quantity = new_quantity
		product.save()
		orders.append(
			Order(
				user=user,
				product=product,
				order_id=order_id,
				product_quantity=order["product_quantity"]
			)
		)
	user = User.objects.get(user_id=order_details[0]["user_id"])
	user.order_count = user.order_count + 1
	user.save()
	Order.objects.bulk_create(orders)
	return Response({"order_id":order_id})

@api_view(["POST"])
def SendBill(request):
	emailed = "True"
	order_id = request.data["order_id"]
	try:
		sendEmail(order_id)
	except Exception as e:
		emailed = "False"
		print("Error while sending email , may be you are not connected to internet or your email address is wrong")
		print("Error is : ",e)
	return Response({"emailed":emailed})


def imageGen():
	while True:
		global Face
		frame = Face.copy()
		ret,frame = cv2.imencode('.jpg', frame)
		frame = frame.tobytes()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def imagePublish(request):
    return StreamingHttpResponse(imageGen(),
                        content_type='multipart/x-mixed-replace; boundary=frame')
                    

@api_view(["POST"])
def AddUser(request):
	img = cv2.imread("media/detectedFace/face1.jpg")
	img_name = uuid.uuid4()
	path = str(img_name)+".jpg"
	cv2.imwrite("media/"+ path,img)
	user_details = request.data
	user = User.objects.create(user_name=user_details["user_name"],user_address=user_details["user_address"],user_phone=user_details["user_phone"],user_email=user_details["user_email"],user_image=path)
	user.save()
	return Response({"user_id":user.user_id})

@api_view(["GET"])
def orderInfo(request,order_id):
	order_info = Order.objects.filter(order_id=order_id)
	user_info = order_info[0].user
	result = []
	serilizeOrderInfo = OrderSerializer(order_info,many=True).data
	for order in serilizeOrderInfo:
		productDis = ProductSerializer(Product.objects.get(id=order["product"])).data
		dis = {} 	
		for key,value in order.items():
			dis[key] = value
		for key,value in productDis.items():
			dis[key] = value
		result.append(dis)
	serilizeUserInfo = UserSerializer(user_info)
	return Response([serilizeUserInfo.data] + result)

@api_view(["GET"])
def loadData(request):
	import pandas as pd
	df = pd.read_csv('Api/assets/customer.csv')
	products = []
	for i in range(len(df)):
		products.append(
			Product(
			title=df.iloc[i]["Product Name"],
			description=df.iloc[i]["Product details"],
			logo=df.iloc[i]["Image"],
			category=df.iloc[i]["Category"],
			price=df.iloc[i]["Price"][3:],
			weight=df.iloc[i]["Weight"],
			quantity=df.iloc[i]["Quantity"]
			
			)
		)
	Product.objects.bulk_create(products)
	return Response({"status":"Data loaded"})


def framesGenerator(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def videoStream(request):
    url = 0
    url = "https://192.168.67.206:8080/video"
    camera = VideoCamera(url)
    return StreamingHttpResponse(framesGenerator(camera),
                        content_type='multipart/x-mixed-replace; boundary=frame')
                    

#================================================FACE RECOGNITION PART===============================================================#



load_encodings = False
face_cascade = cv2.CascadeClassifier('Api/assets/haarcascade_frontalface_default.xml')

class VideoCamera():

	def __init__(self,url):
		global load_encodings
		self.url = url
		self.video=VideoStream(src=self.url).start()
		if not load_encodings:
			VideoCamera.update_encoding()
			load_encodings=True
	
	@staticmethod
	def update_encoding():
		global known_names,known_faces,net,known_id
		known_names=[]
		known_faces=[]
		known_id = []
		print("Loading Encoding")
		UNKNOWN_DIR = "Api/Faces/"
		# for name in os.listdir(UNKNOWN_DIR):
		# 	FOLDER = os.path.join(UNKNOWN_DIR, name)
		# 	for filename in os.listdir(FOLDER):
		users = User.objects.all()
		for user in users:
			image = face_recognition.load_image_file(user.user_image)
			
			location = []
			faces = face_cascade.detectMultiScale(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 1.05, 5)
			for (x,y,w,h) in faces:
				(startX, startY, endX, endY) = x,y,x+w,y+h
				if (startX + 5 < endX) and (startY + 5 < endY): 
						location.append((startY,endX,endY,startX))
			if len(location)>0:
				encoding = face_recognition.face_encodings(image, known_face_locations=location)[0]
				known_faces.append(encoding)
				known_names.append(user.user_name)
				known_id.append(user.user_id)
			else:
				print(name,": Face not found in image" )

	def __del__(self):
		self.video.stop()
    
	def face_detection(self,image):
		rects = []
	
		self.face_cascade = cv2.CascadeClassifier('Api/assets/haarcascade_frontalface_default.xml')
		faces = self.face_cascade.detectMultiScale(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 1.05, 5)
		for (x,y,w,h) in faces:
			(startX, startY, endX, endY) = x,y,x+w,y+h
			if (startX + 5 < endX) and (startY + 5 < endY): 
					rects.append((startY,endX,endY,startX))
		return rects

	
	def face_recog(self):
		global known_names,known_faces,Face,counter
		image = self.frame
		image2 = self.frame.copy()
		#locations = face_recognition.face_locations(image2, number_of_times_to_upsample=3,model="hog")
		rects = self.face_detection(image2)

		encodings = face_recognition.face_encodings(image2, rects)
		
		for face_encoding, face_location in zip(encodings, rects):
			(startY,endX,endY,startX) = face_location
			crop_image=image2[startY-40:endY+40,startX-40:endX+40,:]
			crop_image_H,crop_image_W,crop_image_C=crop_image.shape
			if crop_image_H>100 and crop_image_W>100:

				face_rect = self.face_detection(crop_image)
				if len(face_rect)==1:
					
					if counter%10==0:
						Face = crop_image
						cv2.imwrite("media/detectedFace/face.jpg",crop_image)
					counter += 1
					if counter > 500:
						counter = 1
					results = face_recognition.compare_faces(known_faces, face_encoding,tolerance=0.6)
					global distance,face_dis_flag
					distance = face_recognition.face_distance(known_faces,face_encoding)
					face_dis_flag = True
					match = None
					if True in results:
						match = known_names[results.index(True)]
						# print(f"Match Found:", {match})
					else:
						match = "Unknown"
			
				

					top_left = (face_location[3], face_location[0])
					bottom_right = (face_location[1], face_location[2])

					color = [0, 255, 0]

					cv2.rectangle(image, top_left, bottom_right, 1)

					top_left = (face_location[3], face_location[0])
					bottom_right = (face_location[1], face_location[2])

					cv2.rectangle(image, top_left, bottom_right,(0,0,255),2)
					cv2.putText(image, match, (face_location[3], face_location[2]+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

	def dressCode(self):
		x1,y1,x2,y2 = 200,10,440,470
		h = 300
		w = 150
		cv2.rectangle(self.frame, (x1,y1), (x2,y2),(0,0,255),2)
		img = self.frame[y1:y2,x1:x2,:]
		img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		img = cv2.resize(img,(w,h))
		pred = model.predict(img.reshape(1,h,w,1))
		clas = model.predict_classes(img.reshape(1,h,w,1))
		label= ["Formal","Informal"]
		cv2.putText(self.frame,"Prediction: "+str(label[clas[0]]),(10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
		cv2.putText(self.frame,"Probability of formal: "+str(pred[0][0]),(10,70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
		cv2.putText(self.frame,"Probability of informal: "+str(pred[0][1]),(10,120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
	def get_frame(self):
		self.frame = self.video.read()
		
		if self.frame.shape:
			self.face_recog()
			self.dressCode()
		ret, jpeg = cv2.imencode('.jpg', self.frame)
		return jpeg.tobytes()
