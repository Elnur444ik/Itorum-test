from django.core.validators import RegexValidator

phone_regex_validator = RegexValidator(regex=r"^7\d{10}$", message='Введен некорректный номер телефона')
code_regex_validator = RegexValidator(regex='^.{3}$', message='Введен некорректный код оператора')