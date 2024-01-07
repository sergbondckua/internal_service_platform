import copy

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from reportlab.lib.units import cm

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Table,
    TableStyle,
    Spacer,
)

from search_keys.models import Cell
from labels_print.forms import TagKeyFormSet


class TagKeyView:
    """Create a new tag key."""

    pass


def tag_key_view(request):
    data = None
    if request.method == "POST":
        formset = TagKeyFormSet(request.POST)
        if formset.is_valid():
            data = [form.cleaned_data for form in formset]
    else:
        formset = TagKeyFormSet()

    context = {"formset": formset, "data": data}
    return render(request, "labels_print/tag_key.html", context)


class PageNumCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(PageNumCanvas, self).__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        # Save the current page attributes before starting a new page
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        # Restore the saved page attributes and draw page numbers
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            super(PageNumCanvas, self).showPage()
        super(PageNumCanvas, self).save()

    def draw_page_number(self, page_count):
        page = "Страница %d из %d" % (self._pageNumber, page_count)
        self.setFont("Roboto", 9)
        self.drawRightString(A4[0] - 10, 10, page)


def register_fonts():
    fonts = [
        ("Roboto", "static/fonts/Roboto-Regular.ttf", "UTF-8"),
        ("Roboto-Bold", "static/fonts/Roboto-Bold.ttf", "UTF-8"),
        ("Roboto-Italic", "static/fonts/Roboto-Italic.ttf", "UTF-8"),
        ("Roboto-BoldItalic", "static/fonts/Roboto-BoldItalic.ttf", "UTF-8"),
    ]

    for font_name, font_path, encoding in fonts:
        pdfmetrics.registerFont(TTFont(font_name, font_path, encoding))


def add_font_mappings():
    addMapping("Roboto", 0, 0, "Roboto")  # normal
    addMapping("Roboto", 0, 1, "Roboto-Italic")  # italic
    addMapping("Roboto", 1, 0, "Roboto-Bold")  # bold
    addMapping("Roboto", 1, 1, "Roboto-BoldItalic")  # italic and bold


def conclusion_to_pdf(request, pk):
    cell_instance = get_object_or_404(Cell, id=pk)
    buildings = cell_instance.buildings.all()

    street_buildings = {}
    for building in buildings:
        street_name = building.street.name
        number = building.number

        if street_name not in street_buildings:
            street_buildings[street_name] = [number]
        else:
            street_buildings[street_name].append(number)

    result_data = {
        street: ", ".join(map(str, numbers))
        for street, numbers in street_buildings.items()
    }

    result_string = "\n".join(
        [f"{key}: {value}" for key, value in result_data.items()]
    )
    filename = cell_instance.title + "_results.pdf"
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="%s"' % filename

    register_fonts()
    add_font_mappings()

    doc = SimpleDocTemplate(
        response,
        pagesize=landscape(A4),
        rightMargin=10,
        leftMargin=10,
        topMargin=10,
        bottomMargin=10,
        title="Результаты",
    )

    story = []
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="Justify",
            alignment=TA_JUSTIFY,
            fontName="Roboto",
            fontSize=11,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Justify-Bold", alignment=TA_JUSTIFY, fontName="Roboto-Bold"
        )
    )
    table_style = [
        ("WORD_WRAP", (0, 0), (-1, -1)),
        ("FONT", (0, 0), (-1, -1), "Roboto", 9.5),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        # ("SPAN", (0, 0), (-1, 0)),  # Merge cells in the first row
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("NO_SPLIT", (0, 0), (-1, -1)),
    ]

    doc_title = copy.copy(styles["Heading1"])
    doc_title.alignment = TA_CENTER
    doc_title.fontName = "Roboto-Bold"
    doc_title.fontSize = 20
    title = "Друк комірок"
    story.append(Paragraph(title, doc_title))

    personal_data = [
        ["%s (%s)" % (cell_instance.title, cell_instance.box), "", ""],
        [result_string, "", ""],
    ]

    # Specify column widths and row heights
    column_widths = [8.176 * cm, 8.176 * cm]  # Adjust as needed
    row_heights = [0.6 * cm, 3.5 * cm]  # Adjust as needed

    # Create the table with specified column widths and row heights
    table = Table(
        personal_data, colWidths=column_widths, rowHeights=row_heights
    )

    table.setStyle(TableStyle(table_style))
    story.append(table)
    story.append(Spacer(1, 10))
    doc_title.fontSize = 12

    doc.build(story, canvasmaker=PageNumCanvas)
    return response
