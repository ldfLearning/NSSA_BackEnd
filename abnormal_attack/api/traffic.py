from django import forms
from http import HTTPStatus
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from abnormal_attack.models import AbnormalTraffic
from abnormal_attack.serializers import AbnormalTrafficSerializer
from response import CustomResponse, ERROR_CODES, ERROR_MESSAGES


# 对AbnormalTraffic表单进行检查
class AbnormalTrafficForm(forms.ModelForm):
    class Meta:
        model = AbnormalTraffic
        fields = '__all__'

    def clean_type(self):
        type_value = self.cleaned_data['type']
        valid_types = [choice[0]
                       for choice in AbnormalTraffic.FLOW_TYPE_CHOICES]
        if type_value not in valid_types:
            raise forms.ValidationError('Invalid type value')
        return type_value


# 批量查询和新增
class AbnormalTrafficListAPIView(APIView):
    # 设置分页类
    pagination_class = PageNumberPagination

    # 批量查询
    def get(self, request):
        try:
            page = request.GET.get('page', 1)           # 默认为第一页
            page_size = request.GET.get('pageSize', 10) # 默认每页大小为10
            content = request.GET.get('content')        # 关键字查询（time,ip,detail）
            types = request.GET.getlist('type')         # 类型筛选
            sort = request.GET.get('sort', 0)           # 默认按升序排序
            

            # 构建筛选条件
            filters = Q()
            if content:
                filters |= Q(time__icontains=content)
                filters |= Q(src_ip__icontains=content)
                filters |= Q(dst_ip__icontains=content)
                filters |= Q(detail__icontains=content)

            if types:
                filters &= Q(type__in=types)
                

            # 应用筛选条件
            abnormal_traffic = AbnormalTraffic.objects.filter(filters)

            # 排序
            if sort == 0:
                abnormal_traffic = abnormal_traffic.order_by('-time')
            else:
                abnormal_traffic = abnormal_traffic.order_by('time')

            # 应用分页类进行分页
            paginator = self.pagination_class()
            paginator.page = int(page)
            paginator.page_size = int(page_size)
            result_page = paginator.paginate_queryset(
                abnormal_traffic, request)
            serializer = AbnormalTrafficSerializer(result_page, many=True)

            # 响应
            return CustomResponse(data={
                'count': abnormal_traffic.count(),
                'traffic': serializer.data,
            })
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

    # 新增
    def post(self, request):
        form = AbnormalTrafficForm(request.data)
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


# 查询、修改、删除
class AbnormalTrafficDetailAPIView(APIView):
    # 根据id查询对应记录
    def get_object(self, id):
        try:
            return AbnormalTraffic.objects.get(id=id)
        except AbnormalTraffic.DoesNotExist:
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
            abnormal_traffic = self.get_object(id)
            serializer = AbnormalTrafficSerializer(abnormal_traffic)
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
            abnormal_traffic = self.get_object(id)
            # 校验数据
            form = AbnormalTrafficForm(request.data, instance=abnormal_traffic)
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
            # serializer = AbnormalTrafficSerializer(
            #     abnormal_traffic, data=request.data)
            # if serializer.is_valid():
            #     serializer.save()
            #     return CustomResponse(data=serializer.data)
            # return CustomResponse(
            #     code=ERROR_CODES['INVALID_DATA'],
            #     msg=ERROR_MESSAGES['INVALID_DATA'],
            #     data=serializer.errors,
            #     status=HTTPStatus.INTERNAL_SERVER_ERROR

            # )
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
            # id = request.GET.get('id')
            # abnormal_traffic = self.get_object(id)
            # abnormal_traffic.delete()
            ids = request.GET.get('id')
            for id in ids.split(','):
                abnormal_traffic = self.get_object(id)
                abnormal_traffic.delete()
            return CustomResponse()
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
