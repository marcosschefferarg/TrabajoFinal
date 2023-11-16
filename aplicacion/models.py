from django.db import models

class BandaHoraria(models.Model):
    nombre = models.CharField(max_length=255)
    horario_inicio = models.DateTimeField()
    horario_fin = models.DateTimeField()
    
    def __str__(self):
        return self.nombre

class Curso(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    banda_horaria = models.ForeignKey(BandaHoraria, on_delete = models.CASCADE)
    nota = models.IntegerField()   
    
    def __str__(self):
        return self.nombre

class Alumno(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    dni = models.IntegerField(primary_key=True) 
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField()
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f'{self.nombre} {self.apellido}'
    
