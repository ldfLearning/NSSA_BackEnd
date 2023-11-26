from http import HTTPStatus
from django.conf import settings
from response import CustomResponse, ERROR_CODES
from rest_framework.views import APIView

class EmailUpdateAPIView(APIView):
     def post(self, request):  
         subject = request.data.get('subject')  # 邮件主题
         recipient = request.data.get('recipient')  # 收件人
         addresser_show = request.data.get('addresser_show')  # 发件人显示
         try:
            settings.EMAIL_RECIPIENT = recipient
            settings.EMAIL_SUBJECT_PREFIX = subject
            settings.EMAIL_ADDRESSER_SHOW = addresser_show
            print(settings.EMAIL_RECIPIENT)
            print(settings.EMAIL_SUBJECT_PREFIX)
            print(settings.EMAIL_ADDRESSER_SHOW)

            return CustomResponse()

         except Exception as e:
           return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
     
