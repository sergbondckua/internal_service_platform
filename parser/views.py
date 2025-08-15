from django.views.generic import TemplateView


class PayStrParser(TemplateView):
    """ Парсинг платіжного рядка"""

    template_name = "parser/paystr.html"
