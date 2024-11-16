from django.db import models

class abiturient(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    token = models.CharField(max_length=255, null=False)
    first_name = models.CharField(max_length=100, null=False)
    second_name = models.CharField(max_length=100, null=False)
    is_admin = models.BooleanField(default=False)
    has_diplom_original = models.BooleanField(default=False)
    is_requested = models.BooleanField(default=False)
    is_enrolled = models.BooleanField(default=False)

    class Meta:
        db_table = 'abiturients'
        managed = True

class direction(models.Model):
    id = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=255, null=False)
    budget_places_number = models.IntegerField(null=False)
    min_ball = models.IntegerField(null=False)
    is_filled = models.BooleanField(default=False)
    is_finalized = models.BooleanField(default=False)

    class Meta:
        db_table = 'directions'
        managed = True

class abiturient_direction_link(models.Model):
    id = models.AutoField(primary_key=True)
    abiturient = models.ForeignKey('abiturient', on_delete=models.CASCADE)
    direction = models.ForeignKey('direction', on_delete=models.CASCADE)
    place = models.IntegerField(default=0, null=False)
    mark = models.IntegerField(default=0, null=False)
    admission_status = models.CharField(max_length=255, default='request_in_progress', null=False)
    prioritet_number = models.IntegerField(default=1, null=False)
    has_diplom_original = models.BooleanField(default=False)

    class Meta:
        db_table = 'abiturient_direction_links'
        managed = True