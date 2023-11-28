from http import HTTPStatus
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from response import CustomResponse, ERROR_CODES
#假设其他组的模型表已经建好
from abnormal_attack.models import AbnormalTraffic
import random 

class FlowAPIView(APIView):
    def post(self, request):
       try:
            random_numbers = [random.randint(0, 50) for _ in range(10)] 
            return CustomResponse(data=random_numbers)
       except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                data=[],
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
       
    def get(self, request):
        try:
            random_number = random.randint(0, 50)
            return CustomResponse(data=random_number)
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                data=[],
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )