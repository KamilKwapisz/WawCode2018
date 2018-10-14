from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.username)


class UserEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tytul = models.CharField(max_length=40)
    opis = models.CharField(max_length=100)
    lokalizacjaNS = models.FloatField()
    lokalizacjaWE = models.FloatField()
    dataOd = models.DateTimeField()

    def __str__(self):
        return str(self.tytul)


class Lokal(models.Model):
    nazwa = models.CharField(max_length=40)
    adres = models.CharField(max_length=200)
    coordinates = models.CharField(max_length=100, blank=True, null=True)
    cenaPiwa = models.FloatField(blank=True, null=True)
    cenaWodki = models.FloatField(blank=True, null=True)
    jedzenie = models.BooleanField(default=False)
    regionalne = models.BooleanField(default=False)
    karaoke = models.BooleanField(default=False)
    godzinyOtwarcia = models.TextField()
    palarnia = models.BooleanField(default=False)
    ogrodek = models.BooleanField(default=False)
    ladowanieTelefonu = models.BooleanField()
    parkiet = models.BooleanField(default=False)
    mecze = models.BooleanField(default=False)
    jaki_mecz = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.nazwa)

    def get_absolute_url(self):
        return reverse('chlanie:lokal-detail', kwargs={'pk': self.id})


class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lokal = models.ForeignKey(Lokal, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    created = models.DateTimeField(editable=False, default=timezone.now())

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(Rate, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} ocenił lokal {self.lokal.nazwa} na {self.rating} gwiazdek"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    lokal = models.ForeignKey(Lokal, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    created = models.DateTimeField(editable=False, default=timezone.now())

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)


class WydarzenieLokalu(models.Model):
    lokal = models.ForeignKey(Lokal, on_delete=models.CASCADE)
    tytul = models.CharField(max_length=40)
    opis = models.CharField(max_length=100)
    godzinaOd = models.DateTimeField()

    def __str__(self):
        return str(self.tytul)


class Like(models.Model):
    lokal = models.ForeignKey(Lokal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False, default=timezone.now())

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} polubił {self.lokal}"


class Wlasciciel(models.Model):
    wlasciciel = models.OneToOneField(User, on_delete=models.CASCADE)
    lokal = models.ForeignKey(Lokal, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.wlasciciel.username} polubił {self.lokal.nazwa}"
