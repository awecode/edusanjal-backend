from rest_framework.pagination import PageNumberPagination as BasePageNumberPagination
from rest_framework.response import Response


class PageNumberPagination(BasePageNumberPagination):
    def clean_agg(self, dct, order, skip):
        agg = {}
        for key, value in dct.items():
            if type(value) == dict and 'buckets' in value.keys():
                items = value.get('buckets')
                # Skip if specified
                if key in skip:
                    items = [item for item in items if item['key'] not in skip[key]]
                # Order if specified
                if key in order:
                    sort_order = {val: idx for idx, val in enumerate(order[key])}
                    items.sort(key=lambda x: sort_order[x['key']])
            else:
                items = value
            agg[key] = items
        return agg

    def get_paginated_response(self, data, aggregations=None, aggregation_order={}, aggregation_skip={}):

        global_agg = {}
        if 'global' in aggregations.keys():
            global_agg = self.clean_agg(aggregations['global'], aggregation_order, aggregation_skip)
            del aggregations['global']

        local_agg = self.clean_agg(aggregations, aggregation_order, aggregation_skip)

        return Response(self.get_response_data(data, local_agg, global_agg))

    def get_response_data(self, data, local_agg={}, global_agg={}):
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
            'local_agg': local_agg,
            'global_agg': global_agg,
            'results': data
        }
