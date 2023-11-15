import json
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from .models import Alumno, Curso
import csv

# Debe tener una URL/Endpoint llamada /cargarAlumnos que llame a una función
# de la vista que lea un archivo csv de alumnos (con columnas equivalentes a sus
# atributos) y guarde esos alumnos verificando que no se repitan por su clave
# primaria.
def cargar_Alumnos(request):
  if request.method == 'POST' and request.FILES.get['csv_file']:
        csv_file = request.FILES['csv_file']

        if csv_file.name.endswith('.csv'):
            try:
                decoded_file = csv_file.read().decode('utf-8')
                csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')
                next(csv_data)
                
                #uso el siguiente iterador para recorrer el archivo CSV y asi crear o actualizar el objeto Alumno
                for row in csv_data:
                    dni, nombre, apellido, telefono, correo_electronico, curso_id = row
                    # Verificar si el alumno ya existe por su clave primaria (DNI)
                    dni = int(row['DNI'])
                    if Alumno.objects.filter(dni=dni).exists():
                        continue  # Si el alumno ya existe, pasa al siguiente

                    # Crear un nuevo objeto Alumno
                    Alumno.objects.create(
                        nombre=row['Nombre'],
                        apellido=row['Apellido'],
                        dni=dni,
                        telefono=row['Teléfono'],
                        correo_electronico=row['Correo Electrónico'],
                        curso_id=int(row['Curso'])  # Asume que hay una columna 'Curso' en el CSV
                    )

                return JsonResponse({'message': 'Alumnos cargados exitosamente.'}, status=200)
            except Exception as e:
                return JsonResponse({'error': f'Ocurrió un error al procesar el archivo CSV: {str(e)}'}, status=500) #400??
  
  return JsonResponse({'error': 'Método no permitido o archivo no proporcionado.'}, status=405)

# Debe tener una URL/Endpoint llamada /listarAlumnos que llame a una función
# de la vista que liste esos alumnos.
def listar_alumnos(request):
    if request.method == 'GET':
        alumnos = Alumno.objects.all()

        # Serializa los datos de los alumnos en una lista de diccionarios
        serialized_alumnos = []
        for alumno in alumnos:
            serialized_alumnos.append({
                'nombre': alumno.nombre,
                'apellido': alumno.apellido,
                'dni': alumno.dni,
                'telefono': alumno.telefono,
                'correo_electronico': alumno.correo_electronico,
                'curso': alumno.curso.nombre if alumno.curso else None,
                'banda_horaria': alumno.curso.banda_horaria.nombre if alumno.curso else None,
            })

        return JsonResponse({'alumnos': serialized_alumnos})
    else:
        return JsonResponse({'error': 'Método no permitido. Utiliza el método GET para listar los alumnos.'}, status=405)    

# Debe tener una URL/Endpoint llamada /alumno que reciba el dni de un alumno
# por parámetro (GET) y retorne la información en formato csv del alumno
# incluidos el curso y la banda horaria.
def obtener_alumno(request, dni):
    if request.method == 'GET':
        alumno = get_object_or_404(Alumno, dni=dni)

        # Serializa los datos del alumno en un diccionario
        serialized_alumno = {
            'nombre': alumno.nombre,
            'apellido': alumno.apellido,
            'dni': alumno.dni,
            'telefono': alumno.telefono,
            'correo_electronico': alumno.correo_electronico,
            'curso': alumno.curso.nombre if alumno.curso else None,
            'banda_horaria': alumno.curso.banda_horaria.nombre if alumno.curso else None,
        }

        # Retorna la respuesta en formato JSON
        return JsonResponse({'alumno': serialized_alumno})
    else:
        return JsonResponse({'error': 'Método no permitido. Utiliza el método GET para obtener el alumno.'}, status=405)

# Endpoint para Modificar Alumnos: Crea un nuevo endpoint /modificarAlumno
# que permita la actualización de los datos de un alumno existente utilizando el
# método HTTP PUT. Esta función debe recibir el DNI del alumno y los datos
# actualizados en formato JSON para modificar el registro correspondiente en la
# base de datos. Debe verificar que el alumno exista y si no existe debe devolver
# el error HTTP correspondiente.
def modificar_alumno(request, dni):
    alumno = get_object_or_404(Alumno, dni=dni)

    if request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))

            # Actualiza los campos del alumno con los datos proporcionados
            alumno.nombre = data.get('nombre', alumno.nombre)
            alumno.apellido = data.get('apellido', alumno.apellido)
            alumno.telefono = data.get('telefono', alumno.telefono)
            alumno.correo_electronico = data.get('correo_electronico', alumno.correo_electronico)
            alumno.curso.descripcion = data.get('curso_descripcion', alumno.curso.descripcion)
            alumno.curso.banda_horaria.nombre = data.get('banda_nombre', alumno.curso.banda_horaria.nombre)
            alumno.curso.banda_horaria.horario_inicio = data.get('horario_inicio', alumno.curso.banda_horaria.horario_inicio)
            alumno.curso.banda_horaria.horario_fin = data.get('horario_fin', alumno.curso.banda_horaria.horario_fin)
            alumno.curso.nota = data.get('nota', alumno.curso.nota)
            
            # Guarda el registro actualizado en la base de datos
            alumno.save()

            return JsonResponse({'message': 'Alumno modificado correctamente.'}, status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Error en el formato JSON de la solicitud.'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido. Utiliza el método PUT para modificar al alumno.'}, status=405)

# Endpoint para Eliminar Alumnos: Implementa un endpoint /eliminarAlumno que
# permita la eliminación de un alumno existente utilizando el método HTTP
# DELETE. Al recibir el DNI de un alumno por parámetro en la URL del endpoint,
# la función correspondiente debe eliminar este registro de la base de datos.
# Debe verificar que el alumno exista y si no existe debe devolver el error HTTP
# correspondiente.
def eliminar_alumno(request, dni):
    alumno = get_object_or_404(Alumno, dni=dni)

    if request.method == 'DELETE':
        # Elimina el registro del alumno de la base de datos
        alumno.delete()

        return JsonResponse({'message': 'Alumno eliminado correctamente.'}, status=200)
    else:
        return JsonResponse({'error': 'Método no permitido. Utiliza el método DELETE para eliminar al alumno.'}, status=405)

# Endpoint para Asignar Curso a Alumnos: Crea una funcionalidad en la API que
# permita asignar un curso a un alumno en particular. Implementa un endpoint
# /asignarCurso que reciba el DNI del alumno y el ID del curso deseado para
# asociar el alumno con dicho curso. Debe verificar que el alumno y el curso
# existan y si no existen debe devolver el error HTTP correspondiente.
def asignar_curso(request, dni, id_curso):
    alumno = get_object_or_404(Alumno, dni=dni)
    curso = get_object_or_404(Curso, id=id_curso)

    if request.method == 'POST':
        # Asigna el curso al alumno
        alumno.curso = curso
        alumno.save()

        return JsonResponse({'message': f'Curso asignado correctamente al alumno con DNI {dni}.'}, status=200)
    else:
        return JsonResponse({'error': 'Método no permitido. Utiliza el método POST para asignar un curso al alumno.'}, status=405)
    
# Endpoint para Consultar Alumnos por Curso: Desarrolla un endpoint
# /alumnosPorCurso que reciba el ID del curso como parámetro (GET) y devuelva
# una lista de todos los alumnos matriculados en ese curso, proporcionando
# información básica de cada alumno en formato JSON.

def alumnos_por_curso(request, id_curso):
    # Filtra los alumnos que están matriculados en el curso específico
    if request.method == 'GET':
        alumnos = Alumno.objects.filter(curso_id=id_curso)

        # Serializa los datos de los alumnos en una lista de diccionarios
        serialized_alumnos = []
        for alumno in alumnos:
            serialized_alumnos.append({
                'nombre': alumno.nombre,
                'apellido': alumno.apellido,
                'dni': alumno.dni,
                'telefono': alumno.telefono,
                'correo_electronico': alumno.correo_electronico,
            })

        # Retorna la respuesta en formato JSON
        return JsonResponse({'alumnos': serialized_alumnos})
    else:
        return JsonResponse({'error': 'Método no permitido. Utiliza el método GET para consultar alumnos por curso.'}, status=405)