from django.db import models

# Create your models here.

class ApiKey(models.Model):
    key = models.CharField(max_length=100)

    def __str__(self):
        return self.key

class Diagnostic(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    alert = models.BooleanField(default=False,null=True,blank=True)
    
    def __str__(self):
        return self.name


class Zone(models.Model):
    code = models.IntegerField(default=0)
    def __str__(self):
        return self.code.__str__()


class Center(models.Model):
    code = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    zone = models.ForeignKey(Zone,on_delete=models.CASCADE)
    latitude = models.FloatField(default=-31.4135,null=True)
    longitude = models.FloatField(default=-64.18105,null=True)
    def get_cases(self,diagnostic):
        diagnostic_cases = self.diagnostic_cases
        diagnostic_cases = diagnostic_cases.filter(diagnostic=diagnostic)
        cant = 0
        for diagnostic_case in diagnostic_cases:
            cant += diagnostic_case.cases
        return cant

    def __str__(self):
        return self.name

class SpreadSheet(models.Model):
    file = models.FileField( null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Year(models.Model):
    year = models.IntegerField()
    population = models.IntegerField(null=True,default=1)
    def __str__(self):
        return str(self.year)

class Week(models.Model):
    week = models.IntegerField()
    year = models.ForeignKey(Year,on_delete=models.CASCADE,null=False, related_name = "weeks") # default=1329604
    spread_sheet = models.ForeignKey(SpreadSheet,on_delete=models.CASCADE,blank=True, null=True)
    creation = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.year) + ' ' + str(self.week)

class Age(models.Model):
    from_age = models.IntegerField(unique=True)
    to_age = models.IntegerField(unique=True)
    def __str__(self):
        return 'De ' + str(self.from_age) + ' a ' + str(self.to_age)


ages = [( '<1','<1 a??o'),
    ( '1 a 5','1 a 5 a??os'),
    ( '6 a 9','6 a 9 a??os'),
    ( '10 a 14','10 a 14 a??os'),
    ('15 a 19','15 a 19 a??os'),
    ('20 a 54 ','20 a 54 a??os'),
    ('55 a 64','55 a 64 a??os'),
    ('65 y mas','65 y mas a??os')]

class Sex(models.Model):
    name = models.CharField(max_length=30,unique=True) #should be 'gender'
    def __str__(self):
        return str(self.name)

class DiagnosticCases(models.Model):
    sex = models.ForeignKey(Sex,on_delete=models.CASCADE,blank=True)
    age = models.ForeignKey(Age,on_delete=models.CASCADE,blank=True)
    cases = models.IntegerField()
    diagnostic = models.ForeignKey(Diagnostic,on_delete=models.CASCADE,blank=True)
    center = models.ForeignKey(Center,related_name="diagnostic_cases",on_delete=models.CASCADE,blank=True)
    week = models.ForeignKey(Week,on_delete=models.CASCADE,blank=True)
    creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        str = 'sex: ' + self.sex.name + ' age: ' + self.age.__str__() + ' diagnostic: ' + self.diagnostic.__str__()
        return str

    class Meta:
        verbose_name_plural = "Diagnostic cases"






