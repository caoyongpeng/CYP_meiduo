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

    def get_paginated_response(self, data):

        return Response({
            'count':self.page.paginator.count,
            'lists':data,
            'page':self.page.number,
            'pages':self.page.paginator.num_pages,
            'pagesize':self.max_page_size
        })