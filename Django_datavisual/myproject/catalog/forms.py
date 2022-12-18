from django import forms
#從model 匯入 資料模型
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

'''
class StudentModelForm(forms.ModelForm):
    
    class Meta:
        model = test
        fields = ('cName','cSex','cBirthday','cEmail','cPhone','cAddr')
        #也可以fields = '__all__'
        可以使用 labels = {
            'name':'中文名',
            'price':'錢'}
            利用以上形式讓表單標題顯示自己要的label
'''


class PostForm(forms.Form):
    captcha = CaptchaField()






class uesr_GPUForm(forms.Form):
    CHOICES = [(-1,"全部顯示"),(1,"gtx1050"),(2,"gtx1060"),(3,"gtx1070"),(4,"gtx1080"),(5,"gtx1650"),(6,"gtx1660"),(7,"rtx2060"),(8,"rtx2070"),(9,"rtx2080")]	
    #"gtx1050","gtx1060","gtx1070","gtx1080,gtx1650,gtx1660,rtx2070,rtx2080"
    cName = forms.CharField(max_length=20,initial="",required=False)#建立
    #cPage = forms.CharField(max_length=10 ,required=True)
    choice_test = forms.CharField(max_length=10, required=False,widget = forms.widgets.Select(choices=CHOICES))

class productSearch(forms.Form):
    #"gtx1050","gtx1060","gtx1070","gtx1080,gtx1650,gtx1660,rtx2070,rtx2080"
    cName = forms.CharField(max_length=20,initial="",required=False)#建立
    storeName = forms.CharField(max_length=20 , initial="" , required= False) 
    #cPage = forms.CharField(max_length=10 ,required=True)

