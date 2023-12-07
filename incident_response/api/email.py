from http import HTTPStatus
from django import forms
from django.conf import settings
from response import CustomResponse, ERROR_CODES,ERROR_MESSAGES
from rest_framework.views import APIView
# from emergency_response.models import EmailSettings
# from emergency_response.serializers import EmailSettingsSerializer
# from .warning import AbnormalWarningForm
from incident_response.models import EmailSettings
from incident_response.serializers import EmailSettingsSerializer
from incident_response.api.warning import IncidentEventForm
from django.core.mail import send_mail
from email.utils import formataddr

# 对EmailSettings表单进行检查
class EmailSettingsForm(forms.ModelForm):
    class Meta:
        model = EmailSettings
        fields = '__all__'

class EmailSettingsAPIView(APIView):
    def post(self, request):
        try:
            # 修改设置或添加第一条数据
            email_settings, created = EmailSettings.objects.get_or_create()
            email_settings.email_recipient = request.data.get('email_recipient', email_settings.email_recipient)
            email_settings.email_subject = request.data.get('email_subject', email_settings.email_subject)
            email_settings.email_addresser_name = request.data.get('email_addresser_name', email_settings.email_addresser_name)
            email_settings.save()
            return CustomResponse()
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

# 测试邮件发送 
class EmailSendAPIView(APIView):
    def getEmailSettings(self):
        try:
            # 获取唯一的 EmailSettings 记录
            email_settings = EmailSettings.objects.get()
            return email_settings
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        
    def send_email_view(self,warning_msg):
        try:
          emailsetting = self.getEmailSettings()
          print(emailsetting)
          subject = emailsetting.email_subject #主题
          from_name = emailsetting.email_addresser_name  # 发件人显示
          from_email = settings.EMAIL_HOST_USER  # 发件人邮箱
          message = warning_msg
          recipient_list = [emailsetting.email_recipient]  # 收件人邮箱列表
          # 使用formataddr函数设置发件人名称和邮箱地址
          from_address = formataddr((from_name, from_email))
          send_mail(subject, message, from_address, recipient_list)
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

    def post(self,request):
        ip = request.data.get('ip')  
        time = request.data.get('time')  
        detail = request.data.get('detail')  

        form = IncidentEventForm(request.data)
        if form.is_valid():
            form.save()
            warning_msg = time+',  '+ip+'的机器正在遭遇威胁，详细情况如下：'+detail
            self.send_email_view(warning_msg)
            return CustomResponse()
        else:
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=ERROR_MESSAGES['INVALID_REQUEST'],
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )