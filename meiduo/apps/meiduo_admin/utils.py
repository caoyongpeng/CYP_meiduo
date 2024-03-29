from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


def jwt_response_payload_handler(token,user=None,request=None):

    return {
        'token':token,
        'id':user.id,
        'username':user.username
    }

class PageNum(PageNumberPagination):

    page_size_query_param = 'pagesize'

    max_page_size = 8

    def get_paginated_response(self,data):

        return Response({
            'count': self.page.paginator.count,  # 总数量
            'lists': data,  # 用户数据
            'page': self.page.number,  # 当前页数
            'pages': self.page.paginator.num_pages,  # 总页数
            'pagesize': self.max_page_size  # 后端指定的页容量
        })