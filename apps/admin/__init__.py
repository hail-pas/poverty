import settings
from . import routes
from .paralib import Site, app, Menu

site = Site(
    name='微服务管理后台',
    logo=settings.SERVER_URL + '/static/images/logo.png',
    locale='zh-CN',
    locale_switcher=False,
    menus=[
        Menu(
            name='首页',
            url='/',
            icon='fa fa-home'
        ),
        Menu(
            name='配置',
            title=True
        ),
        Menu(
            name='应用',
            url='/rest/App',
            icon='fa fa-pencil',
            search_fields=('uaid',)
        ),
        Menu(
            name='在线参数',
            url='/rest/Config',
            icon='fa fa-cog',
            search_fields=('key',)
        ),
        Menu(
            name='授权',
            title=True
        ),
        Menu(
            name='用户',
            url='/rest/User',
            icon='fa fa-user'
        ),
        Menu(
            name='角色',
            url='/rest/Role',
            icon='fa fa-group'
        ),
        Menu(
            name='注销',
            url='/logout',
            icon='fa fa-lock'
        )
    ]
)
