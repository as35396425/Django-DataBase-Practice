from django.shortcuts import redirect, render
from django.http import HttpResponse

from soupsieve import select
from .forms import PostForm
# Create your views here.
from django.http  import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
import datetime
from .models import product
from catalog import models
from django.http import HttpResponse




from django.http import HttpResponse


from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.views.generic import ListView, DetailView 
from django.db import connection
from . import forms
# Create your views here.

from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views.generic.edit import FormView



def login(request):
        postform = PostForm(request.POST)
        if request.method == 'POST':
            
            if postform.is_valid():  #forms驗證通過
                name = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=name, password=password)
                if user is not None:
                    if user.is_active:
                        auth.login(request,user)
                        message = '登入成功！'
                        
                        return redirect('/login1/')
                        
                    else:
                        message = '帳號尚未啟用！'
                else:
                    message = '登入失敗！'
                    
            else:message = "請輸入驗證碼"
        if request.user.is_authenticated:
            message = "已經登入"
            return redirect('/login1/') 
            if request.method == 'POST':
            
                return redirect('/login1/') 
                
        return render(request, "login.html", locals())


     
     
def logout(request):
	auth.logout(request)
	return redirect('/login/')	

def addtest(request):
	if request.method == 'POST':
		name = request.POST['username']
		password = request.POST['password']
		email = request.POST["email"]
		first_name = request.POST["first_name"]
		last_name = request.POST["last_name"]	
		try:
			user=User.objects.get(username=name)
		except :
			user = None
		if user!=None:
			message = name + "帳號已存在"
		else:
			user=User.objects.create_user(name,email,password)
			user.first_name = first_name
			user.last_name = last_name
			user.is_staff=False	# 工作人員狀態
			user.save()
			return redirect('/login/')
	else:
		message = "請輸入註冊資訊"
	return render(request,'adduser.html',locals())






def resultProduct(request, productType =None ):



    #p_obj = Pname.objects.filter(pk = 1).first()
    #student = product.objects.all()
    cartCount = 0
    for k,v in request.COOKIES.items():
        if not (k.isdigit()):
            continue
        cartCount+=1

    cursor = connection.cursor()

    select_data = "SELECT DISTINCT productType FROM catalog_product "
    cursor.execute(select_data)
    #print(cursor.fetchall()) 
    zzz = cursor.fetchall()


    #total_type = product.objects.get(productType)
    #p_obj = Pname.objects.filter(pName = "gtx1050").first()
    #student = p_obj.price.all()    #price r elate_name
    post_form = forms.productSearch(data = request.POST)
    if request.user.is_authenticated:
        user_name=request.user.username
        
   # if request.method == "POST" and post_form.is_valid(): 
    if request.method == "POST" and post_form.is_valid():
        #post_form = forms.productSearch(data = request.POST)
            #模板那邊使用{{post_form.XXX}}來取得表單資料
        name = post_form.cleaned_data['cName']
        storeForm = post_form.cleaned_data['storeName']
        print(name)
        student = product.objects.filter( productName__contains = name ,storeName__contains =  storeForm )
        #student  = student.filter()

        request.session["productName"] = name
        request.session["storeName"] = storeForm



    else:
        #print("找到",request.session["productName"])
        if "productName" and "storeName" in request.session :
            student = product.objects.filter(productName__contains = request.session["productName"] ,storeName__contains = request.session["storeName" ] )
            print(1)
        elif "productName" in request.session :
            student = product.objects.filter(productName__contains = request.session["productName"] )
            print(2)
        elif "storeName" in request.session :
            student = product.objects.filter(storeName__contains = request.session["storeName" ])
            print(3)
        else:
            student = product.objects.all()

    if productType != None:
        student = product.objects.filter(productType = productType)
        if productType == "all":
            student = product.objects.all()
            if "productName" in request.session :
                del request.session["productName"]
            if "storeName" in request.session:
                del request.session["storeName"]
            return redirect("/login1/")


    paginator = Paginator(student,4)
    pageNumber = request.GET.get('page')
    try:
        page_obj = paginator.page(pageNumber)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage: #
        page_obj = paginator.page(paginator.num_pages)



    #return render(request,'producer.html',locals())
    return render(request,'producer.html',locals())




def addCart(request,pk=None):
    #productID = request.GET.get('pk','')
    productID = pk
    if(productID):

        prev_url = request.META['HTTP_REFERER']
        
        response = redirect(prev_url )
        goods_count = request.COOKIES.get(productID)
        if(goods_count):
            goods_count = int(goods_count)+1
        else :
            goods_count = 1
        response.set_cookie(productID,goods_count)

    return response
from  django.contrib.auth.decorators import login_required
#@login_required

def showCart(request):


    cart_goods_list = []
    
    cart_goods_count = 0
    cart_goods_money = 0

    '''顯示購物車頁面'''
    for productionID , productionNum in request.COOKIES.items():
        #判斷ID是否為數字 ->確定是否為商品的COOKIES
        if not  productionID.isdigit():
            continue
        cart_goods = product.objects.get(productID = productionID)
        cart_goods.Num = productionNum #數量(單)

        aGoodTotalPrice =  int(productionNum)* int(cart_goods.productPrice)
        cart_goods.total = aGoodTotalPrice #總金額(單)
        cart_goods_list.append(cart_goods)#把cookie相等的商品加入列表

        #總數量和金額 (全)
        cart_goods_count += int(productionNum)
        cart_goods_money += aGoodTotalPrice

    return render(request , 'cartPage.html' , locals())

def removeCart(request , pk = None):
    
    
    
    productID = pk
    if (productID ) :
        prev_url = request.META['HTTP_REFERER']
        response = redirect(prev_url)
        #取得上一頁url
        productCount = request.COOKIES.get(productID,'')
        #藉由是否獲取到cookies值，判別商品存在購物車
        if productCount:
            response.delete_cookie(productID)

    return response

@login_required
def place_order(request):
    '''提交訂單'''
    #需要購物車所有商品 數量 總價 運費 ...
    cart_goods_list = []
    cart_goods_count = 0
    cart_goods_money = 0
    for productID,productCount in request.COOKIES.items():
        if not productID.isdigit():
            continue
        cart_goods = product.objects.get(productID = productID)
        cart_goods.productNum = productCount  

        cart_goods.aGoodTotalPrice =  int(productCount )* int(cart_goods.productPrice)
        #單商品價格總計 
        cart_goods_list.append(cart_goods)

        cart_goods_count += int(productCount)

        cart_goods_money += cart_goods.aGoodTotalPrice
    
    return render(request,'placeOrder.html',locals())
import time

@login_required
def submit_order(request):
    oreder_info = models.OrderInfo()


    addr = request.POST['addr']
    buyer = request.POST['buy']
    phoneNum = request.POST['phone']
    #extra = request.POST['extra']

    oreder_info.orderAddr = addr
    oreder_info.orderBuy = buyer
    oreder_info.orderPhone = phoneNum
    #oreder_info.orderExtra = extra
    #order_info.orderUser = User.objects.get(username=Uid) //F.K賦予實例
    oreder_info.orderID =str( time.time()*1000) + str(int(time.process_time())  * 1000000)
    oreder_info.save()
    response = redirect("submit_success/%s" %oreder_info.orderID)


    for productID , productNum in request.COOKIES.items():
        if not productID.isdigit():
            continue
        product = models.product.objects.get(productID = productID)
        order_product = models.OrderProduct()
        order_product.productInfo = product
        order_product.product_num = productNum
        order_product.productOrder = oreder_info
        usermodel = User.objects.get(username=request.user.username)
        order_product.productUserOrder = usermodel
        order_product.save()
        response.delete_cookie(productID)

        
    return response
@login_required
def submit_success(request,pk = None):
    order_id = pk

    order_info = models.OrderInfo.objects.get(orderID = order_id)
    order_product_list = models.OrderProduct.objects.filter(productOrder = order_info)

    orderUser = User.objects.get(username = request.user.username)
    test = models.OrderProduct.objects.filter(productUserOrder  = orderUser)

    total_money = 0

    total_num = 0
    for product in order_product_list:
        product.total_money = int(product.productInfo.productPrice )* int(product.product_num)
        total_money+=product.total_money
        total_num+=product.product_num
    return render(request , 'success.html' , locals())

def searchUserOrder(request):


    orderUser = User.objects.get(username = request.user.username)
    order_product_list = models.OrderProduct.objects.filter(productUserOrder  = orderUser)
    orderIdList = []

    x=order_product_list .values('productOrder').distinct()
    print(x)
    for forderID in x:
        #print(orderID['productOrder'])
        productOrderID=models.OrderInfo.objects.filter(id = forderID['productOrder'])
        orderIdList.append(*productOrderID)
    print(orderIdList)

    total_money = 0
    
    total_num = 0
    for product in order_product_list:
        product.productOrder.orderID
        product.total_money = int(product.productInfo.productPrice )* int(product.product_num)
        total_money+=product.total_money
        total_num+=product.product_num
    


    return render(request , 'UserOrder.html' , locals())


class BooksListView(ListView,FormView):
    model = product
    paginate_by = 10
    form_class = forms.productSearch
    success_url = r'http://127.0.0.1:8000/login12/'
    
    good = product.objects.all() 


    def categories(self):
            
        cursor = connection.cursor()

        select_data = "SELECT DISTINCT productType FROM catalog_product "
        cursor.execute(select_data)
        #print(cursor.fetchall()) 
        zzz = cursor.fetchall()
        return zzz
    def food(self):
        
        return product.objects.all() 
    
    def get_queryset(self):
        query_set = super(BooksListView, self).get_queryset()
        #print(query_set)
        category = self.kwargs.get('productType')
        search = self.kwargs.get('productName')
        print(category)
        if category:
            query_set = query_set.filter(productType =category)
            
        if search:
            query_set = query_set.filter(productName =search)
        
        return query_set
    def form_valid(self, form) -> HttpResponse:
        
        Kw = form.cleaned_data['cName']

        y = product.objects.filter( productName__contains = Kw)
        #print(student)
        #return self.render_to_response(self.get_context_data(form=self.form_class(initial=self.initial)))
        return super().form_valid(form)


book_list_view = BooksListView.as_view() 

from django.http import HttpResponseRedirect, Http404
import base64
import pickle

from django.http import JsonResponse


class FoodDetailview (DetailView):
    model = product

    def get(self, request, pk, *args, **kwargs,):
        try:
            print(request.COOKIES.get(pk),pk)#獲取COOKIES
            cookies = request.COOKIES.get(pk)
            prev_url = request.META['HTTP_REFERER']
            return super( FoodDetailview, self).get(self, request, pk=pk, *args, **kwargs)
        except Http404:
            return HttpResponseRedirect('/login1/')
    def post(self, request, pk, *args, **kwargs):

        return 
    def get_context_data(self,  *args, **kwargs):
        context = super().get_context_data(**kwargs)
        print(kwargs,2222)
        return context
    def dispatch(self, request, *args, **kwargs):
        cookies = request.COOKIES
        
        return super(FoodDetailview, self).dispatch(request, *args, **kwargs)


foodDetailview =  FoodDetailview.as_view()



#class CartView(TemplateView):
class FoodDetailview_T (DetailView):
    model = product

    def get(self, request, *args, **kwargs):
            product_id = self.kwargs.get('product_id', '')
            cart_str = request.COOKIES.get('cart', '')
            if product_id:
                if cart_str:
                    cart_bytes = cart_str.encode()
                    cart_bytes = base64.b64decode(cart_bytes)
                    cart_dict = pickle.loads(cart_bytes)
                else:
                    cart_dict = {}
                if product_id in cart_dict:
                    cart_dict[product_id]['count'] += 1
                else:
                    cart_dict[product_id] = {
                        'count': 1,
                    }
                cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
            context = {}
            context["status"] = 200
            response = JsonResponse(context)
            response.set_cookie("cart", cart_str)
            return response



