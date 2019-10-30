# for additional validation

# from django.db import models
# from django.core.validators import MinValueValidator, EmailValidator

# class Person(models.Model):
#     name = models.CharField(max_length=10)
#     age = models.IntegerField(
#         validators=[MinValueValidator(20, message='미성년자 출입금지')]
#     )
#     email = models.CharField(max_length=120,
#         validators=[EmailValidator(message='이메일 형식이 아닙니다.')]
#     )