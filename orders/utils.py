from django.template import RequestContext

def get_base_context(request):
	c = RequestContext(request).dicts[-1] #get last context
	return c