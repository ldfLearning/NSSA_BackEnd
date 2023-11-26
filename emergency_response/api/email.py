from django.http import JsonResponse
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView

class EmailUpdateAPIView(APIView):
     def post(self, request):  
         res = {'code': 0, 'msg': '邮箱设置成功'}
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
         except Exception as e:
            print(e)
            res['code'] = -1
            res['msg'] = '邮箱设置失败'
            return JsonResponse(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

         return JsonResponse(res)
     
