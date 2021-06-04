from django.db import models




# Create your models here.
class Diagnostico(models.Model):
    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre


class Zona(models.Model):
    codigo = models.IntegerField(default=0)
    def __str__(self):
        return self.codigo.__str__()



class Centro(models.Model):
    codigo = models.IntegerField(default=0)
    nombre = models.CharField(max_length=100)
    zona = models.ForeignKey(Zona,on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre


edades = [('1', '1'),
    ('1 / 5', '1 a 5'),
    ('6 / 9', '6 a 9'),
    ('10 / 14', '10 a 14'),
    ('15 / 19', '15 a 19'),
    ('20 / 54 ', '20 a 54 '),
    ('55 /  64', '55 a  64'),
    ('65+', '65 y mas')]
sexo = (
       ('M', ('Masculino')),
       ('F', ('Femenino')),
       )

class Semana(models.Model):
    semana = models.IntegerField()
    year = models.IntegerField()
    creacion = models.DateTimeField(blank=True)




class Paciente(models.Model):
    
    sexo = models.CharField(choices=sexo,max_length=32)
    edad = models.CharField(choices=edades,max_length=32)
    diagnostico = models.ForeignKey(Diagnostico,on_delete=models.CASCADE,blank=True)
    centro = models.ForeignKey(Centro,on_delete=models.CASCADE,blank=True)
    semana = models.ForeignKey(Semana,on_delete=models.CASCADE,blank=True)
    creacion = models.DateTimeField(blank=True)
    def __str__(self):
        str = 'sexo ' + self.sexo + ' edad ' + self.edad + ' diagnostico ' + self.diagnostico.__str__()
        return str

class Archivo(models.Model):
    tabla = models.FileField( null=True)