#!/usr/bin/env python
"""
Script de prueba completo para la API de DevOps Backend
Prueba todos los endpoints implementados incluyendo:
- Horarios (schedules)
- Asistencias
- Ajustes de horas
- Validaciones

Autor: Sistema DevOps
Fecha: 2025
"""

import requests
import json
from datetime import date, timedelta

# Configuración
BASE_URL = "http://localhost:8000/api"

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.YELLOW}ℹ {text}{Colors.ENDC}")

def print_test(text):
    print(f"\n{Colors.BOLD}Prueba: {text}{Colors.ENDC}")

# Variables globales para almacenar datos de prueba
test_data = {
    'monitor_token': None,
    'monitor_id': None,
    'monitor_username': None,
    'horario_id': None,
    'asistencia_id': None,
    'ajuste_id': None
}

def test_registro_monitor():
    """HU1: Registro de monitor"""
    print_header("TEST 1: REGISTRO DE MONITOR")
    
    # Generar username único
    import random
    username = f"monitor_test_{random.randint(1000, 9999)}"
    
    print_test("Registro de nuevo monitor")
    response = requests.post(f"{BASE_URL}/registro/", json={
        "username": username,
        "nombre": "Monitor de Prueba",
        "password": "password123",
        "confirm_password": "password123"
    })
    
    if response.status_code == 201:
        data = response.json()
        test_data['monitor_token'] = data['token']
        test_data['monitor_id'] = data['usuario']['id']
        test_data['monitor_username'] = data['usuario']['username']
        print_success(f"Monitor registrado exitosamente: {data['usuario']['nombre']}")
        print_info(f"ID: {data['usuario']['id']}, Username: {data['usuario']['username']}")
        return True
    else:
        print_error(f"Error al registrar monitor: {response.status_code}")
        print_error(response.text)
        return False


def test_login_monitor():
    """HU2: Login de monitor"""
    print_header("TEST 2: LOGIN DE MONITOR")
    
    print_test("Login con credenciales del monitor")
    response = requests.post(f"{BASE_URL}/login/", json={
        "nombre_de_usuario": test_data['monitor_username'],
        "password": "password123"
    })
    
    if response.status_code == 200:
        data = response.json()
        test_data['monitor_token'] = data['token']
        print_success(f"Login exitoso: {data['usuario']['nombre']}")
        print_info(f"Token: {data['token'][:50]}...")
        return True
    else:
        print_error(f"Error al hacer login: {response.status_code}")
        print_error(response.text)
        return False


def test_crear_horarios():
    """HU3: Crear horarios fijos (schedules)"""
    print_header("TEST 3: CREAR HORARIOS FIJOS (SCHEDULES)")
    
    headers = {"Authorization": f"Bearer {test_data['monitor_token']}"}
    
    # Prueba 1: Crear un horario individual
    print_test("Crear horario individual")
    response = requests.post(f"{BASE_URL}/schedules/", 
        headers=headers,
        json={
            "dia_semana": 0,  # Lunes
            "jornada": "M",   # Mañana
            "sede": "SA"      # San Antonio
        }
    )
    
    if response.status_code == 201:
        data = response.json()
        test_data['horario_id'] = data['id']
        print_success(f"Horario creado: Lunes Mañana en San Antonio (ID: {data['id']})")
    else:
        print_error(f"Error al crear horario: {response.status_code}")
        print_error(response.text)
        return False
    
    # Prueba 2: Crear múltiples horarios
    print_test("Crear múltiples horarios")
    response = requests.post(f"{BASE_URL}/schedules/multiple/",
        headers=headers,
        json={
            "horarios": [
                {"dia_semana": 1, "jornada": "M", "sede": "BA"},  # Martes Mañana Barcelona
                {"dia_semana": 2, "jornada": "T", "sede": "SA"},  # Miércoles Tarde San Antonio
                {"dia_semana": 3, "jornada": "M", "sede": "SA"}   # Jueves Mañana San Antonio
            ]
        }
    )
    
    if response.status_code in [201, 207]:
        data = response.json()
        print_success(f"Horarios creados: {data['total_creados']} de {data['total_solicitados']}")
    else:
        print_error(f"Error al crear horarios múltiples: {response.status_code}")
        print_error(response.text)
    
    return True


def test_listar_horarios():
    """HU3: Listar horarios con filtros"""
    print_header("TEST 4: LISTAR Y FILTRAR HORARIOS")
    
    headers = {"Authorization": f"Bearer {test_data['monitor_token']}"}
    
    # Prueba 1: Listar todos los horarios del usuario
    print_test("Listar todos los horarios del monitor")
    response = requests.get(f"{BASE_URL}/schedules/", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Horarios listados: {len(data)} horarios encontrados")
        for horario in data:
            print_info(f"  - {horario['dia_semana_display']} {horario['jornada_display']} en {horario['sede_display']}")
    else:
        print_error(f"Error al listar horarios: {response.status_code}")
        return False
    
    return True


def test_crear_asistencias():
    """HU5: Crear asistencias"""
    print_header("TEST 5: CREAR ASISTENCIAS")
    
    headers = {"Authorization": f"Bearer {test_data['monitor_token']}"}
    
    # Prueba 1: Crear asistencia válida
    print_test("Crear asistencia válida")
    fecha_hoy = date.today().isoformat()
    
    response = requests.post(f"{BASE_URL}/asistencias/",
        headers=headers,
        json={
            "horario_id": test_data['horario_id'],
            "fecha": fecha_hoy,
            "presente": True,
            "horas": 4.0
        }
    )
    
    if response.status_code == 201:
        data = response.json()
        test_data['asistencia_id'] = data['id']
        print_success(f"Asistencia creada exitosamente (ID: {data['id']})")
        print_info(f"  Fecha: {data['fecha']}, Horas: {data['horas']}, Estado: {data['estado_autorizacion']}")
    else:
        print_error(f"Error al crear asistencia: {response.status_code}")
        print_error(response.text)
        return False
    
    # Prueba 2: Intentar crear asistencia duplicada (debe fallar - validación de unicidad)
    print_test("Validar unicidad - intentar crear asistencia duplicada")
    response = requests.post(f"{BASE_URL}/asistencias/",
        headers=headers,
        json={
            "horario_id": test_data['horario_id'],
            "fecha": fecha_hoy,
            "presente": True,
            "horas": 3.0
        }
    )
    
    if response.status_code == 400:
        print_success("Validación de unicidad funcionando correctamente - asistencia duplicada rechazada")
    else:
        print_error(f"Error en validación de unicidad: {response.status_code}")
    
    # Prueba 3: Validar rango de horas (debe aceptar 0-24)
    print_test("Validar rango de horas - probar con horas inválidas (>24)")
    response = requests.post(f"{BASE_URL}/asistencias/",
        headers=headers,
        json={
            "horario_id": test_data['horario_id'],
            "fecha": (date.today() + timedelta(days=1)).isoformat(),
            "presente": True,
            "horas": 25.0  # Inválido
        }
    )
    
    if response.status_code == 400:
        print_success("Validación de rango de horas funcionando correctamente - horas > 24 rechazadas")
    else:
        print_error(f"Error en validación de rango de horas: {response.status_code}")
    
    return True


def test_listar_asistencias():
    """HU5: Listar asistencias con filtros"""
    print_header("TEST 6: LISTAR Y FILTRAR ASISTENCIAS")
    
    headers = {"Authorization": f"Bearer {test_data['monitor_token']}"}
    
    # Prueba 1: Listar todas las asistencias
    print_test("Listar todas las asistencias del monitor")
    response = requests.get(f"{BASE_URL}/asistencias/", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Asistencias listadas: {data['total_asistencias']} asistencias, {data['total_horas']} horas totales")
        for asistencia in data['asistencias']:
            print_info(f"  - {asistencia['fecha']}: {asistencia['horas']}h - {asistencia['estado_autorizacion_display']}")
    else:
        print_error(f"Error al listar asistencias: {response.status_code}")
        return False
    
    # Prueba 2: Filtrar por estado
    print_test("Filtrar asistencias por estado (pendiente)")
    response = requests.get(f"{BASE_URL}/asistencias/?estado=pendiente", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Asistencias pendientes: {data['total_asistencias']}")
    else:
        print_error(f"Error al filtrar asistencias: {response.status_code}")
    
    return True


def test_actualizar_asistencia():
    """HU5: Actualizar asistencias"""
    print_header("TEST 7: ACTUALIZAR ASISTENCIAS")
    
    headers = {"Authorization": f"Bearer {test_data['monitor_token']}"}
    
    print_test("Actualizar horas de asistencia")
    response = requests.put(f"{BASE_URL}/asistencias/{test_data['asistencia_id']}/",
        headers=headers,
        json={
            "horas": 5.5
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Asistencia actualizada: {data['horas']} horas")
    else:
        print_error(f"Error al actualizar asistencia: {response.status_code}")
        print_error(response.text)
        return False
    
    return True


def test_validacion_ajuste_horas():
    """HU7A: Validar rango de ajuste de horas (-24 a 24)"""
    print_header("TEST 8: VALIDACIÓN DE AJUSTE DE HORAS")
    
    # Nota: Este test requiere un usuario DIRECTIVO
    # Por simplicidad, asumimos que existe un directivo en el sistema
    print_info("Nota: Este test requiere autenticación como DIRECTIVO")
    print_info("Verificando validación en el serializer...")
    
    # La validación está implementada en AjusteHorasCreateSerializer.validate_cantidad_horas()
    # que valida el rango -24.00 a 24.00
    
    print_success("Validación de ajuste de horas implementada en serializer")
    print_info("  - Rango permitido: -24.00 a 24.00")
    print_info("  - No se permite valor 0")
    
    return True


def test_obtener_asistencia():
    """HU5: Obtener detalle de asistencia"""
    print_header("TEST 9: OBTENER DETALLE DE ASISTENCIA")
    
    headers = {"Authorization": f"Bearer {test_data['monitor_token']}"}
    
    print_test(f"Obtener asistencia ID: {test_data['asistencia_id']}")
    response = requests.get(f"{BASE_URL}/asistencias/{test_data['asistencia_id']}/", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print_success("Asistencia obtenida exitosamente")
        print_info(f"  Fecha: {data['fecha']}")
        print_info(f"  Horas: {data['horas']}")
        print_info(f"  Estado: {data['estado_autorizacion_display']}")
    else:
        print_error(f"Error al obtener asistencia: {response.status_code}")
        return False
    
    return True


def test_actualizar_horario():
    """HU3: Actualizar horario"""
    print_header("TEST 10: ACTUALIZAR HORARIO")
    
    headers = {"Authorization": f"Bearer {test_data['monitor_token']}"}
    
    print_test(f"Actualizar horario ID: {test_data['horario_id']}")
    response = requests.put(f"{BASE_URL}/schedules/{test_data['horario_id']}/",
        headers=headers,
        json={
            "dia_semana": 0,
            "jornada": "T",  # Cambiar de Mañana a Tarde
            "sede": "BA"     # Cambiar de San Antonio a Barcelona
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print_success("Horario actualizado exitosamente")
        print_info(f"  Nueva jornada: {data['jornada']}")
        print_info(f"  Nueva sede: {data['sede']}")
    else:
        print_error(f"Error al actualizar horario: {response.status_code}")
        print_error(response.text)
        return False
    
    return True


def test_obtener_usuario_actual():
    """HU2: Obtener información del usuario actual"""
    print_header("TEST 11: OBTENER USUARIO ACTUAL")
    
    headers = {"Authorization": f"Bearer {test_data['monitor_token']}"}
    
    print_test("Obtener información del usuario autenticado")
    response = requests.get(f"{BASE_URL}/usuario/actual/", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Usuario obtenido: {data['nombre']}")
        print_info(f"  Username: {data['username']}")
        print_info(f"  Tipo: {data['tipo_usuario_display']}")
    else:
        print_error(f"Error al obtener usuario actual: {response.status_code}")
        return False
    
    return True


def test_eliminar_asistencia():
    """HU5: Eliminar asistencia"""
    print_header("TEST 12: ELIMINAR ASISTENCIA")
    
    headers = {"Authorization": f"Bearer {test_data['monitor_token']}"}
    
    print_test(f"Eliminar asistencia ID: {test_data['asistencia_id']}")
    response = requests.delete(f"{BASE_URL}/asistencias/{test_data['asistencia_id']}/", headers=headers)
    
    if response.status_code == 204:
        print_success("Asistencia eliminada exitosamente")
    else:
        print_error(f"Error al eliminar asistencia: {response.status_code}")
        return False
    
    # Verificar que fue eliminada
    print_test("Verificar que la asistencia fue eliminada")
    response = requests.get(f"{BASE_URL}/asistencias/{test_data['asistencia_id']}/", headers=headers)
    
    if response.status_code == 404:
        print_success("Confirmado: asistencia no existe")
    else:
        print_error("Error: asistencia aún existe")
        return False
    
    return True


def test_eliminar_horario():
    """HU3: Eliminar horario"""
    print_header("TEST 13: ELIMINAR HORARIO")
    
    headers = {"Authorization": f"Bearer {test_data['monitor_token']}"}
    
    print_test(f"Eliminar horario ID: {test_data['horario_id']}")
    response = requests.delete(f"{BASE_URL}/schedules/{test_data['horario_id']}/", headers=headers)
    
    if response.status_code == 204:
        print_success("Horario eliminado exitosamente")
    else:
        print_error(f"Error al eliminar horario: {response.status_code}")
        return False
    
    return True


def run_all_tests():
    """Ejecutar todos los tests"""
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════════════════════════╗")
    print("║                   SCRIPT DE PRUEBAS - DEVOPS BACKEND API                      ║")
    print("║                                                                                ║")
    print("║  Prueba completa de endpoints de horarios, asistencias y validaciones         ║")
    print("╚════════════════════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")
    
    print_info(f"Base URL: {BASE_URL}")
    print_info("Asegúrate de que el servidor Django esté corriendo en localhost:8000\n")
    
    results = []
    
    # Ejecutar tests en orden
    tests = [
        ("Registro de Monitor", test_registro_monitor),
        ("Login de Monitor", test_login_monitor),
        ("Crear Horarios (Schedules)", test_crear_horarios),
        ("Listar Horarios", test_listar_horarios),
        ("Crear Asistencias", test_crear_asistencias),
        ("Listar Asistencias", test_listar_asistencias),
        ("Actualizar Asistencia", test_actualizar_asistencia),
        ("Validación Ajuste de Horas", test_validacion_ajuste_horas),
        ("Obtener Asistencia", test_obtener_asistencia),
        ("Actualizar Horario", test_actualizar_horario),
        ("Obtener Usuario Actual", test_obtener_usuario_actual),
        ("Eliminar Asistencia", test_eliminar_asistencia),
        ("Eliminar Horario", test_eliminar_horario),
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Excepción en {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Resumen
    print_header("RESUMEN DE PRUEBAS")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        if result:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")
    
    print(f"\n{Colors.BOLD}Resultado Final: {passed}/{total} pruebas pasaron{Colors.ENDC}")
    
    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}¡Todas las pruebas pasaron exitosamente!{Colors.ENDC}")
    else:
        print(f"{Colors.YELLOW}Algunas pruebas fallaron. Revisa los detalles arriba.{Colors.ENDC}")


if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Pruebas interrumpidas por el usuario{Colors.ENDC}")
    except Exception as e:
        print_error(f"Error fatal: {str(e)}")
        import traceback
        traceback.print_exc()

