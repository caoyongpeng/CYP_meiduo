from django.core.mail import send_mail

from apps.users.utils import generic_active_email_url
from celery_tasks.main import app


@app.task
def send_active_email(user_id,email):
        subject = '美多商场激活邮件'

        message = ''

        from_email = '欢乐玩家<13464604691@163.com>'

        recipient_list = [email]
        active_url = generic_active_email_url(user_id,email)
        html_mesage = '<p>尊敬的用户您好！</p>' \
                        '<p>感谢您使用美多商城。</p>' \
                        '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                        '<p><a href="%s">%s<a></p>' % (email, active_url, active_url)

        send_mail(subject=subject,
                  message=message,
                  from_email=from_email,
                  recipient_list=recipient_list,
                  html_message=html_mesage)