import os

from django.conf import settings
from django.db.models import QuerySet
from django.http import HttpResponse

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Spacer,
    Paragraph,
)


class PDFGenerator:
    """Class for generating PDF documents."""

    FONT_PATH = os.path.join(settings.STATIC_DIR, "fonts")
    TABLE_STYLES = [
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
    ]
    COLUMN_WIDTH = 8.5 * cm
    ROW_HEIGHT = 4.1 * cm

    def __init__(self, http_response: HttpResponse, cell_data: QuerySet):
        self.http_response = http_response
        self.cell_data = cell_data
        self.styles = getSampleStyleSheet()

    def generate_pdf_doc(self):
        """Generate the PDF document."""
        self.register_and_mapping_fonts()
        self.set_sheet_styles()

        doc = self.create_base_document()
        cell_groups = self.get_cell_groups()
        label_data = self.get_label_data(cell_groups)
        table = self.create_table(label_data)
        story = [table, Spacer(1, 10)]
        doc.build(story)

    def create_base_document(self):
        """Create the base PDF document."""
        return SimpleDocTemplate(
            self.http_response,
            pagesize=landscape(A4),
            rightMargin=10,
            leftMargin=10,
            topMargin=60,
            bottomMargin=107,
            title="Друк наліпок для комірок",
        )

    def set_sheet_styles(self):
        """Set additional sheet styles."""
        self.styles.add(
            ParagraphStyle(
                name="Center",
                alignment=TA_CENTER,
                fontName="Roboto",
                wordWrap=True,
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="Label",
                alignment=TA_LEFT,
                fontName="Roboto",
                fontSize=11.5,
                leading=15,
                wordWrap=True,
            )
        )

    def register_and_mapping_fonts(self):
        """Register and map fonts for the PDF."""
        fonts = [
            (
                "Roboto",
                os.path.join(self.FONT_PATH, "Roboto-Regular.ttf"),
                "UTF-8",
            ),
            (
                "Roboto-Bold",
                os.path.join(self.FONT_PATH, "Roboto-Bold.ttf"),
                "UTF-8",
            ),
        ]

        # Register fonts with PDF metrics
        for font_name, font_path, encoding in fonts:
            pdfmetrics.registerFont(TTFont(font_name, font_path, encoding))

        # Map font names to font styles
        addMapping("Roboto", 0, 0, "Roboto")
        addMapping("Roboto", 1, 0, "Roboto-Bold")

    def create_table(self, label_data: list) -> Table:
        """Create a table with specified column widths and row heights."""
        column_widths = [self.COLUMN_WIDTH] * 3
        row_heights = [0.6 * cm, self.ROW_HEIGHT] * (len(label_data) // 2)

        # Create a table and set its style
        table = Table(label_data, colWidths=column_widths, rowHeights=row_heights)
        table.setStyle(TableStyle(self.TABLE_STYLES))
        return table

    def get_label_data(self, cell_groups: dict) -> list:
        """Get label data based on cell groups."""
        label_data = []
        cell_group_headers = [
            Paragraph(cell_name, self.styles["Center"])
            for cell_name in list(cell_groups.keys())
        ]
        label_data.append(cell_group_headers)

        street_building_paragraphs = []

        # Iterate through cell groups and format street/building information
        for _, cell_group in cell_groups.items():
            street_buildings_info = []
            for street, building_numbers in cell_group.items():
                street_buildings_info.append(
                    f"<b>{street}:</b> • {', '.join(building_numbers)}\n"
                )
            street_building_summary = " ".join(street_buildings_info)
            street_building_paragraphs.append(
                Paragraph(
                    street_building_summary.replace("\n", "<br />\n"),
                    self.styles["Label"],
                )
            )

        label_data.append(street_building_paragraphs)

        new_data = []

        # Organize label data into groups of 3 for better layout
        for i in range(0, len(label_data[0]), 3):
            new_data.append(label_data[0][i : i + 3])
            new_data.append(label_data[1][i : i + 3])

        return new_data

    def get_cell_groups(self) -> dict:
        """Get cell groups based on input data."""
        cell_groups = {}

        # Iterate through input data and organize cell groups
        for cell in self.cell_data:
            cell_name = f"{cell.title} ({cell.box})"
            if cell_name not in cell_groups:
                cell_groups[cell_name] = {}

            for street in cell.buildings.all():
                street_old = (
                    f"({street.street.old_name})" if street.street.old_name else ""
                )
                street_name = f"{street.street.name} {street_old}"
                if street_name not in cell_groups[cell_name]:
                    cell_groups[cell_name][street_name] = []
                cell_groups[cell_name][street_name].append(street.number)

        return cell_groups
