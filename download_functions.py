from plotly.io import write_image
from docx import Document
from docx.shared import Inches
import io
import plotly.graph_objects as go
from docx.shared import RGBColor
from docx.enum.table import WD_ALIGN_VERTICAL
import docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def remove_margins(doc):
    """ Remove all margins in the Word document to allow images to use the full page """
    section = doc.sections[0]
    section.top_margin = 0
    section.bottom_margin = 0
    section.left_margin = 0
    section.right_margin = 0

def save_chart_to_image(fig):
    """ Save Plotly figure as image in memory and return the image file stream """
    img_stream = io.BytesIO()
    img_bytes = fig.to_image(format="png")  # format can be 'png', 'jpeg', 'svg', etc.
    img_stream.write(img_bytes)
    img_stream.seek(0)  # Go back to the beginning of the BytesIO stream
    with open("chart.png", "wb") as f:
        f.write(img_stream.read())
    return img_stream

def create_word_doc(data, file_name="Chainage_Wise_Analyzed_Data.docx"):
    doc = Document()

    doc.add_heading('Chainage Wise Gap Analysis', 0)

    for chainage, (transposed_data1, transposed_data2, gap_analysis, figs) in data.items():
        doc.add_heading(f"Chainage: {chainage}", level=1)
        
        # **Table 1: PIU Data**
        doc.add_heading("PIU Data:", level=2)
        table1 = doc.add_table(rows=1, cols=len(transposed_data1.columns))

        hdr_cells = table1.rows[0].cells
        for i, col in enumerate(transposed_data1.columns):
            hdr_cells[i].text = col
            hdr_cells[i].paragraphs[0].runs[0].bold = True
            set_cell_background_color(hdr_cells[i], 'ADD8E6')

        for index, row in transposed_data1.iterrows():
            row_cells = table1.add_row().cells
            for i, val in enumerate(row):
                row_cells[i].text = str(val)
            if index % 2 == 0:
                for cell in row_cells:
                    set_cell_background_color(cell, 'F0F8FF')
            else:
                for cell in row_cells:
                    set_cell_background_color(cell, 'FFFFFF')

            for cell in row_cells:
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        # **Table 2: RA Data**
        doc.add_heading("RA Data:", level=2)
        table2 = doc.add_table(rows=1, cols=len(transposed_data2.columns))

        hdr_cells = table2.rows[0].cells
        for i, col in enumerate(transposed_data2.columns):
            hdr_cells[i].text = col
            hdr_cells[i].paragraphs[0].runs[0].bold = True
            set_cell_background_color(hdr_cells[i], 'ADD8E6')

        for index, row in transposed_data2.iterrows():
            row_cells = table2.add_row().cells
            for i, val in enumerate(row):
                row_cells[i].text = str(val)
            if index % 2 == 0:
                for cell in row_cells:
                    set_cell_background_color(cell, 'F0F8FF')
            else:
                for cell in row_cells:
                    set_cell_background_color(cell, 'FFFFFF')

            for cell in row_cells:
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        # **Gap Analysis Table**
        doc.add_heading("Gap Analysis:", level=2)
        gap_table = doc.add_table(rows=1, cols=len(gap_analysis.columns))

        hdr_cells = gap_table.rows[0].cells
        for i, col in enumerate(gap_analysis.columns):
            hdr_cells[i].text = col
            hdr_cells[i].paragraphs[0].runs[0].bold = True
            set_cell_background_color(hdr_cells[i], 'ADD8E6')

        for index, row in gap_analysis.iterrows():
            row_cells = gap_table.add_row().cells
            for i, val in enumerate(row):
                row_cells[i].text = str(val)
            if index % 2 == 0:
                for cell in row_cells:
                    set_cell_background_color(cell, 'F0F8FF')
            else:
                for cell in row_cells:
                    set_cell_background_color(cell, 'FFFFFF')

            for cell in row_cells:
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        # remove_margins(doc)
        # for fig in figs:
        img_stream = save_chart_to_image(figs)
        doc.add_picture(img_stream, width=Inches(5.5)) 

        doc.add_page_break()
    # Save the document
    doc.save(file_name)

def set_cell_background_color(cell, color_hex):
    """
    This function sets the background color of a table cell using the color hex code.
    The hex code should be in the format 'RRGGBB'.
    """
    # Get the XML element of the cell
    cell_element = cell._element
    
    # Create the shading element
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), color_hex)  # Set the fill color with the hex code
    cell_element.get_or_add_tcPr().append(shading) 


def create_word_doc_new(moretables,morecharts ,data_new, file_name="Chainage_Wise_Analyzed_Data.docx"):
    doc = Document()
    print('more tables',moretables)
    for key,data in moretables.items():
        doc.add_heading(key, level=2)
        gap_table = doc.add_table(rows=1, cols=len(data.columns))

        hdr_cells = gap_table.rows[0].cells
        for i, col in enumerate(data.columns):
            hdr_cells[i].text = col
            hdr_cells[i].paragraphs[0].runs[0].bold = True
            set_cell_background_color(hdr_cells[i], 'fcfcfc')

        for index, row in data.iterrows():
            row_cells = gap_table.add_row().cells
            for i, val in enumerate(row):
                if isinstance(val, float) and val.is_integer():
                    row_cells[i].text = str(int(val))
                else:
                    row_cells[i].text = str(val)
            if index % 2 == 0:
                for cell in row_cells:
                    set_cell_background_color(cell, 'fcfcfc')
            else:
                for cell in row_cells:
                    set_cell_background_color(cell, 'fcfcfc')

            for cell in row_cells:
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        doc.add_page_break()

    for fig in morecharts:
        img_stream = save_chart_to_image(fig)
        doc.add_picture(img_stream, width=Inches(5.5)) 

    doc.add_page_break()

    doc.add_heading('Chainage Wise Gap Analysis', 0)

    for chainage, (data, figs) in data_new.items():
        doc.add_heading(f"Chainage: {chainage}", level=1)
        
        # # **Table 1: PIU Data**
        # doc.add_heading("PIU Data:", level=2)
        # table1 = doc.add_table(rows=1, cols=len(transposed_data1.columns))

        # hdr_cells = table1.rows[0].cells
        # for i, col in enumerate(transposed_data1.columns):
        #     hdr_cells[i].text = col
        #     hdr_cells[i].paragraphs[0].runs[0].bold = True
        #     set_cell_background_color(hdr_cells[i], 'ADD8E6')

        # for index, row in transposed_data1.iterrows():
        #     row_cells = table1.add_row().cells
        #     for i, val in enumerate(row):
        #         row_cells[i].text = str(val)
        #     if index % 2 == 0:
        #         for cell in row_cells:
        #             set_cell_background_color(cell, 'F0F8FF')
        #     else:
        #         for cell in row_cells:
        #             set_cell_background_color(cell, 'FFFFFF')

        #     for cell in row_cells:
        #         cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        # # **Table 2: RA Data**
        # doc.add_heading("RA Data:", level=2)
        # table2 = doc.add_table(rows=1, cols=len(transposed_data2.columns))

        # hdr_cells = table2.rows[0].cells
        # for i, col in enumerate(transposed_data2.columns):
        #     hdr_cells[i].text = col
        #     hdr_cells[i].paragraphs[0].runs[0].bold = True
        #     set_cell_background_color(hdr_cells[i], 'ADD8E6')

        # for index, row in transposed_data2.iterrows():
        #     row_cells = table2.add_row().cells
        #     for i, val in enumerate(row):
        #         row_cells[i].text = str(val)
        #     if index % 2 == 0:
        #         for cell in row_cells:
        #             set_cell_background_color(cell, 'F0F8FF')
        #     else:
        #         for cell in row_cells:
        #             set_cell_background_color(cell, 'FFFFFF')

        #     for cell in row_cells:
        #         cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        # **Gap Analysis Table**
        doc.add_heading("Gap Analysis:", level=2)
        gap_table = doc.add_table(rows=1, cols=len(data.columns))

        hdr_cells = gap_table.rows[0].cells
        for i, col in enumerate(data.columns):
            hdr_cells[i].text = col
            hdr_cells[i].paragraphs[0].runs[0].bold = True
            set_cell_background_color(hdr_cells[i], 'fcfcfc')

        for index, row in data.iterrows():
            row_cells = gap_table.add_row().cells
            for i, val in enumerate(row):
                if isinstance(val, float) and val.is_integer():
                    row_cells[i].text = str(int(val))
                else:
                    row_cells[i].text = str(val)
            if index % 2 == 0:
                for cell in row_cells:
                    set_cell_background_color(cell, 'fcfcfc')
            else:
                for cell in row_cells:
                    set_cell_background_color(cell, 'fcfcfc')

            for cell in row_cells:
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        # remove_margins(doc)
        # for fig in figs:
        img_stream = save_chart_to_image(figs)
        doc.add_picture(img_stream, width=Inches(5.5)) 

        doc.add_page_break()
    # Save the document
    doc.save(file_name)