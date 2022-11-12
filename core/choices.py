from django.db.models import TextChoices

class Terms(TextChoices):
    ONE_TIME = '', 'One-time'
    MONTHLY = 'mo', "Monthly"
    YEARLY = 'yr', "Yearly"

class Actions(TextChoices):
    BLANK = '-', '-'
    VIEW = 'view', "View"
    HOVER = 'hover', 'Hover'
    LEAVE = 'leave', 'Leave'
    SELECT = 'select', 'Select'
    UNSELECT = 'unselect', 'Un-select'
    SIGNUP_HOVER = 'signup_hover', 'Sing Up Hover'
    SIGNUP_LEAVE = 'signup_leave', 'Sing Up Leave'
    SIGNUP_CLICK = 'signup_click', 'Sign Up Click'
    CONVERSION_HOVER = 'conversion_hover', 'Conversion Hover'
    CONVERSION_LEAVE = 'conversion_leave', 'Conversion Leave'
    CONVERSION_CLICK = 'conversion_click', 'Conversion Click'