from django import forms
from http import HTTPStatus
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from abnormal_attack.models import AbnormalHost
from abnormal_attack.serializers import AbnormalHostSerializer
from response import CustomResponse, ERROR_CODES, ERROR_MESSAGES


# 对AbnormalHost表单进行检查
class AbnormalHostForm(forms.ModelForm):
    class Meta:
        model = AbnormalHost
        fields = '__all__'


# 批量查询和新增
class AbnormalHostListAPIView(APIView):
    # 设置分页类
    pagination_class = PageNumberPagination

    # 批量查询
    def get(self, request):
        try:
            content = request.GET.get('content')
            ip = request.GET.get('ip')
            sort = request.GET.get('sort', 'desc')  # 默认按升序排序
            page = request.GET.get('page', 1)  # 默认为第一页
            page_size = request.GET.get('limit', 10)  # 默认每页大小为10

            # 构建筛选条件
            filters = {}
            if content:
                filters['detail__icontains'] = content
            if ip:
                filters['ip'] = ip

            # 应用筛选条件
            abnormal_host = AbnormalHost.objects.filter(**filters)

            # 排序
            if sort.lower() == 'desc':
                abnormal_host = abnormal_host.order_by('-time')
            else:
                abnormal_host = abnormal_host.order_by('time')

            # 应用分页类进行分页
            paginator = self.pagination_class()
            paginator.page = int(page)
            paginator.page_size = int(page_size)
            result_page = paginator.paginate_queryset(
                abnormal_host, request)
            serializer = AbnormalHostSerializer(result_page, many=True)

            # 响应
            return CustomResponse(data={
                'count': abnormal_host.count(),
                'host': serializer.data,
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
        form = AbnormalHostForm(request.data)
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
class AbnormalHostDetailAPIView(APIView):
    # 根据id查询对应记录
    def get_object(self, id):
        try:
            return AbnormalHost.objects.get(id=id)
        except AbnormalHost.DoesNotExist:
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
            abnormal_host = self.get_object(id)
            serializer = AbnormalHostSerializer(abnormal_host)
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
            abnormal_host = self.get_object(id)
            # 校验数据
            form = AbnormalHostForm(request.data, instance=abnormal_host)
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
            id = request.GET.get('id')
            abnormal_host = self.get_object(id)
            abnormal_host.delete()
            return CustomResponse(status=204)
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )