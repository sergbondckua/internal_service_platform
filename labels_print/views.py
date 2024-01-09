import copy

from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from reportlab.lib.units import cm

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
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
from labels_print.forms import TagKeyFormSet, TagCellForm


class TagKeyView:
    """Create a new tag key."""

    pass


def tag_key_view(request):
    template_name = "labels_print/tag_key.html"
    heading_message = "Formset Demo"
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
        super().__init__(*args, **kwargs)
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
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        page = f"Powered by: Serhii Bondarenko. Сторінка {self._pageNumber} із {page_count}"
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
    addresses = cell_instance.buildings.all()

    filename = cell_instance.title + "_results.pdf"
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename='{filename}'"

    register_fonts()
    add_font_mappings()

    doc = SimpleDocTemplate(
        response,
        pagesize=landscape(A4),
        rightMargin=10,
        leftMargin=10,
        topMargin=50,
        bottomMargin=80,
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
    styles.add(
        ParagraphStyle(
            name="Label",
            alignment=TA_LEFT,
            fontName="Roboto",
            fontSize=13,
            wordWrap=True,
        )
    )

    table_style = [
        # ("WORD_WRAP", (0, 0), (-1, -1)),
        ("FONT", (0, 0), (-1, -1), "Roboto", 12),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("ALIGN", (0, 2), (-1, 2), "CENTER"),
        ("ALIGN", (0, 4), (-1, 4), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        # ("SPAN", (0, 0), (-1, 0)),  # Merge cells in the first row
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.white),
        # ("NO_SPLIT", (0, 0), (-1, -1)),
    ]

    doc_title = copy.copy(styles["Heading1"])
    doc_title.alignment = TA_CENTER
    doc_title.fontName = "Roboto-Bold"
    doc_title.fontSize = 20
    title = ""
    story.append(Paragraph(title, doc_title))

    street_buildings_map = {}
    for address in addresses:
        street_name = (
            address.street.name
            if not address.street.old_name
            else f"{address.street.name} ({address.street.old_name})"
        )
        number = address.number

        if street_name not in street_buildings_map:
            street_buildings_map[street_name] = [number]
        else:
            street_buildings_map[street_name].append(number)

    street_building_summary = {
        street: ", ".join(numbers)
        for street, numbers in street_buildings_map.items()
    }

    street_building_text = "\n".join(
        [
            f"<b>{key}</b>:\n   • {value}"
            for key, value in street_building_summary.items()
        ]
    )

    label_data = [
        [
            "Column 1",
            "Column 2",
            "Column 3",
            "Column 4",
            "Column 5",
            "Column 6",
            "Column 3",
            "Column 4",
            "Column 5",
            "Column 6",
        ],
        [
            "Data 1",
            "Data 2",
            "Data 3",
            "Data 4",
            "Data 5",
            "Data 6",
            "Data 3",
            "Data 4",
            "Data 5",
            "Data 6",
        ],
    ]
    new_data = []

    for i in range(0, len(label_data[0]), 3):
        new_data.append(label_data[0][i : i + 3])
        new_data.append(label_data[1][i : i + 3])

    # Specify column widths and row heights
    column_widths = [8.5 * cm, 8.5 * cm, 8.5 * cm]
    row_heights = [0.6 * cm, 4.5 * cm] * (len(new_data) // 2)

    # Create the table with specified column widths and row heights
    table = Table(new_data, colWidths=column_widths, rowHeights=row_heights)

    table.setStyle(TableStyle(table_style))
    story.append(table)
    story.append(Spacer(1, 10))
    doc_title.fontSize = 12

    doc.build(story, canvasmaker=PageNumCanvas)
    return response


class TagCellFormView(generic.FormView, generic.TemplateView):
    template_name = "labels_print/tag_cell_print.html"
    form_class = TagCellForm

    # def form_valid(self, form):
    #     selected_cells = form.cleaned_data["tags"]
    #     cell_groups = self.group_cells_by_street(selected_cells)
    #     return self.render_to_response(
    #         self.get_context_data(form=form, cell_groups=cell_groups)
    #     )

    def form_valid(self, form):
        selected_cells = form.cleaned_data["tags"]
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "filename=label_print.pdf"
        self.conclusion_to_pdf(response, selected_cells)
        return response

    def conclusion_to_pdf(self, response, selected_cells):
        register_fonts()
        add_font_mappings()

        doc = SimpleDocTemplate(
            response,
            pagesize=landscape(A4),
            rightMargin=10,
            leftMargin=10,
            topMargin=60,
            bottomMargin=80,
            title="Друк наліпок для комірок",
        )

        story = []

        styles = getSampleStyleSheet()
        styles.add(
            ParagraphStyle(
                name="Center",
                alignment=TA_CENTER,
                fontName="Roboto",
                wordWrap=True,
            )
        )
        styles.add(
            ParagraphStyle(
                name="Label",
                alignment=TA_LEFT,
                fontName="Roboto",
                fontSize=12,
                leading=15,
                wordWrap=True,
            )
        )

        table_style = [
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
            # ("BOX", (0, 0), (-1, -1), 2, colors.black),
        ]

        cell_groups = self.group_cells_by_street(selected_cells)
        label_data = []
        cell_group_headers = [
            Paragraph(cell_name, styles["Center"])
            for cell_name in list(cell_groups.keys())
        ]
        label_data.append(cell_group_headers)

        street_building_paragraphs = []
        street_building_summary = ""
        for _, cell_group in cell_groups.items():
            street_buildings_info = []
            for street, building_numbers in cell_group.items():
                street_buildings_info.append(
                    f"<b>{street}:</b>\n• {', '.join(building_numbers)}\n"
                )
                street_building_summary = " ".join(street_buildings_info)
            street_building_paragraphs.append(
                Paragraph(
                    street_building_summary.replace("\n", "<br />\n"),
                    styles["Label"],
                )
            )

        # Create table for label information
        label_data.append(street_building_paragraphs)

        new_data = []

        for i in range(0, len(label_data[0]), 3):
            new_data.append(label_data[0][i : i + 3])
            new_data.append(label_data[1][i : i + 3])

        # Specify column widths and row heights
        column_widths = [8.5 * cm, 8.5 * cm, 8.5 * cm]
        row_heights = [0.6 * cm, 4.5 * cm] * (len(new_data) // 2)

        # Create the table with specified column widths and row heights
        table = Table(
            new_data, colWidths=column_widths, rowHeights=row_heights
        )

        table.setStyle(TableStyle(table_style))

        doc_title = copy.copy(styles["Heading1"])
        doc_title.alignment = TA_CENTER
        doc_title.fontName = "Roboto-Bold"
        doc_title.fontSize = 10
        title = ""
        story.append(Paragraph(title, doc_title))
        story.append(table)
        story.append(Spacer(1, 10))
        doc_title.fontSize = 12

        doc.build(story, canvasmaker=PageNumCanvas)

    @staticmethod
    def group_cells_by_street(selected_cells: QuerySet) -> dict:
        cell_groups = {}

        for cell in selected_cells:
            cell_name = f"{cell.title} ({cell.box})"
            if cell_name not in cell_groups:
                cell_groups[cell_name] = {}

            for street in cell.buildings.all():
                street_old = (
                    f"({street.street.old_name})"
                    if street.street.old_name
                    else ""
                )
                street_name = f"{street.street.name} {street_old}"
                if street_name not in cell_groups[cell_name]:
                    cell_groups[cell_name][street_name] = []
                cell_groups[cell_name][street_name].append(street.number)

        return cell_groups
