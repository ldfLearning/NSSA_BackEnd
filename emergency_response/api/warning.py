from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from emergency_response.serializers import AbnormalWarningSerializer
from ..tasks import monitor_warning
from ..models import AbnormalWarning

class WarningMonitorAPIView(APIView):
      def get(self, request):  
            res = {'code': 0, 'msg': '告警响应查询成功', 'data': []}
            try:
                warning_results = monitor_warning()
                res['data'] = warning_results
            except Exception as e:
                print(e)
                res['code'] = -1
                res['msg'] = '告警响应失败'
                return JsonResponse(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return JsonResponse(res)
      
class WarningListAPIView(APIView):
      # 设置分页类
      pagination_class = PageNumberPagination

      # 批量查询
      def get(self, request):
        try:
            content = request.GET.get('content')
            type = request.GET.get('type')
            ip = request.GET.get('ip')
            status = request.GET.get('status')
            sort = request.GET.get('sort', 'desc')  # 默认按升序排序
            page = request.GET.get('page', 1)  # 默认为第一页
            page_size = request.GET.get('limit', 10)  # 默认每页大小为10

            # 构建筛选条件
            filters = {}
            if content:
                filters['detail__icontains'] = content
            if type:
                filters['type'] = type
            if ip:
                filters['ip'] = ip
            if status:
                filters['status'] = status

            # 应用筛选条件
            abnormal_warning = AbnormalWarning.objects.filter(**filters)

            # 排序
            if sort.lower() == 'desc':
                abnormal_warning = abnormal_warning.order_by('-time')
            else:
                abnormal_warning = abnormal_warning.order_by('time')

            # 应用分页类进行分页
            paginator = self.pagination_class()
            paginator.page = int(page)
            paginator.page_size = int(page_size)
            result_page = paginator.paginate_queryset(
                abnormal_warning, request)
            serializer = AbnormalWarningSerializer(result_page, many=True)

            # 响应
            return JsonResponse(
                code=0,
                msg='查询成功',
                data={
                'count': abnormal_warning.count(),
                'warning': serializer.data,
            })
        except Exception as e:
            return JsonResponse(
                code=-1,
                msg=str(e),
                data={},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
