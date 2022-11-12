from django.db.models import TextChoices

class FrontendEvents(TextChoices):
    BLANK = '-', '-'
    CLICK = 'click', 'Click'
    FOCUS = 'focus', 'Select'
    BLUR = 'blur', 'Blur'
    HOVER = 'mouseenter', 'Hover'
    LEAVE = 'mouseleave', 'Leave'
    SELECT = 'select', 'Select'
    SUBMIT = 'submit', 'Submit'
    COPY = 'copy', 'Copy'
    VIEW = 'view', 'View'
    CONVERSION = 'conversion', 'Conversion'


class ElementTypes(TextChoices):
    UNKNOWN = '-', '-'
    BUTTON = 'BUTTON', 'Button'
    A = 'A', 'Button'
    P = 'P', 'Paragraph'
    H1 = 'H1', 'Heading'
    H2 = 'H2', 'Heading'
    H3 = 'H3', 'Heading'
    H4 = 'H4', 'Heading'
    H5 = 'H5', 'Heading'
    H6 = 'H6', 'Heading'
    DIV = 'DIV', 'Text'
    SPAN = 'SPAN', 'Text'
    SUBMIT = 'submit', 'Button'
