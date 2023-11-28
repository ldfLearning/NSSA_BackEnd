from django.shortcuts import render
from django.db.models import Q
from http import HTTPStatus
from incident_response.models import IncidentEvent
from incident_response.serializers import IncidentEventSerializer
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from response import CustomResponse, ERROR_CODES, ERROR_MESSAGES

# Create your views here.

class IncidentEventListAPIView(APIView):
    # 设置分页类
    pagination_class = PageNumberPagination

    # 批量查询
    def get(self, request):
        try:
            # 提取参数
            page = request.GET.get('page', 1)           # 默认为第一页
            page_size = request.GET.get('pageSize', 10) # 默认每页大小为10
            finished = request.GET.get('finished', False) # 默认查找未读记录
            # 筛选查询
            filters = Q()
            if finished:
                filters &= Q(finished=finished)
            incident_event = IncidentEvent.objects.filter(filters)
            # 时间倒序
            incident_event = incident_event.order_by('time')
            # 分页
            paginator = self.pagination_class()
            paginator.page = int(page)
            paginator.page_size = int(page_size)
            result_page = paginator.paginate_queryset(
                incident_event, request)
            serializer = IncidentEventSerializer(result_page, many=True)
            # 响应
            return CustomResponse(data={
                'count': incident_event.count(),
                'events': serializer.data,
            })
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        
class IncidentEventDetailAPIView(APIView):
    # 根据id查询对应记录
    def get_object(self, id):
        try:
            return IncidentEvent.objects.get(id=id)
        except IncidentEvent.DoesNotExist:
            return CustomResponse(
                code=ERROR_CODES['NOT_FOUND'],
                msg=ERROR_MESSAGES['NOT_FOUND'],
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
    
    # 标记为已读
    def put(self, request):
        try:
            # 查询记录
            id = request.GET.get('id')
            incident_event = self.get_object(id)
            # 修改保存
            incident_event.finished = True
            incident_event.save()
            # 响应前端
            return CustomResponse()
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )