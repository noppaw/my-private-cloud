from rest_framework.generics import ListAPIView
from .models import MicroApp
from .serializers import MicroAppSerializer

class MicroAppListView(ListAPIView):
    # ดึงเฉพาะ App ที่ติ๊ก is_active=True เท่านั้น
    queryset = MicroApp.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = MicroAppSerializer