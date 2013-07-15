from django.conf.urls import patterns, url


urlpatterns = patterns('chpasswd.views',

    url(r'^$', 'chpasswd_prompt', name='chpasswd_prompt'),
    url(r'^change$', 'chpasswd_change', name='chpasswd_change'),

)
