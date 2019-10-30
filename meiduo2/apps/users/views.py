import json

import re

from django.http import HttpResponseForbidden
from django.http import JsonResponse,HttpResponse,HttpResponseBadRequest
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from apps.users.models import User, Address
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.contrib.auth.mixins import LoginRequiredMixin

from utils.response_code import RETCODE


class RegisterView(View):
    def get(self,request):
        return render(request,'register.html')
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')

        if not all([username,password,password2,mobile]):
            return HttpResponseBadRequest('参数不全')
        import re

        if not re.match(r'[a-zA-Z0-9]{5,20}', username):
            return HttpResponseBadRequest('用户名错误')
        if not re.match(r'[a-zA-Z0-9]{8,20}', password):
            return HttpResponseBadRequest('密码不符合规则')
        if password2 != password:
            return HttpResponseBadRequest('密码不一致')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('手机号错误')

        user = User.objects.create_user(username=username,password=password,mobile=mobile)



        login(request,user)

        response = redirect(reverse('contents:index'))
        response.set_cookie('username',user.username,max_age=3600)
        return response

class RegisterCountView(View):
    def get(self,request,username):
        count = User.objects.filter(username=username).count()
        return JsonResponse({'count':count})

class LoginView(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        remembered = request.POST.get('remembered')

        if not all([username,password]):
            return HttpResponseBadRequest('参数错误')
        user = authenticate(username=username,password=password)
        if user is None:
            return HttpResponseBadRequest('用户名或密码错误')
        login(request,user)
        if remembered == 'on':
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)

        response = redirect(reverse('contents:index'))

        response.set_cookie('username',user.username,max_age=3600)

        return response
class LogoutView(View):
    def get(self,request):
        logout(request)

        response = redirect(reverse('contents:index'))
        response.delete_cookie('username')
        return response
class UserCenterInfoView(LoginRequiredMixin,View):
    def get(self,request):
        context = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active,
        }

        return render(request,'user_center_info.html',context=context)
class EmailView(LoginRequiredMixin,View):

    def put(self,request):

        body=request.body
        body_str=body.decode()
        data=json.loads(body_str)

        email=data.get('email')
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            return JsonResponse({'code':RETCODE.PARAMERR,'errmsg':'邮箱不符合规则'})

        request.user.email=email
        request.user.save()

        from django.core.mail import send_mail


        subject='美多商场激活邮件'

        message=''

        from_email = '欢乐玩家<13464604691@163.com>'

        recipient_list = [email]

        html_mesage="<a href='http://www.meiduo.site:8000/emailsactive/?id=%s&email=%s'>戳我有惊喜</a>"%(request.user.id,email)

        send_mail(subject=subject,
                  message=message,
                  from_email=from_email,
                  recipient_list=recipient_list,
                  html_message=html_mesage)

        return JsonResponse({'code':RETCODE.OK,'errmsg':'ok'})

class EmailActiveView(View):
    def get(self,request):


        id = request.GET.get('id')
        email = request.GET.get('email')

        user = User.objects.get(id = id,email = email)

        if user is None:
            return HttpResponseBadRequest('验证失败')
        user.email_active = True
        user.save()

        return redirect(reverse('users:center'))

class UserCenterSiteView(View):

    def get(self,request):

        return render(request,'user_center_site.html')

class CreateAddressView(LoginRequiredMixin, View):

    def post(self, request):

        count = request.user.addresses.count()
        if count >= 20:
            return JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '超过地址数量上限'})

        json_dict = json.loads(request.body.decode())
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return HttpResponseBadRequest('缺少必传参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('参数mobile有误')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return HttpResponseBadRequest('参数tel有误')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return HttpResponseBadRequest('参数email有误')

        try:
            address = Address.objects.create(
                user=request.user,
                title = receiver,
                receiver = receiver,
                province_id = province_id,
                city_id = city_id,
                district_id = district_id,
                place = place,
                mobile = mobile,
                tel = tel,
                email = email
            )

            if not request.user.default_address:
                request.user.default_address = address
                request.user.save()
        except Exception as e:

            return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '新增地址失败'})

        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        return JsonResponse({'code': RETCODE.OK, 'errmsg': '新增地址成功', 'address':address_dict})


class UpdateDestroyAddressView(LoginRequiredMixin, View):


    def put(self, request, address_id):

        json_dict = json.loads(request.body.decode())
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        # 校验参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return HttpResponseBadRequest('缺少必传参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('参数mobile有误')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return HttpResponseBadRequest('参数tel有误')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return HttpResponseBadRequest('参数email有误')

        try:
            Address.objects.filter(id=address_id).update(
                user = request.user,
                title = receiver,
                receiver = receiver,
                province_id = province_id,
                city_id = city_id,
                district_id = district_id,
                place = place,
                mobile = mobile,
                tel = tel,
                email = email
            )
        except Exception as e:

            return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '更新地址失败'})


        address = Address.objects.get(id=address_id)
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        return JsonResponse({'code': RETCODE.OK, 'errmsg': '更新地址成功', 'address': address_dict})

    def delete(self, request, address_id):

        try:

            address = Address.objects.get(id=address_id)

            address.is_deleted = True
            address.save()
        except Exception as e:

            return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '删除地址失败'})

        return JsonResponse({'code': RETCODE.OK, 'errmsg': '删除地址成功'})

class AddressView(LoginRequiredMixin, View):


    def get(self, request):

        login_user = request.user
        addresses = Address.objects.filter(user=login_user, is_deleted=False)

        address_dict_list = []
        for address in addresses:
            address_dict = {
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "province_id":address.province_id,
                "city": address.city.name,
                "city_id":address.city_id,
                "district": address.district.name,
                "district_id":address.district_id,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            }
            address_dict_list.append(address_dict)

        context = {
            'default_address_id': login_user.default_address_id,
            'addresses': address_dict_list,
        }

        return render(request, 'user_center_site.html', context=context)

class ChangePasswordView(LoginRequiredMixin, View):

    def get(self, request):

        return render(request, 'user_center_pass.html')

    def post(self, request):

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')

        if not all([old_password, new_password, new_password2]):
            return HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', new_password):
            return HttpResponseBadRequest('密码最少8位，最长20位')
        if new_password != new_password2:
            return HttpResponseBadRequest('两次输入的密码不一致')

        if not request.user.check_password(old_password):
            return render(request, 'user_center_pass.html', {'origin_password_errmsg':'原始密码错误'})

        try:
            request.user.set_password(new_password)
            request.user.save()

        except Exception as e:
            import logging
            logger = logging.getLogger('django')
            logger.error(e)
            return render(request, 'user_center_pass.html', {'change_password_errmsg': '修改密码失败'})

        logout(request)

        response = redirect(reverse('users:login'))

        response.delete_cookie('username')

        return response