from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 40
    page_size_query_param = 'page_size'
    limit_query_param = 'limit_size'
    max_page_size = 10000

    def get_next_link(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return page_number

    def get_paginated_response(self, data):
        response = {}
        response['page_size'] = self.page_size
        response['count'] = self.page.paginator.count
        response['next_page_number'] = self.page.next_page_number() if self.page.has_next() else None
        response['current_page_number'] = self.page.number
        response['previous_page_number'] = self.page.previous_page_number() if self.page.has_previous() else None
        response['next'] = self.get_next_link()
        response['previous'] = self.get_previous_link()
        response['result'] = data
        return Response(response)
