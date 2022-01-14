import re
from io import BytesIO
from django.core.files.base import ContentFile
from reportlab.platypus import SimpleDocTemplate, PageTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus.frames import Frame
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.units import cm
from functools import partial
from administrativo.models import ModeloContratoEducacional
from .models import Escola



def get_school_id(request):
    if hasattr(request.user, 'pessoaestudante'):
        return request.user.pessoaestudante.escola.id
    elif hasattr(request.user, 'pessoaresponsavel'):
        return request.user.pessoaresponsavel.escola.id
    elif hasattr(request.user, 'pessoacolaborador'):
        return request.user.pessoacolaborador.escola.id
    elif hasattr(request.user, 'escola'):
        return request.user.escola.id


from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
registerFont(TTFont('Arial','arial.ttf'))
registerFont(TTFont('Arial-Bold','arialbd.ttf'))
registerFontFamily('Arial', normal='Arial', bold='Arial-Bold')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER, fontName='Arial', fontSize=8, leading=20))
styles.add(ParagraphStyle(name='centered-bold', alignment=TA_CENTER, fontName='Arial-Bold', fontSize=8, leading=20))
styles.add(ParagraphStyle(name='justified-bold', alignment=TA_JUSTIFY, fontName='Arial-Bold', fontSize=8))
styles.add(ParagraphStyle(name='justified', alignment=TA_JUSTIFY, fontName='Arial', fontSize=8))
styles.add(ParagraphStyle(name='justified-level-2', alignment=TA_JUSTIFY, fontName='Arial', fontSize=8, firstLineIndent=1.25*cm))
styles.add(ParagraphStyle(name='justified-level-3', alignment=TA_JUSTIFY, fontName='Arial', fontSize=8, leftIndent=1.25*cm, firstLineIndent=2.5*cm))
styles.add(ParagraphStyle(name='right', alignment=TA_RIGHT, fontName='Arial', fontSize=8))


def get_image(path, height=1.27*cm):
    img = ImageReader(path)
    iw, ih = img.getSize()
    aspect = iw / float(ih)
    return Image(path, height=height, width=(height * aspect))



def GeneratePdf(elements_list, logo=None):
    if logo != None:
        def generate_header_footer(canvas, doc, header_content=None, footer_content=None):
            width, height = doc.width+doc.leftMargin+doc.rightMargin, doc.height+doc.topMargin+doc.bottomMargin
            if header_content is not None:
                canvas.saveState()
                header_content.drawOn(canvas, ((width-1.27*cm)/2), (height-doc.topMargin))
                canvas.restoreState()
            if footer_content is not None:
                canvas.saveState()
                footer_content.drawOn(canvas, ((width-1.27*cm)/2), (height-doc.topMargin))
                canvas.restoreState()

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.27*cm,
        leftMargin=1.27*cm,
        topMargin=1.27*cm,
        bottomMargin=1.27*cm)

    if logo != None:
        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height)
        header_content = get_image(logo)
        template = PageTemplate(frames=frame, onPage=partial(generate_header_footer, header_content=header_content))
        doc.addPageTemplates([template])

    elements = []
    for item in elements_list:
        elements.append(item)
    
    doc.build(elements)

    file = ContentFile(buffer.getvalue())
    file.content_type = 'application/pdf'
    buffer.close()

    return file



############### Contrato de Prestação de Serviços Educacionais ###############
def contrato_educacional(request, variaveis_dict, estudante_contratante):
    titulo = f'CONTRATO'
    subtitulo = f'CURSO ' + variaveis_dict["curso_descricao"].upper()

    turma_contrato = ModeloContratoEducacional.objects.get(pk=request.POST['class-id']).contrato
    texto = f'{turma_contrato}'.split('\n')
    i = 0
    while i < len(texto):
        while True:
            busca = re.search(r'\{\{[\w\d\s_]{1,}\}\}', texto[i])
            if busca:
                variavel = busca.group()[2:-2]
                indices = busca.span()
                texto[i] = texto[i][:indices[0]] + str(variaveis_dict[f'{variavel}']) + texto[i][indices[1]:]
            else:
                break
        i += 1

    local_data = f'São José do Rio Preto, {variaveis_dict["data_assinatura"]}.'
    campo_assinatura = f'______________________________________________________________'
    assinatura_cliente = f'{variaveis_dict["contratante_nome"]} (CPF: {variaveis_dict["contratante_cpf"]})'
    assinatura_escola = f'{variaveis_dict["escola_nome_fantasia"]} (CNPJ: {variaveis_dict["escola_cnpj"]})'

    escola = Escola.objects.get(pk=get_school_id(request))
    elements_list = [
        Paragraph(titulo, styles['centered-bold']),
        Paragraph(subtitulo, styles['centered']),
    ]
    i = 0
    while i < len(texto):
        if '*****' in texto[i]:
            texto[i] = texto[i].replace('*****', '')
            elements_list.append(Paragraph(texto[i], styles['justified-bold']))
        elif '//////////' in texto[i]:
            texto[i] = texto[i].replace('//////////', '')
            elements_list.append(Paragraph(texto[i], styles['justified-level-3']))
        elif '/////' in texto[i]:
            texto[i] = texto[i].replace('/////', '')
            elements_list.append(Paragraph(texto[i], styles['justified-level-2']))
        else:
            elements_list.append(Paragraph(texto[i], styles['justified']))
        i += 1
    elements_list.extend([
        Spacer(1, 10),
        Paragraph(local_data, styles['right']),
        Spacer(1, 25),
        Paragraph(campo_assinatura, styles['centered']),
        Paragraph(assinatura_cliente, styles['centered']),
    ])

    if escola.assinatura:
        elements_list.extend([
            get_image(escola.assinatura, height=1.7*cm)
        ])
    else:
        elements_list.extend([
            Spacer(1, 30),
            Paragraph(campo_assinatura, styles['centered']),
        ])
    elements_list.extend([
        Paragraph(assinatura_escola, styles['centered']),
    ])

    return GeneratePdf(
        elements_list=elements_list,
        logo=escola.logo)
