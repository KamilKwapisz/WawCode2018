from django.db import models
from django.contrib.auth.models import User


class Uzytkownik(models.Model):
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
    lokalizacjaNS = models.FloatField()
    lokalizacjaWE = models.FloatField()
    cenaPiwa = models.FloatField()
    cenaWodki = models.FloatField()
    jedzenie = models.BooleanField()
    regionalne = models.BooleanField()
    karaoke = models.BooleanField()
    godzinyOtwarcia = models.TextField()
    palarnia = models.BooleanField()
    ogrodek = models.BooleanField()
    ladowanieTelefonu = models.BooleanField()
    parkiet = models.BooleanField()
    mecze = models.BooleanField()

    def __str__(self):
        return str(self.nazwa)


class Komentarz(models.Model):
    nick = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)
    lokal = models.ForeignKey(Lokal, on_delete=models.CASCADE)
    tekst = models.CharField(max_length=100)
    ileGwiazdek = models.IntegerField()

    def __str__(self):
        return str(self.nick)


class WydarzenieLokalu(models.Model):
    lokal = models.ForeignKey(Lokal, on_delete=models.CASCADE)
    tytul = models.CharField(max_length=40)
    opis = models.CharField(max_length=100)
    godzinaOd = models.DateTimeField()

    def __str__(self):
        return str(self.tytul)


class Polubienie(models.Model):
    lokal = models.ForeignKey(Lokal, on_delete=models.CASCADE)
    nick = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)

    def __str__(self):
        return str(' lubi '.join(self.nick, self.lokal))


class Wlasciciel(models.Model):
    wlasciciel = models.OneToOneField(User, on_delete=models.CASCADE)
    lokal = models.ForeignKey(Lokal, on_delete=models.CASCADE)

    def __str__(self):
        return str(' jest wlascicielem '.join([self.wlasciciel.username, self.lokal.nazwa]))
