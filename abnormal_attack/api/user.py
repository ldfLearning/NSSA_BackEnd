from django import forms
from http import HTTPStatus
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from ..models import AbnormalUser
from ..serializers import AbnormalUserSerializer
from ...response import CustomResponse, ERROR_CODES, ERROR_MESSAGES

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
            content = request.GET.get('content')
            type = request.GET.get('type')
            time = request.GET.get('time')
            user_name = request.GET.get('user_name')
            topic = request.GET.get('topic')
            src_ip = request.GET.get('src_ip')
            sort = request.GET.get('sort', 'desc')      # 默认按升序排序
            page = request.GET.get('page', 1)           # 默认为第一页
            page_size = request.GET.get('limit', 10)    # 默认每页大小为10

            # 构建筛选条件
            filters = {}
            if content:
                filters['detail__icontains'] = content
            if type:
                filters['type'] = type
            if src_ip:
                filters['src_ip'] = src_ip

            # 应用筛选条件
            abnormal_user = AbnormalUser.objects.filter(**filters)

            # 排序
            if sort.lower() == 'desc':
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

    # 删除记录
    def delete(self, request):
        try:
            id = request.GET.get('id')
            abnormal_user = self.get_object(id)
            abnormal_user.delete()
            return CustomResponse(status=204)
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )