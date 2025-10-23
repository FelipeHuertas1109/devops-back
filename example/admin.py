from django.contrib import admin
from .models import UsuarioPersonalizado, HorarioFijo, AjusteHoras, ConfiguracionSistema

@admin.register(UsuarioPersonalizado)
class UsuarioPersonalizadoAdmin(admin.ModelAdmin):
    list_display = ['username', 'nombre', 'tipo_usuario', 'is_active', 'date_joined']
    list_filter = ['tipo_usuario', 'is_active', 'date_joined']
    search_fields = ['username', 'nombre']
    ordering = ['username']

@admin.register(HorarioFijo)
class HorarioFijoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'dia_semana', 'jornada', 'sede']
    list_filter = ['dia_semana', 'jornada', 'sede']
    search_fields = ['usuario__username', 'usuario__nombre']
    ordering = ['usuario', 'dia_semana', 'jornada']

@admin.register(AjusteHoras)
class AjusteHorasAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'fecha', 'cantidad_horas', 'creado_por', 'created_at']
    list_filter = ['fecha', 'created_at', 'creado_por']
    search_fields = ['usuario__username', 'usuario__nombre', 'motivo']
    ordering = ['-created_at']
    date_hierarchy = 'fecha'
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ConfiguracionSistema)
class ConfiguracionSistemaAdmin(admin.ModelAdmin):
    list_display = ['clave', 'valor', 'tipo_dato', 'creado_por', 'created_at']
    list_filter = ['tipo_dato', 'created_at']
    search_fields = ['clave', 'descripcion']
    ordering = ['clave']
    readonly_fields = ['created_at', 'updated_at']
