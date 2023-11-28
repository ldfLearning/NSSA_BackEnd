from http import HTTPStatus
from django import forms
from response import CustomResponse, ERROR_CODES,ERROR_MESSAGES
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from emergency_response.serializers import AbnormalWarningSerializer
from ..models import AbnormalWarning

# 对AbnormalWarning表单进行检查
class AbnormalWarningForm(forms.ModelForm):
    class Meta:
        model = AbnormalWarning
        fields = '__all__'

    def clean_type(self):
        type_value = self.cleaned_data['type']
        valid_types = [choice[0]
                       for choice in AbnormalWarning.ABNORMAL_TYPE_CHOICES]
        if type_value not in valid_types:
            raise forms.ValidationError('Invalid type value')
        return type_value

class WarningMonitorAPIView(APIView):
      def monitor_warning(self):
        # 计算当前时间和2分钟前的时间
        end_time = timezone.now()
        print(end_time)
        start_time = end_time - timedelta(minutes=2)
        print(start_time)
        # 查询最近2分钟内的新入库数据
        recent_entries = AbnormalWarning.objects.filter(time__range=(start_time, end_time))
        
        warning_results = []
        warning_result = {}
        # 获取查询结果中的字段值
        for entry in recent_entries:
            warning_result['ip'] = entry.ip
            warning_result['detail'] = entry.detail
            warning_results.append(warning_result)

        return warning_results
      
      def get(self, request):  
            try:
                warning_results = self.monitor_warning()
                return CustomResponse(data=warning_results)
            
            except Exception as e:
                return CustomResponse(
                    code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                    msg=str(e),
                    data={},
                    status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
      
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
            return CustomResponse(
                data={
                'count': abnormal_warning.count(),
                'warning': serializer.data,
            })
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        
         # 新增
      
      #增加，可能不需要这个api
      def post(self, request):
            form = AbnormalWarningForm(request.data)
            if form.is_valid():
                form.save()
                return CustomResponse()
            else:
                return CustomResponse(
                    code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                    msg=ERROR_MESSAGES['INVALID_REQUEST'],
                    data={},
                    status=HTTPStatus.INTERNAL_SERVER_ERROR
                )

class WarningDetailAPIView(APIView):
      # 根据id查询对应记录
    def get_object(self, id):
        try:
            return AbnormalWarning.objects.get(id=id)
        except AbnormalWarning.DoesNotExist:
            return CustomResponse(
                code=ERROR_CODES['NOT_FOUND'],
                msg=ERROR_MESSAGES['NOT_FOUND'],
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

    # 查询记录
    def get(self, request):
        try:
            id = request.GET.get('id')
            abnormal_warning = self.get_object(id)
            serializer = AbnormalWarningSerializer(abnormal_warning)
            return CustomResponse(data=serializer.data)
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

    # 修改记录
    def put(self, request):
        try:
            # 查询记录
            id = request.GET.get('id')
            abnormal_warning = self.get_object(id)
            # 校验数据
            form = AbnormalWarningForm(request.data, instance=abnormal_warning)
            if form.is_valid():
                form.save()
                return CustomResponse(data=form.cleaned_data)
            else:
                return CustomResponse(
                    code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                    msg=ERROR_MESSAGES['INVALID_REQUEST'],
                    data={},
                    status=HTTPStatus.INTERNAL_SERVER_ERROR
                )
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

    # 删除记录
    def delete(self, request):
        try:
            id = request.GET.get('id')
            abnormal_warning = self.get_object(id)
            abnormal_warning.delete()
            return CustomResponse(status=204)
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )