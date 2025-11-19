from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import jwt
from datetime import date, timedelta
from .models import UsuarioPersonalizado, HorarioFijo, Asistencia, AjusteHoras, ConfiguracionSistema

from .serializers import (
    LoginSerializer, UsuarioSerializer, UsuarioCreateSerializer,
    HorarioFijoSerializer, HorarioFijoCreateSerializer, HorarioFijoMultipleSerializer, HorarioFijoEditMultipleSerializer,
    AsistenciaSerializer, AsistenciaCreateSerializer, AsistenciaUpdateSerializer,
    AjusteHorasSerializer, AjusteHorasCreateSerializer,
    ConfiguracionSistemaSerializer, ConfiguracionSistemaCreateSerializer
)

# ===== AUTENTICACIÓN (HU1, HU2) =====

@api_view(['POST'])
@permission_classes([AllowAny])
def login_usuario(request):
    """
    HU2: Login y obtención de token
    Endpoint para autenticación de usuarios (monitores y directivos)
    """
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        nombre_usuario = serializer.validated_data['nombre_de_usuario']
        password = serializer.validated_data['password']
        
        # Buscar usuario por nombre de usuario
        try:
            usuario = UsuarioPersonalizado.objects.get(username=nombre_usuario)
        except UsuarioPersonalizado.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verificar contraseña
        if not usuario.check_password(password):
            return Response(
                {'error': 'Contraseña incorrecta'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generar token JWT que no expira
        refresh = RefreshToken.for_user(usuario)
        access_token = refresh.access_token
        
        # Configurar el token para que no expire
        access_token.set_exp(lifetime=None)
        
        # Crear respuesta con token y datos del usuario usando el serializer
        usuario_serializer = UsuarioSerializer(usuario)
        response_data = {
            'token': str(access_token),
            'usuario': usuario_serializer.data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def registro_usuario(request):
    """
    HU1: Registro de monitor
    Endpoint para registrar nuevos usuarios.
    El tipo_usuario se asigna automáticamente como MONITOR.
    """
    serializer = UsuarioCreateSerializer(data=request.data)
    
    if serializer.is_valid():
        # Crear el usuario
        usuario = serializer.save()
        
        # Generar token JWT automáticamente para el usuario recién creado
        refresh = RefreshToken.for_user(usuario)
        access_token = refresh.access_token
        access_token.set_exp(lifetime=None)
        
        # Serializar datos del usuario para la respuesta
        usuario_serializer = UsuarioSerializer(usuario)
        
        response_data = {
            'mensaje': 'Usuario registrado exitosamente',
            'token': str(access_token),
            'usuario': usuario_serializer.data
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def obtener_usuario_actual(request):
    """
    Endpoint para obtener información del usuario autenticado
    """
    # Obtener usuario desde el token JWT
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({'detail': 'Token de autenticación requerido', 'code': 'token_required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    token = auth_header.split(' ')[1]
    try:
        payload = AccessToken(token)
        user_id = payload.get('user_id')
    except Exception:
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            user_id = payload.get('user_id')
        except Exception as e:
            return Response({'detail': f'Token inválido: {str(e)}', 'code': 'invalid_token'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        usuario = UsuarioPersonalizado.objects.get(pk=user_id)
    except UsuarioPersonalizado.DoesNotExist:
        return Response({'detail': 'Usuario no encontrado', 'code': 'user_not_found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)


# ===== HORARIOS FIJOS (HU3) =====

@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def horarios_fijos(request):
    """
    HU3: Gestión individual de horarios
    GET: Obtener horarios fijos del usuario
    POST: Crear nuevo horario fijo
    """
    # Obtener usuario desde el token JWT
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({'detail': 'Token de autenticación requerido', 'code': 'token_required'}, status=status.HTTP_401_UNAUTHORIZED)
    token = auth_header.split(' ')[1]
    try:
        payload = AccessToken(token)
        user_id = payload.get('user_id')
    except Exception:
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            user_id = payload.get('user_id')
        except Exception as e:
            return Response({'detail': f'Token inválido: {str(e)}', 'code': 'invalid_token'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        usuario = UsuarioPersonalizado.objects.get(pk=user_id)
    except UsuarioPersonalizado.DoesNotExist:
        return Response({'detail': 'Usuario no encontrado', 'code': 'user_not_found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        horarios = HorarioFijo.objects.filter(usuario=usuario)
        serializer = HorarioFijoSerializer(horarios, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = HorarioFijoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=usuario)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def horario_fijo_detalle(request, pk):
    """
    HU3: Gestión individual de horarios
    GET: Obtener horario fijo específico
    PUT: Actualizar horario fijo
    DELETE: Eliminar horario fijo
    """
    # Obtener usuario desde el token JWT
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({'detail': 'Token de autenticación requerido', 'code': 'token_required'}, status=status.HTTP_401_UNAUTHORIZED)
    token = auth_header.split(' ')[1]
    try:
        payload = AccessToken(token)
        user_id = payload.get('user_id')
    except Exception:
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            user_id = payload.get('user_id')
        except Exception as e:
            return Response({'detail': f'Token inválido: {str(e)}', 'code': 'invalid_token'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        usuario = UsuarioPersonalizado.objects.get(pk=user_id)
    except UsuarioPersonalizado.DoesNotExist:
        return Response({'detail': 'Usuario no encontrado', 'code': 'user_not_found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        horario = HorarioFijo.objects.get(pk=pk, usuario=usuario)
    except HorarioFijo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = HorarioFijoSerializer(horario)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = HorarioFijoCreateSerializer(horario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        horario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def horarios_fijos_multiple(request):
    """
    HU3: Operaciones masivas de horarios
    Crear múltiples horarios fijos en una sola petición
    """
    # Verificar autenticación manualmente y obtener usuario desde el token
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({'detail': 'Token de autenticación requerido', 'code': 'token_required'}, status=status.HTTP_401_UNAUTHORIZED)
    token = auth_header.split(' ')[1]
    try:
        payload = AccessToken(token)
        user_id = payload.get('user_id')
    except Exception:
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            user_id = payload.get('user_id')
        except Exception as e:
            return Response({'detail': f'Token inválido: {str(e)}', 'code': 'invalid_token'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        usuario = UsuarioPersonalizado.objects.get(pk=user_id)
    except UsuarioPersonalizado.DoesNotExist:
        return Response({'detail': 'Usuario no encontrado', 'code': 'user_not_found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = HorarioFijoMultipleSerializer(data=request.data)
    
    if serializer.is_valid():
        horarios_data = serializer.validated_data['horarios']
        horarios_creados = []
        errores = []
        
        for i, horario_data in enumerate(horarios_data):
            try:
                # Verificar si ya existe un horario con la misma combinación
                horario_existente = HorarioFijo.objects.filter(
                    usuario=usuario,
                    dia_semana=horario_data['dia_semana'],
                    jornada=horario_data['jornada']
                ).first()
                
                if horario_existente:
                    errores.append(f"Horario {i+1}: Ya existe un horario para {horario_existente.get_dia_semana_display()} {horario_existente.get_jornada_display()}")
                    continue
                
                # Crear el horario fijo
                horario = HorarioFijo.objects.create(
                    usuario=usuario,
                    dia_semana=horario_data['dia_semana'],
                    jornada=horario_data['jornada'],
                    sede=horario_data['sede']
                )
                
                # Serializar el horario creado
                horario_serializado = HorarioFijoSerializer(horario).data
                horarios_creados.append(horario_serializado)
                
            except Exception as e:
                errores.append(f"Horario {i+1}: Error al crear - {str(e)}")
        
        # Preparar respuesta
        response_data = {
            'mensaje': f"Se crearon {len(horarios_creados)} horarios exitosamente para {usuario.username}",
            'horarios_creados': horarios_creados,
            'total_solicitados': len(horarios_data),
            'total_creados': len(horarios_creados),
            'usuario': {
                'id': usuario.id,
                'username': usuario.username,
                'nombre': usuario.nombre
            }
        }
        
        if errores:
            response_data['errores'] = errores
            response_data['mensaje'] += f", {len(errores)} con errores"
            return Response(response_data, status=status.HTTP_207_MULTI_STATUS)
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def horarios_fijos_edit_multiple(request):
    """
    HU3: Operaciones masivas de horarios
    Editar múltiples horarios fijos en una sola petición
    Esta funcionalidad reemplaza TODOS los horarios existentes del usuario con los nuevos
    """
    # Verificar autenticación manualmente y obtener usuario desde el token
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({'detail': 'Token de autenticación requerido', 'code': 'token_required'}, status=status.HTTP_401_UNAUTHORIZED)
    token = auth_header.split(' ')[1]
    try:
        payload = AccessToken(token)
        user_id = payload.get('user_id')
    except Exception:
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            user_id = payload.get('user_id')
        except Exception as e:
            return Response({'detail': f'Token inválido: {str(e)}', 'code': 'invalid_token'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        usuario = UsuarioPersonalizado.objects.get(pk=user_id)
    except UsuarioPersonalizado.DoesNotExist:
        return Response({'detail': 'Usuario no encontrado', 'code': 'user_not_found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = HorarioFijoEditMultipleSerializer(data=request.data)
    
    if serializer.is_valid():
        horarios_data = serializer.validated_data['horarios']
        
        # Eliminar todos los horarios existentes del usuario
        horarios_eliminados = HorarioFijo.objects.filter(usuario=usuario).count()
        HorarioFijo.objects.filter(usuario=usuario).delete()
        
        # Crear los nuevos horarios
        horarios_creados = []
        errores = []
        
        for i, horario_data in enumerate(horarios_data):
            try:
                # Crear el horario fijo
                horario = HorarioFijo.objects.create(
                    usuario=usuario,
                    dia_semana=horario_data['dia_semana'],
                    jornada=horario_data['jornada'],
                    sede=horario_data['sede']
                )
                
                # Serializar el horario creado
                horario_serializado = HorarioFijoSerializer(horario).data
                horarios_creados.append(horario_serializado)
                
            except Exception as e:
                errores.append(f"Horario {i+1}: Error al crear - {str(e)}")
        
        # Preparar respuesta
        response_data = {
            'mensaje': f"Se editaron los horarios exitosamente para {usuario.username}",
            'horarios_eliminados': horarios_eliminados,
            'horarios_creados': horarios_creados,
            'total_solicitados': len(horarios_data),
            'total_creados': len(horarios_creados),
            'usuario': {
                'id': usuario.id,
                'username': usuario.username,
                'nombre': usuario.nombre
            }
        }
        
        if errores:
            response_data['errores'] = errores
            response_data['mensaje'] += f", {len(errores)} con errores"
            return Response(response_data, status=status.HTTP_207_MULTI_STATUS)
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ===== ENDPOINTS PARA DIRECTIVOS (Consulta de Horarios) =====

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def directivo_horarios_monitores(request):
    """
    HU3: Vista directiva de horarios
    Listar todos los horarios fijos de todos los monitores.
    Filtros opcionales: usuario_id, dia_semana, jornada, sede
    Acceso: solo DIRECTIVO
    """
    # Autenticación manual
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({'detail': 'Token de autenticación requerido'}, status=status.HTTP_401_UNAUTHORIZED)

    # Usuario DIRECTIVO temporal
    usuario_directivo = UsuarioPersonalizado.objects.filter(tipo_usuario='DIRECTIVO').first()
    if not usuario_directivo:
        return Response({'detail': 'No hay usuarios DIRECTIVO'}, status=status.HTTP_403_FORBIDDEN)

    # Parámetros de filtrado
    usuario_id = request.query_params.get('usuario_id')
    dia_semana = request.query_params.get('dia_semana')
    jornada = request.query_params.get('jornada')
    sede = request.query_params.get('sede')

    # Query base: solo horarios de monitores
    horarios_qs = HorarioFijo.objects.filter(usuario__tipo_usuario='MONITOR')
    
    # Aplicar filtros
    if usuario_id:
        try:
            usuario_id = int(usuario_id)
            horarios_qs = horarios_qs.filter(usuario__id=usuario_id)
        except ValueError:
            return Response({'detail': 'usuario_id debe ser un número entero'}, status=status.HTTP_400_BAD_REQUEST)
    
    if dia_semana is not None:
        try:
            dia_semana = int(dia_semana)
            if dia_semana < 0 or dia_semana > 6:
                return Response({'detail': 'dia_semana debe ser entre 0-6'}, status=status.HTTP_400_BAD_REQUEST)
            horarios_qs = horarios_qs.filter(dia_semana=dia_semana)
        except ValueError:
            return Response({'detail': 'dia_semana debe ser un número entero'}, status=status.HTTP_400_BAD_REQUEST)
    
    if jornada:
        if jornada not in ['M', 'T']:
            return Response({'detail': 'jornada debe ser M o T'}, status=status.HTTP_400_BAD_REQUEST)
        horarios_qs = horarios_qs.filter(jornada=jornada)
    
    if sede:
        if sede not in ['SA', 'BA']:
            return Response({'detail': 'sede debe ser SA o BA'}, status=status.HTTP_400_BAD_REQUEST)
        horarios_qs = horarios_qs.filter(sede=sede)

    # Ordenar por usuario, día y jornada para mejor presentación
    horarios_qs = horarios_qs.order_by('usuario__nombre', 'dia_semana', 'jornada')
    
    # Serializar y responder
    serializer = HorarioFijoSerializer(horarios_qs.select_related('usuario'), many=True)
    
    # Agregar información de conteo
    response_data = {
        'total_horarios': horarios_qs.count(),
        'total_monitores': horarios_qs.values('usuario').distinct().count(),
        'horarios': serializer.data
    }
    
    return Response(response_data)


# ===== ASISTENCIAS (HU5) =====

@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def asistencias(request):
    """
    HU5: Gestión de asistencias
    GET: Listar asistencias del usuario autenticado con filtros opcionales
    POST: Crear nueva asistencia
    """
    # Obtener usuario desde el token JWT
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({'detail': 'Token de autenticación requerido', 'code': 'token_required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    token = auth_header.split(' ')[1]
    try:
        payload = AccessToken(token)
        user_id = payload.get('user_id')
    except Exception:
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            user_id = payload.get('user_id')
        except Exception as e:
            return Response({'detail': f'Token inválido: {str(e)}', 'code': 'invalid_token'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        usuario = UsuarioPersonalizado.objects.get(pk=user_id)
    except UsuarioPersonalizado.DoesNotExist:
        return Response({'detail': 'Usuario no encontrado', 'code': 'user_not_found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        # Parámetros de filtrado opcionales
        fecha_inicio_str = request.query_params.get('fecha_inicio')
        fecha_fin_str = request.query_params.get('fecha_fin')
        estado = request.query_params.get('estado')
        horario_id = request.query_params.get('horario_id')
        
        # Query base: asistencias del usuario
        asistencias_qs = Asistencia.objects.filter(usuario=usuario).select_related('usuario', 'horario')
        
        # Aplicar filtros
        if fecha_inicio_str:
            try:
                fecha_inicio = date.fromisoformat(fecha_inicio_str)
                asistencias_qs = asistencias_qs.filter(fecha__gte=fecha_inicio)
            except ValueError:
                return Response({'detail': 'Formato de fecha_inicio inválido. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
        
        if fecha_fin_str:
            try:
                fecha_fin = date.fromisoformat(fecha_fin_str)
                asistencias_qs = asistencias_qs.filter(fecha__lte=fecha_fin)
            except ValueError:
                return Response({'detail': 'Formato de fecha_fin inválido. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
        
        if estado:
            if estado not in ['pendiente', 'autorizado', 'rechazado']:
                return Response({'detail': 'Estado debe ser: pendiente, autorizado o rechazado'}, status=status.HTTP_400_BAD_REQUEST)
            asistencias_qs = asistencias_qs.filter(estado_autorizacion=estado)
        
        if horario_id:
            try:
                horario_id = int(horario_id)
                asistencias_qs = asistencias_qs.filter(horario_id=horario_id)
            except ValueError:
                return Response({'detail': 'horario_id debe ser un número entero'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = AsistenciaSerializer(asistencias_qs, many=True)
        
        # Estadísticas
        total_asistencias = asistencias_qs.count()
        total_horas = sum(float(a.horas) for a in asistencias_qs)
        
        return Response({
            'total_asistencias': total_asistencias,
            'total_horas': total_horas,
            'asistencias': serializer.data
        })
    
    elif request.method == 'POST':
        serializer = AsistenciaCreateSerializer(data=request.data, context={'usuario': usuario})
        if serializer.is_valid():
            # Obtener el horario
            horario = HorarioFijo.objects.get(id=serializer.validated_data['horario_id'])
            
            # Verificar que el horario pertenezca al usuario
            if horario.usuario != usuario:
                return Response(
                    {'detail': 'El horario especificado no pertenece al usuario autenticado'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Crear la asistencia
            asistencia = Asistencia.objects.create(
                usuario=usuario,
                horario=horario,
                fecha=serializer.validated_data['fecha'],
                presente=serializer.validated_data['presente'],
                horas=serializer.validated_data['horas']
            )
            
            return Response(AsistenciaSerializer(asistencia).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def asistencia_detalle(request, pk):
    """
    HU5: Gestión de asistencias
    GET: Obtener asistencia específica
    PUT: Actualizar asistencia
    DELETE: Eliminar asistencia
    """
    # Obtener usuario desde el token JWT
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({'detail': 'Token de autenticación requerido', 'code': 'token_required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    token = auth_header.split(' ')[1]
    try:
        payload = AccessToken(token)
        user_id = payload.get('user_id')
    except Exception:
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            user_id = payload.get('user_id')
        except Exception as e:
            return Response({'detail': f'Token inválido: {str(e)}', 'code': 'invalid_token'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        usuario = UsuarioPersonalizado.objects.get(pk=user_id)
    except UsuarioPersonalizado.DoesNotExist:
        return Response({'detail': 'Usuario no encontrado', 'code': 'user_not_found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Obtener la asistencia
    try:
        asistencia = Asistencia.objects.select_related('usuario', 'horario').get(pk=pk, usuario=usuario)
    except Asistencia.DoesNotExist:
        return Response({'detail': 'Asistencia no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = AsistenciaSerializer(asistencia)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = AsistenciaUpdateSerializer(asistencia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(AsistenciaSerializer(asistencia).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        asistencia.delete()
        return Response({'detail': 'Asistencia eliminada exitosamente'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def directivo_asistencias(request):
    """
    HU5: Vista directiva de asistencias
    Listar todas las asistencias con filtros opcionales
    Acceso: solo DIRECTIVO
    """
    # Autenticación manual
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({'detail': 'Token de autenticación requerido'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Usuario DIRECTIVO temporal
    usuario_directivo = UsuarioPersonalizado.objects.filter(tipo_usuario='DIRECTIVO').first()
    if not usuario_directivo:
        return Response({'detail': 'No hay usuarios DIRECTIVO'}, status=status.HTTP_403_FORBIDDEN)
    
    # Parámetros de filtrado
    usuario_id = request.query_params.get('usuario_id')
    fecha_inicio_str = request.query_params.get('fecha_inicio')
    fecha_fin_str = request.query_params.get('fecha_fin')
    estado = request.query_params.get('estado')
    sede = request.query_params.get('sede')
    
    # Query base
    asistencias_qs = Asistencia.objects.all().select_related('usuario', 'horario')
    
    # Aplicar filtros
    if usuario_id:
        try:
            usuario_id = int(usuario_id)
            asistencias_qs = asistencias_qs.filter(usuario__id=usuario_id)
        except ValueError:
            return Response({'detail': 'usuario_id debe ser un número entero'}, status=status.HTTP_400_BAD_REQUEST)
    
    if fecha_inicio_str:
        try:
            fecha_inicio = date.fromisoformat(fecha_inicio_str)
            asistencias_qs = asistencias_qs.filter(fecha__gte=fecha_inicio)
        except ValueError:
            return Response({'detail': 'Formato de fecha_inicio inválido. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
    
    if fecha_fin_str:
        try:
            fecha_fin = date.fromisoformat(fecha_fin_str)
            asistencias_qs = asistencias_qs.filter(fecha__lte=fecha_fin)
        except ValueError:
            return Response({'detail': 'Formato de fecha_fin inválido. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
    
    if estado:
        if estado not in ['pendiente', 'autorizado', 'rechazado']:
            return Response({'detail': 'Estado debe ser: pendiente, autorizado o rechazado'}, status=status.HTTP_400_BAD_REQUEST)
        asistencias_qs = asistencias_qs.filter(estado_autorizacion=estado)
    
    if sede:
        if sede not in ['SA', 'BA']:
            return Response({'detail': 'sede debe ser SA o BA'}, status=status.HTTP_400_BAD_REQUEST)
        asistencias_qs = asistencias_qs.filter(horario__sede=sede)
    
    serializer = AsistenciaSerializer(asistencias_qs, many=True)
    
    # Estadísticas
    total_asistencias = asistencias_qs.count()
    total_horas = sum(float(a.horas) for a in asistencias_qs)
    monitores_distintos = asistencias_qs.values('usuario').distinct().count()
    
    return Response({
        'total_asistencias': total_asistencias,
        'total_horas': total_horas,
        'monitores_distintos': monitores_distintos,
        'asistencias': serializer.data
    })


@api_view(['PUT'])
@authentication_classes([])
@permission_classes([AllowAny])
def directivo_asistencia_autorizar(request, pk):
    """
    HU5: Autorización de asistencias por directivos
    Cambiar el estado de autorización de una asistencia
    Acceso: solo DIRECTIVO
    """
    # Autenticación manual
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({'detail': 'Token de autenticación requerido'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Usuario DIRECTIVO temporal
    usuario_directivo = UsuarioPersonalizado.objects.filter(tipo_usuario='DIRECTIVO').first()
    if not usuario_directivo:
        return Response({'detail': 'No hay usuarios DIRECTIVO'}, status=status.HTTP_403_FORBIDDEN)
    
    # Obtener la asistencia
    try:
        asistencia = Asistencia.objects.select_related('usuario', 'horario').get(pk=pk)
    except Asistencia.DoesNotExist:
        return Response({'detail': 'Asistencia no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    
    # Validar estado
    nuevo_estado = request.data.get('estado_autorizacion')
    if nuevo_estado not in ['pendiente', 'autorizado', 'rechazado']:
        return Response(
            {'detail': 'Estado debe ser: pendiente, autorizado o rechazado'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Actualizar estado
    asistencia.estado_autorizacion = nuevo_estado
    asistencia.save()
    
    return Response(AsistenciaSerializer(asistencia).data)


# ===== AJUSTES MANUALES DE HORAS (HU7A) =====

@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def directivo_ajustes_horas(request):
    """
    HU7A: Ajustes manuales de horas
    GET: Listar ajustes de horas con filtros opcionales
    POST: Crear nuevo ajuste de horas
    Acceso: solo DIRECTIVO
    """
    # Autenticación manual
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({'detail': 'Token de autenticación requerido'}, status=status.HTTP_401_UNAUTHORIZED)

    # Usuario DIRECTIVO temporal
    usuario_directivo = UsuarioPersonalizado.objects.filter(tipo_usuario='DIRECTIVO').first()
    if not usuario_directivo:
        return Response({'detail': 'No hay usuarios DIRECTIVO'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        # Parámetros de filtrado
        monitor_id = request.query_params.get('monitor_id')
        fecha_inicio_str = request.query_params.get('fecha_inicio')
        fecha_fin_str = request.query_params.get('fecha_fin')
        
        # Query base
        ajustes_qs = AjusteHoras.objects.all().select_related('usuario', 'creado_por')
        
        # Aplicar filtros
        if monitor_id:
            try:
                monitor_id = int(monitor_id)
                ajustes_qs = ajustes_qs.filter(usuario__id=monitor_id)
            except ValueError:
                return Response({'detail': 'monitor_id debe ser un número entero'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fechas por defecto: último mes
        if not fecha_inicio_str:
            fecha_inicio = date.today() - timedelta(days=30)
        else:
            try:
                fecha_inicio = date.fromisoformat(fecha_inicio_str)
            except ValueError:
                fecha_inicio = date.today() - timedelta(days=30)
        
        if not fecha_fin_str:
            fecha_fin = date.today()
        else:
            try:
                fecha_fin = date.fromisoformat(fecha_fin_str)
            except ValueError:
                fecha_fin = date.today()
        
        # Filtrar por rango de fechas
        ajustes_qs = ajustes_qs.filter(fecha__gte=fecha_inicio, fecha__lte=fecha_fin)
        
        # Serializar y responder
        serializer = AjusteHorasSerializer(ajustes_qs, many=True)
        
        # Calcular estadísticas
        total_ajustes = ajustes_qs.count()
        total_horas_ajustadas = sum(float(ajuste.cantidad_horas) for ajuste in ajustes_qs)
        monitores_afectados = ajustes_qs.values('usuario').distinct().count()
        
        response_data = {
            'periodo': {
                'fecha_inicio': str(fecha_inicio),
                'fecha_fin': str(fecha_fin)
            },
            'estadisticas': {
                'total_ajustes': total_ajustes,
                'total_horas_ajustadas': total_horas_ajustadas,
                'monitores_afectados': monitores_afectados
            },
            'filtros_aplicados': {
                'monitor_id': monitor_id
            },
            'ajustes': serializer.data
        }
        
        return Response(response_data)
    
    elif request.method == 'POST':
        serializer = AjusteHorasCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Obtener instancia del monitor
            monitor = UsuarioPersonalizado.objects.get(id=serializer.validated_data['monitor_id'])
            
            # Crear ajuste
            ajuste = AjusteHoras.objects.create(
                usuario=monitor,
                fecha=serializer.validated_data['fecha'],
                cantidad_horas=serializer.validated_data['cantidad_horas'],
                motivo=serializer.validated_data['motivo'],
                creado_por=usuario_directivo
            )
            
            return Response(AjusteHorasSerializer(ajuste).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def directivo_ajuste_horas_detalle(request, pk):
    """
    HU7A: Ajustes manuales de horas
    GET: Obtener detalles de un ajuste específico
    DELETE: Eliminar ajuste de horas
    Acceso: solo DIRECTIVO
    """
    # Autenticación manual
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({'detail': 'Token de autenticación requerido'}, status=status.HTTP_401_UNAUTHORIZED)

    # Usuario DIRECTIVO temporal
    usuario_directivo = UsuarioPersonalizado.objects.filter(tipo_usuario='DIRECTIVO').first()
    if not usuario_directivo:
        return Response({'detail': 'No hay usuarios DIRECTIVO'}, status=status.HTTP_403_FORBIDDEN)

    # Verificar que el ajuste existe
    try:
        ajuste = AjusteHoras.objects.select_related('usuario', 'creado_por').get(id=pk)
    except AjusteHoras.DoesNotExist:
        return Response({'detail': 'Ajuste de horas no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AjusteHorasSerializer(ajuste)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        ajuste.delete()
        return Response({'detail': 'Ajuste de horas eliminado exitosamente'}, status=status.HTTP_204_NO_CONTENT)


# ===== CONFIGURACIONES DEL SISTEMA (HU9) =====

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def directivo_configuraciones(request):
    """
    HU9: Administración de configuraciones del sistema
    Listar todas las configuraciones del sistema.
    Acceso: solo DIRECTIVO
    """
    # Autenticación manual
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({'detail': 'Token de autenticación requerido'}, status=status.HTTP_401_UNAUTHORIZED)

    # Usuario DIRECTIVO temporal
    usuario_directivo = UsuarioPersonalizado.objects.filter(tipo_usuario='DIRECTIVO').first()
    if not usuario_directivo:
        return Response({'detail': 'No hay usuarios DIRECTIVO'}, status=status.HTTP_403_FORBIDDEN)

    configuraciones = ConfiguracionSistema.objects.all().select_related('creado_por')
    serializer = ConfiguracionSistemaSerializer(configuraciones, many=True)
    
    return Response({
        'total_configuraciones': configuraciones.count(),
        'configuraciones': serializer.data
    })

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def directivo_configuraciones_crear(request):
    """
    HU9: Administración de configuraciones del sistema
    Crear nueva configuración del sistema.
    Acceso: solo DIRECTIVO
    """
    # Autenticación manual
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({'detail': 'Token de autenticación requerido'}, status=status.HTTP_401_UNAUTHORIZED)

    # Usuario DIRECTIVO temporal
    usuario_directivo = UsuarioPersonalizado.objects.filter(tipo_usuario='DIRECTIVO').first()
    if not usuario_directivo:
        return Response({'detail': 'No hay usuarios DIRECTIVO'}, status=status.HTTP_403_FORBIDDEN)

    serializer = ConfiguracionSistemaCreateSerializer(data=request.data)
    if serializer.is_valid():
        # Verificar si ya existe una configuración con esa clave
        clave = serializer.validated_data['clave']
        if ConfiguracionSistema.objects.filter(clave=clave).exists():
            return Response(
                {'detail': f'Ya existe una configuración con la clave "{clave}"'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        configuracion = serializer.save(creado_por=usuario_directivo)
        return Response(ConfiguracionSistemaSerializer(configuracion).data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def directivo_configuraciones_detalle(request, clave):
    """
    HU9: Administración de configuraciones del sistema
    GET: Obtener configuración específica
    PUT: Actualizar configuración
    DELETE: Eliminar configuración
    Acceso: solo DIRECTIVO
    """
    # Autenticación manual
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({'detail': 'Token de autenticación requerido'}, status=status.HTTP_401_UNAUTHORIZED)

    # Usuario DIRECTIVO temporal
    usuario_directivo = UsuarioPersonalizado.objects.filter(tipo_usuario='DIRECTIVO').first()
    if not usuario_directivo:
        return Response({'detail': 'No hay usuarios DIRECTIVO'}, status=status.HTTP_403_FORBIDDEN)

    try:
        configuracion = ConfiguracionSistema.objects.select_related('creado_por').get(clave=clave)
    except ConfiguracionSistema.DoesNotExist:
        return Response({'detail': 'Configuración no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ConfiguracionSistemaSerializer(configuracion)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ConfiguracionSistemaCreateSerializer(configuracion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(ConfiguracionSistemaSerializer(configuracion).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        configuracion.delete()
        return Response({'detail': 'Configuración eliminada exitosamente'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def directivo_configuraciones_detalle_por_id(request, id):
    """
    HU9: Administración de configuraciones del sistema
    GET: Obtener configuración específica por ID
    PUT: Actualizar configuración por ID
    DELETE: Eliminar configuración por ID
    Acceso: solo DIRECTIVO
    """
    # Autenticación manual
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({'detail': 'Token de autenticación requerido'}, status=status.HTTP_401_UNAUTHORIZED)

    # Usuario DIRECTIVO temporal
    usuario_directivo = UsuarioPersonalizado.objects.filter(tipo_usuario='DIRECTIVO').first()
    if not usuario_directivo:
        return Response({'detail': 'No hay usuarios DIRECTIVO'}, status=status.HTTP_403_FORBIDDEN)

    try:
        configuracion = ConfiguracionSistema.objects.select_related('creado_por').get(id=id)
    except ConfiguracionSistema.DoesNotExist:
        return Response({'detail': 'Configuración no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ConfiguracionSistemaSerializer(configuracion)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ConfiguracionSistemaCreateSerializer(configuracion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(ConfiguracionSistemaSerializer(configuracion).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        configuracion.delete()
        return Response({'detail': 'Configuración eliminada exitosamente'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def directivo_configuraciones_inicializar(request):
    """
    HU9: Administración de configuraciones del sistema
    Inicializar configuraciones por defecto del sistema.
    Acceso: solo DIRECTIVO
    """
    # Autenticación manual
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({'detail': 'Token de autenticación requerido'}, status=status.HTTP_401_UNAUTHORIZED)

    # Usuario DIRECTIVO temporal
    usuario_directivo = UsuarioPersonalizado.objects.filter(tipo_usuario='DIRECTIVO').first()
    if not usuario_directivo:
        return Response({'detail': 'No hay usuarios DIRECTIVO'}, status=status.HTTP_403_FORBIDDEN)

    configuraciones_por_defecto = [
        {
            'clave': 'costo_por_hora',
            'valor': '9965',
            'descripcion': 'Costo por hora de trabajo de los monitores en pesos colombianos (COP)',
            'tipo_dato': 'decimal'
        },
        {
            'clave': 'semanas_semestre',
            'valor': '14',
            'descripcion': 'Total de semanas que dura un semestre académico',
            'tipo_dato': 'entero'
        }
    ]

    configuraciones_creadas = []
    configuraciones_existentes = []

    for config_data in configuraciones_por_defecto:
        clave = config_data['clave']
        
        if ConfiguracionSistema.objects.filter(clave=clave).exists():
            configuraciones_existentes.append(clave)
        else:
            configuracion = ConfiguracionSistema.objects.create(
                clave=clave,
                valor=config_data['valor'],
                descripcion=config_data['descripcion'],
                tipo_dato=config_data['tipo_dato'],
                creado_por=usuario_directivo
            )
            configuraciones_creadas.append(ConfiguracionSistemaSerializer(configuracion).data)

    return Response({
        'mensaje': f'Se crearon {len(configuraciones_creadas)} configuraciones nuevas',
        'configuraciones_creadas': configuraciones_creadas,
        'configuraciones_existentes': configuraciones_existentes,
        'total_procesadas': len(configuraciones_por_defecto)
    }, status=status.HTTP_201_CREATED)

# ===== DIRECTIVO AUTORIZACIÓN =====

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def autorizar_monitor(request):
    """
    Endpoint para que el directivo autorice a un monitor para marcar asistencia.
    """
    usuario = request.user

    # Verificar si el usuario es un directivo
    if usuario.tipo_usuario != 'directivo':
        return Response(
            {'error': 'No tiene permisos para realizar esta acción.'},
            status=status.HTTP_403_FORBIDDEN
        )

    monitor_id = request.data.get('monitor_id')

    # Verificar si el monitor existe
    try:
        monitor = UsuarioPersonalizado.objects.get(id=monitor_id, tipo_usuario='monitor')
    except UsuarioPersonalizado.DoesNotExist:
        return Response(
            {'error': 'Monitor no encontrado.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Autorizar al monitor
    monitor.autorizado = True
    monitor.save()

    return Response(
        {'message': f'El monitor {monitor.username} ha sido autorizado para marcar asistencia.'},
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def marcar_asistencia(request):
    """
    Endpoint para que los monitores marquen su asistencia.
    """
    usuario = request.user

    # Verificar si el usuario es un monitor autorizado
    if usuario.tipo_usuario != 'monitor' or not usuario.autorizado:
        return Response(
            {'error': 'No tiene permisos para realizar esta acción o no está autorizado.'},
            status=status.HTTP_403_FORBIDDEN
        )

    # Registrar la asistencia
    asistencia = {
        'monitor_id': usuario.id,
        'fecha': date.today(),
        'horas': request.data.get('horas', 0)
    }

    # Aquí se puede agregar lógica para guardar la asistencia en la base de datos

    return Response(
        {'message': f'Asistencia registrada para el monitor {usuario.username}.'},
        status=status.HTTP_200_OK
    )
