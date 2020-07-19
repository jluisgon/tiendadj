

from rest_framework.routers import DefaultRouter

from . import viewsets

# instanciar el objeto enrutador
router = DefaultRouter()

# se registrar las rutas
# colors puede ser cualquier nombre
router.register(r'colors', viewsets.ColorViewSet, basename = 'colors')
router.register(r'productos', viewsets.ProductViewSet, basename = 'productos')

urlpatterns = router.urls
