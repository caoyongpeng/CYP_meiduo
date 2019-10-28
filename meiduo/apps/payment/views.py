from django.http import JsonResponse
from django.shortcuts import render

from django.views import View

from apps.orders.models import OrderInfo
from apps.payment.models import Payment
from utils.response_code import RETCODE


from django.contrib.auth.mixins import LoginRequiredMixin
class PaymentView(LoginRequiredMixin,View):

    def get(self,request,order_id):

        try:
            order=OrderInfo.objects.get(order_id=order_id,
                                        user=request.user,
                                        status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'])
        except OrderInfo.DoesNotExist:
            return JsonResponse({'code':RETCODE.NODATAERR,'errmsg':'没有此订单'})

        from alipay import AliPay
        from meiduo import settings

        app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
        alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()


        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",
            debug = settings.ALIPAY_DEBUG
        )
        subject = "测试订单"


        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.total_amount),
            subject=subject,
            return_url=settings.ALIPAY_RETURN_URL,
        )

        alipay_url=settings.ALIPAY_URL + '?' + order_string
        return JsonResponse({'code':RETCODE.OK,'errmsg':'ok','alipay_url':alipay_url})


class PaymentStatusView(View):

    def get(self,request):

        from alipay import AliPay
        from meiduo import settings

        app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
        alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()

        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",
            debug=settings.ALIPAY_DEBUG
        )


        data = request.GET.dict()

        signature = data.pop("sign")


        success = alipay.verify(data, signature)
        if success:
            trade_no=data.get('trade_no')
            out_trade_no=data.get('out_trade_no')

            Payment.objects.create(
                order_id=out_trade_no,
                trade_id=trade_no
            )

            OrderInfo.objects.filter(order_id=out_trade_no).update(status=OrderInfo.ORDER_STATUS_ENUM['UNSEND'])



        return render(request,'pay_success.html',context={'trade_no':trade_no})