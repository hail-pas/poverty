from django.conf import settings
from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem


class AppConfig(DjangoSuitConfig):
    layout = 'vertical'
    menu = (
        ParentItem('任务调度', permissions=('auth.add_user',), children=[
            ChildItem(url=settings.FLOWER_URL, label='异步任务监控', target_blank=True),
        ], icon='fa fa-clock-o'),
        ParentItem('基本信息', app='api', permissions='api.view_user', children=[
            ChildItem(model='user'),
            ChildItem(model='potentialcustomer'),
            ChildItem(model='order'),
            ChildItem(model='task'),
            ChildItem(model='kstask'),
            ChildItem(model='balancelog'),
            ChildItem(model='company'),
            ChildItem(model='invoice'),
            ChildItem(model='answerlog'),
            ChildItem(model='monitor'),
            ChildItem(model='monitorlog'),
            ChildItem(model='workmonitor'),
            ChildItem(model='workmonitorlog'),
            ChildItem(model='ksstatistic'),
            ChildItem(model='suggest'),
            ChildItem(model='finishspeedlog'),
        ], icon='fa fa-leaf'),
        ParentItem('基本配置', app='api', children=[
            ChildItem(model='ksuser'),
            ChildItem(model='good'),
            ChildItem(model='ksservice'),
            ChildItem(model='taskplatform'),
            ChildItem(model='taskcategory'),
            ChildItem(model='taskcategoryextraneed'),
            # ChildItem(model='taskcategorylevel'),
            ChildItem(model='notice'),
            ChildItem(model='legalknowledge'),
            ChildItem(model='config'),
            ChildItem(model='questioncategory'),
            ChildItem(model='question'),
            ChildItem(model='app'),
        ], icon='fa fa-cog'),
        ParentItem('其他操作', app='dashboard', children=[
            ChildItem(url='dashboard:order', label='label'),
        ], icon='fa fa-pencil'),
        ParentItem('操作日志', app='admin', icon='fa fa-file'),
        ParentItem('认证和授权', app='auth', icon='fa fa-users')
    )
