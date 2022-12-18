from django.db import models
from sqlalchemy import false
from django.contrib import auth
from django.contrib.auth.models import User
    #一個物件test繼承於models裡面的Model


class Pname(models.Model):
    pName = models.CharField(max_length=20,null=True)
    



class product(models.Model):
	productID = models.AutoField(primary_key=True)
	storeName = models.CharField(max_length= 100)
	productName = models.CharField(max_length=100)
	productAddr = models.CharField(max_length=100)
	productType = models.CharField(max_length=100)
	productNum = models.CharField(max_length=100)
	productPrice = models.CharField(max_length=100)


	productImg = models.ImageField(upload_to='image/', blank=False, null=False)

class shoppingCart(models.Model):

	productID =  models.ForeignKey(product,on_delete=models.CASCADE,related_name="cart_productBuy")#foreugnKey 賦值直接給實例
	userID = models.ForeignKey(User,on_delete= models.CASCADE,related_name="cart_userBuy") #沒加%(class) 關聯名稱會重複
	amout = models.IntegerField(null=True)
	createdTime = models.DateTimeField(auto_now_add=True,null=True)
	updatedTime = models.DateTimeField(auto_now=True,null=True)

class userOeder(models.Model):
	productID =  models.ForeignKey(product,on_delete=models.CASCADE,related_name="order_productBuy")
	#userID = models.ForeignKey(User,on_delete= models.CASCADE,related_name="order_userBuy")



class OrderInfo(models.Model):

	status = (
		(1,"待付款"),
		(2,"待發貨"),
		(3,"待收貨"),
		(4,"已完成"),
	)
	orderID = models.CharField(max_length=100)
	orderAddr = models.CharField(max_length=100)
	orderBuy = models.CharField(max_length=100)
	orderPhone = models.CharField(max_length=12)
	orderFee = models.IntegerField(default=10)	
	orderExtra = models.CharField(max_length=200)
	orderStatus = models.IntegerField(default=1 , choices=status)

class OrderProduct(models.Model):
	productInfo = models.ForeignKey(product,on_delete=models.CASCADE , related_name="OrderToProduct")
	product_num = models.IntegerField()
	productOrder = models.ForeignKey(OrderInfo,on_delete=models.CASCADE ,related_name="orderToInfo" )
	productUserOrder = models.ForeignKey(User,on_delete= models.CASCADE,related_name="order_userBuy")


class Price(models.Model):
    
	CHOICES = [(-1,"全部顯示"),(1,"gtx1050"),(2,"gtx1060"),(3,"gtx1070"),(4,"gtx1080")]	
	pName_id = models.ForeignKey(Pname,on_delete=models.CASCADE,related_name="price")
	#pName = models.CharField(max_length=20,null=True)
	cName = models.CharField(max_length=100,null=True)#建立
	cPrice = models.IntegerField(null=True)
	cUrl = models.CharField(max_length=100,null=True)
	web_record = models.CharField(max_length=10,null=True)
	select_v = models.CharField(max_length=10,choices=CHOICES,null=True)
	created_at = models.DateTimeField(auto_now_add=True,null=True)
	updated_at = models.DateTimeField(auto_now=True,null=True)




