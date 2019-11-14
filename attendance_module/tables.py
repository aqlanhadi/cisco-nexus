from django.contrib.auth.models import User

from datatableview.views import Datatable, DatatableView

class GuardList(DatatableView):
    model = User

    class datatable_class(Datatable):
        class Meta:
            columns = ['id', 'username']
    
    def get_datatable_kwargs(self, **kwargs):
        return super().get_datatable_kwargs(**kwargs)