from django.db import models

class GraduateAttribute(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name.__str__()

class CharacterStrength(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name.__str__()

class AttributeStrengthMap(models.Model):
    graduate_attribute = models.ForeignKey(GraduateAttribute, on_delete=models.CASCADE)
    character_strength = models.ForeignKey(CharacterStrength, on_delete=models.CASCADE)
    weight = models.FloatField()  # ✅ if you renamed this from value


class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    attributes = models.ManyToManyField(GraduateAttribute)
    def __str__(self):
        return self.name.__str__() + " - " + self.date.__str__()+ " - " + self.attributes.__str__()

class Student(models.Model):
    roll_no = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.roll_no.__str__() + " - " + self.name.__str__()

class Participation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    def __str__(self):
        return self.student.__str__() + " - " + self.event.__str__()