import datetime
import urllib, httplib


class TaskUtils():
    
    def _run_spider(self, **kwargs):
        param_dict = {
            'project': 'default',
            'spider': kwargs['spider'],
            'id': kwargs['id'],
            'run_type': kwargs['run_type'],
            'do_action': kwargs['do_action']
        }
        params = urllib.urlencode(param_dict)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = httplib.HTTPConnection("localhost:6800")
        conn.request("POST", "/schedule.json", params, headers)
        conn.getresponse()
    
    
    def run_spiders(self, ref_obj_class, scraper_runtime_field_name, spider_name):
        
        kwargs = {
            '%s__status' % scraper_runtime_field_name: 'A',
            '%s__scheduler_runtime__next_action_time__lt' % scraper_runtime_field_name: datetime.datetime.now,
        }
        
        ref_obj_list = ref_obj_class.objects.filter(**kwargs)
        for ref_object in ref_obj_list:
            self._run_spider(id=ref_object.id, spider=spider_name, run_type='TASK', do_action='yes')
        

    def run_checkers(self, ref_obj_class, scheduler_runtime_field_name, checker_name):
        
        kwargs = {
            '%s__next_action_time__lt' % scheduler_runtime_field_name: datetime.datetime.now,
        }
        
        ref_obj_list = ref_obj_class.objects.filter(**kwargs)
        for ref_object in ref_obj_list:
            self._run_spider(id=ref_object.id, spider=checker_name, run_type='TASK', do_action='yes')

