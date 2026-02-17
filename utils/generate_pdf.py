import markdown2
from fpdf import FPDF
from PIL import Image as PILImage

def generate_stride_pdf(img_path, report_md):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "Relatorio de Modelagem de Ameacas STRIDE", ln=True, align="C")
    pdf.ln(5)
    with PILImage.open(img_path) as img:
        width, height = img.size
        aspect_ratio = height / width

    pdf_img_width = 180
    pdf_img_height = pdf_img_width * aspect_ratio

    pdf.image(img_path, x=10, y=25, w=pdf_img_width)

    new_y_position = 25 + pdf_img_height + 10
    pdf.set_y(new_y_position)
    report_safe = report_md.encode('latin-1', 'ignore').decode('latin-1')

    html_content = markdown2.markdown(report_safe)

    pdf.set_font("helvetica", size=11)

    pdf.write_html(html_content)
    return bytes(pdf.output())
