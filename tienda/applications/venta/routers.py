

from rest_framework.routers import DefaultRouter

from . import viewsets

# instanciar el objeto enrutador
router = DefaultRouter()

# se registrar las rutas
# colors puede ser cualquier nombre
router.register(r'ventas', viewsets.VentasViewSet, basename = 'ventas')

urlpatterns = router.urls
