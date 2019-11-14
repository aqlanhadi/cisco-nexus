from django.contrib.auth.models import User
from table import Table
from table.columns import Column

class SalaryList(Table):
    id = Column(field='id')
    username = Column(field='username')

    class Meta:
        model = User