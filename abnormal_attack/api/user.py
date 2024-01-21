from django import forms
from http import HTTPStatus
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from abnormal_attack.models import AbnormalUser
from abnormal_attack.serializers import AbnormalUserSerializer
from response import CustomResponse, ERROR_CODES, ERROR_MESSAGES

# 对AbnormalUser表单进行检查
class AbnormalUserForm(forms.ModelForm):
    class Meta:
        model = AbnormalUser
        fields = '__all__'

# 批量查询和新增
class AbnormalUserListAPIView(APIView):
    # 设置分页类
    pagination_class = PageNumberPagination

    # 批量查询
    def get(self, request):
        try:
            page = request.GET.get('page', 1)           # 默认为第一页
            page_size = request.GET.get('pageSize', 10) # 默认每页大小为10
            content = request.GET.get('content')        # 关键字查询（time,ip,detail）
            types = request.GET.getlist('type')              # 类型筛选
            sort = request.GET.get('sort', 0)           # 默认按升序排序

            # 构建筛选条件
            filters = Q()
            if content:
                filters |= Q(time__icontains=content)
                filters |= Q(user_name__icontains=content)
                filters |= Q(topic__icontains=content)
                filters |= Q(src_ip__icontains=content)
            if types:
                filters &= Q(type__in=types)

            # 应用筛选条件
            abnormal_user = AbnormalUser.objects.filter(filters)

            # 排序
            if sort == 0:
                abnormal_user = abnormal_user.order_by('-time')
            else:
                abnormal_user = abnormal_user.order_by('time')

            # 应用分页类进行分页
            paginator = self.pagination_class()
            paginator.page = int(page)
            paginator.page_size = int(page_size)
            result_page = paginator.paginate_queryset(
                abnormal_user, request)
            serializer = AbnormalUserSerializer(result_page, many=True)

            # 响应
            return CustomResponse(data={
                'count': abnormal_user.count(),
                'user': serializer.data,
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
        form = AbnormalUserForm(request.data)
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

# 查询、删除
class AbnormalUserDetailAPIView(APIView):
    # 根据id查询对应记录
    def get_object(self, id):
        try:
            return AbnormalUser.objects.get(id=id)
        except AbnormalUser.DoesNotExist:
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
            abnormal_user = self.get_object(id)
            serializer = AbnormalUserSerializer(abnormal_user)
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
            abnormal_user = self.get_object(id)
            # 校验数据
            form = AbnormalUserForm(request.data, instance=abnormal_user)
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
            # serializer = AbnormalUserSerializer(
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
            # abnormal_user = self.get_object(id)
            # abnormal_user.delete()
            ids = request.GET.get('id')
            for id in ids.split(','):
                abnormal_user = self.get_object(id)
                abnormal_user.delete()
            return CustomResponse()
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
