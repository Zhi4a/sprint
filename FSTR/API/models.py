from django.db import models


class MyUser(models.Model):
    fam = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    otc = models.CharField(max_length=50)
    phone = models.CharField(max_length=25)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f'{self.name}, {self.email}'


class Pass(models.Model):
    ADDED_STATUS = [
        ('new', 'новое'),
        ('pending', 'взято в работу'),
        ('accepted', 'успешно'),
        ('rejected', 'не принято'),
    ]

    created = models.DateTimeField(auto_now_add=True)
    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connect = models.CharField(max_length=255, blank=True)
    add_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=8, choices=ADDED_STATUS, default='new')

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    coordinates = models.ForeignKey('Coordinates', on_delete=models.CASCADE)
    levels = models.ForeignKey('Level', blank=True, on_delete=models.PROTECT)


class Coordinates(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()


class Level(models.Model):
    winter_level = models.CharField(max_length=3, blank=True)
    summer_level = models.CharField(max_length=3, blank=True)
    autumn_level = models.CharField(max_length=3, blank=True)
    spring_level = models.CharField(max_length=3, blank=True)


class Images(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=20)
    data = models.BinaryField()

    passes = models.ForeignKey(Pass, related_name='images', on_delete=models.CASCADE)
