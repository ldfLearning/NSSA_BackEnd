import json
from django.core import serializers
# from drf_yasg import openapi
# from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from situation_events.utils import result, HttpCode
from django.db.models import Q
from situation_events.models import SituationEvent
from datetime import datetime

class SituationEventView(APIView):
    
    # @swagger_auto_schema(
    #     manual_parameters=[
    #         openapi.Parameter("page", openapi.IN_QUERY, description="第几页", type=openapi.TYPE_INTEGER),
    #         openapi.Parameter("pageSize", openapi.IN_QUERY, description="页面大小", type=openapi.TYPE_INTEGER),
    #         openapi.Parameter("keyword", openapi.IN_QUERY, description="关键字", type=openapi.TYPE_STRING),
    #         openapi.Parameter("beginTime", openapi.IN_QUERY, description="开始时间", type=openapi.TYPE_STRING),
    #         openapi.Parameter("endTime", openapi.IN_QUERY, description="结束时间", type=openapi.TYPE_STRING),
    #     ],
    #     operation_summary='分页查询',
    # )
    def get(self, request):
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('pageSize', 10))
        keyword = request.GET.get('keyword')
        try:
            begin_time = datetime.strptime(request.GET.get('beginTime'), "%Y-%m-%d %H:%M:%S")
        except:
            begin_time = datetime.strptime("0001-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        # print('end_time=', request.GET.get('endTime'))
        try:
            end_time = datetime.strptime(request.GET.get('endTime'), "%Y-%m-%d %H:%M:%S")
        except:
            end_time = datetime.now()
        start = (page - 1) * page_size
        end = page * page_size
        try:
            total = SituationEvent.objects.all().count()
            if page == 0:
                list_info = SituationEvent.objects.filter(
                    (Q(happened_at__gte=begin_time)) & (Q(happened_at__lte=end_time))
                )
                count = len(list_info)
                return result(HttpCode.ok, "查询成功", list(list_info.values()), total, count)
            if keyword:
                list_info = SituationEvent.objects.filter(
                    (Q(event_type__contains=keyword) | Q(event_info__contains=keyword))
                    & (Q(happened_at__gte=begin_time)) & (Q(happened_at__lte=end_time))
                    )[start:end]
                count = len(list_info)
            else:
                list_info = SituationEvent.objects.filter(
                    (Q(happened_at__gte=begin_time)) & (Q(happened_at__lte=end_time)))[start:end]
                count = len(list_info)
            return result(HttpCode.ok, "查询成功", json.loads(serializers.serialize("json", list_info)), total, count)
        except Exception as e:
            return result(HttpCode.error, "查询失败")
        
class SituationEventItemView(APIView):

    # @swagger_auto_schema(
    #     operation_summary='根据id查询',
    #     manual_parameters=[
    #         openapi.Parameter("id", openapi.IN_QUERY, description="id号", type=openapi.TYPE_INTEGER),
    #     ],
    # )
    def get(self, request):
        query = request.query_params.dict()
        query_id = query['id'] #单个id传入
        count = SituationEvent.objects.filter(id=query_id).count()

        if count == 0:
            return result(HttpCode.not_found, "数据不存在")
        else:
            item = SituationEvent.objects.filter(id=query_id)
            info = json.loads(serializers.serialize("json", list(item)))
            return result(HttpCode.ok, "查询成功", info)

    # @swagger_auto_schema(
    #     operation_summary='根据id列表删除',
    #     manual_parameters=[
    #         openapi.Parameter("id_list", openapi.IN_QUERY, description="id列表", type=openapi.TYPE_INTEGER),
    #     ],
    # )
    def delete(self, request):
        query = request.query_params.dict()
        delete_id_list = query['id_list'].split(',')
        
        for delete_id in delete_id_list:
            exit_id = SituationEvent.objects.filter(id=delete_id).count()
            if exit_id == 0:
                 return result(HttpCode.not_found, f"id为{exit_id}数据不存在")
            try:
                SituationEvent.objects.get(id=delete_id).delete()
            except Exception as e:
                print(e)
                return result(HttpCode.error, f"id为{exit_id}删除失败")

        return result(HttpCode.ok, "删除成功")

class SituationEventItemTypeView(APIView):

    # @swagger_auto_schema(
    #     operation_summary='根据类型查询',
    #     manual_parameters=[
    #         openapi.Parameter("event_type", openapi.IN_QUERY, description="event_type类型", type=openapi.TYPE_STRING),
    #     ],
    # )
    def get(self, request):
        query = request.query_params.dict()
        query_type = query['event_type']
        count = SituationEvent.objects.filter(event_type=query_type).count()

        if count == 0:
            return result(HttpCode.not_found, "数据不存在")
        else:
            item = SituationEvent.objects.filter(event_type=query_type)
            info = json.loads(serializers.serialize("json", list(item)))
            return result(HttpCode.ok, "查询成功", info)
