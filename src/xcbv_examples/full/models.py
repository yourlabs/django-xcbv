from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Pet(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Toy(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(Pet, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
