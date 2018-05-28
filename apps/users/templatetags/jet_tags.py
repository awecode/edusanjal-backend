from collections import OrderedDict

from jet.templatetags.jet_tags import *
from jet.utils import get_original_menu_items


@assignment_tag
def jet_get_bookmarks(user):
    return None


def get_menu_items(context):
    context['user'] = None
    original_app_list = OrderedDict(map(lambda app: (app['app_label'], app), get_original_menu_items(context)))

    def map_item(item):
        item['items'] = item['models']
        return item

    app_list = list(map(map_item, original_app_list.values()))

    current_found = False

    for app in app_list:
        if not current_found:
            for model in app['items']:
                if not current_found and model.get('url') and context['request'].path.startswith(model['url']):
                    model['current'] = True
                    current_found = True
                else:
                    model['current'] = False

            if not current_found and app.get('url') and context['request'].path.startswith(app['url']):
                app['current'] = True
                current_found = True
            else:
                app['current'] = False

    return app_list


@assignment_tag(takes_context=True)
def jet_get_menu(context):
    return get_menu_items(context)
