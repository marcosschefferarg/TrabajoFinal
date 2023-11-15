from django.urls import path
from . import views

urlpatterns = [
    path('cargar_Alumnos/', views.cargar_Alumnos, name='cargar_Alumnos'),
    path('listar_alumnos', views.listar_alumnos, name='listar_alumnos'),
    path('alumno/<int:dni>/', views.obtener_alumno, name='obtener_alumno'),
    path('modificarAlumno/<int:dni>/', views.modificar_alumno, name='modificar_alumno'),
    path('eliminarAlumno/<int:dni>/', views.eliminar_alumno, name='eliminar_alumno'),
    path('asignarCurso/<int:dni>/<int:id_curso>/', views.asignar_curso, name='asignar_curso'),
    path('alumnosPorCurso/<int:id_curso>/', views.alumnos_por_curso, name='alumnos_por_curso'),
]
