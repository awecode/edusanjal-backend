from rest_framework.pagination import PageNumberPagination as BasePageNumberPagination
from rest_framework.response import Response


class PageNumberPagination(BasePageNumberPagination):
    def get_paginated_response(self, data, aggregations=None):
        trimmed_aggregations = {}
        # local aggregation
        # aggregate = aggregations
        # global aggregation with bucket count
        aggregate = aggregations.get('count')
        for key, value in aggregate.items():
            if type(value) == dict and 'buckets' in value.keys():
                trimmed_aggregations[key] = value.get('buckets')
            else:
                trimmed_aggregations[key] = value
        return Response(self.get_response_data(data, trimmed_aggregations))

    def get_response_data(self, data, aggregations):
        count = self.page.paginator.count
        size = self.page_size
        return {
            'pagination': {
                # 'next': self.get_next_link(),
                # 'previous': self.get_previous_link(),
                'count': count,
                'page': self.page.number,
                'pages': (count + (-count % size)) // size,  # round-up division
            },
            'aggregations': aggregations,
            'results': data
        }
