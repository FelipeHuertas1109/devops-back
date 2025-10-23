from django.urls import path
from . import views

urlpatterns = [
    # ===== AUTENTICACIÓN (HU1, HU2) =====
    path('login/', views.login_usuario, name='login_usuario'),
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('usuario/actual/', views.obtener_usuario_actual, name='obtener_usuario_actual'),
    
    # ===== HORARIOS FIJOS (HU3) =====
    path('horarios/', views.horarios_fijos, name='horarios_fijos'),
    path('horarios/multiple/', views.horarios_fijos_multiple, name='horarios_fijos_multiple'),
    path('horarios/edit-multiple/', views.horarios_fijos_edit_multiple, name='horarios_fijos_edit_multiple'),
    path('horarios/<int:pk>/', views.horario_fijo_detalle, name='horario_fijo_detalle'),
    
    # ===== DIRECTIVO - CONSULTA DE HORARIOS (HU3) =====
    path('directivo/horarios/', views.directivo_horarios_monitores, name='directivo_horarios_monitores'),
    
    # ===== AJUSTES MANUALES DE HORAS (HU7A) =====
    path('directivo/ajustes-horas/', views.directivo_ajustes_horas, name='directivo_ajustes_horas'),
    path('directivo/ajustes-horas/<int:pk>/', views.directivo_ajuste_horas_detalle, name='directivo_ajuste_horas_detalle'),
    
    # ===== CONFIGURACIONES DEL SISTEMA (HU9) =====
    path('directivo/configuraciones/', views.directivo_configuraciones, name='directivo_configuraciones'),
    path('directivo/configuraciones/crear/', views.directivo_configuraciones_crear, name='directivo_configuraciones_crear'),
    path('directivo/configuraciones/inicializar/', views.directivo_configuraciones_inicializar, name='directivo_configuraciones_inicializar'),
    path('directivo/configuraciones/<str:clave>/', views.directivo_configuraciones_detalle, name='directivo_configuraciones_detalle'),
    path('directivo/configuraciones/<int:id>/', views.directivo_configuraciones_detalle_por_id, name='directivo_configuraciones_detalle_por_id'),
]
