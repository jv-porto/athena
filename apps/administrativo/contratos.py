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



"""from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
registerFont(TTFont('Arial','arial.ttf'))
registerFont(TTFont('Arial-Bold','arialbd.ttf'))
registerFontFamily('Arial', normal='Arial', bold='Arial-Bold')"""

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER, fontName='Times-Roman', fontSize=8, leading=20))
styles.add(ParagraphStyle(name='centered-bold', alignment=TA_CENTER, fontName='Times-Bold', fontSize=8, leading=20))
styles.add(ParagraphStyle(name='justified', alignment=TA_JUSTIFY, fontName='Times-Roman', fontSize=8))
styles.add(ParagraphStyle(name='justified-level-2', alignment=TA_JUSTIFY, fontName='Times-Roman', fontSize=8, firstLineIndent=1.25*cm))
styles.add(ParagraphStyle(name='justified-level-3', alignment=TA_JUSTIFY, fontName='Times-Roman', fontSize=8, leftIndent=1.25*cm, firstLineIndent=2.5*cm))
styles.add(ParagraphStyle(name='right', alignment=TA_RIGHT, fontName='Times-Roman', fontSize=8))



def GeneratePdf(elements_list, logo=None):
    if logo != None:
        def get_image(path, height=1.27*cm):
            img = ImageReader(path)
            iw, ih = img.getSize()
            aspect = iw / float(ih)
            return Image(path, height=height, width=(height * aspect))

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
def contrato_educacional_engaja_2022(request, variaveis_dict, estudante_contratante):
    titulo = f'CLÁUSULAS DO CONTRATO'
    subtitulo = f'CURSO ENGAJA'
    if estudante_contratante is False:
        paragrafo_1 = f'1 –  O CURSO: O (a) contratante {variaveis_dict["contratante_nome"]}, portador (a) do RG {variaveis_dict["contratante_rg"]}, CPF {variaveis_dict["contratante_cpf"]}, residente em {variaveis_dict["contratante_endereco_lougradouro"]}, {variaveis_dict["contratante_endereco_numero"]}, {variaveis_dict["contratante_endereco_complemento"]}, {variaveis_dict["contratante_endereco_bairro"]}, {variaveis_dict["contratante_endereco_cidade"]}, {variaveis_dict["contratante_endereco_estado"]}, CEP {variaveis_dict["contratante_endereco_cep"]}, contrata os serviços da contratada a fim de que a (o) aluna (o) {variaveis_dict["estudante_nome"]}, portador (a) do RG {variaveis_dict["estudante_rg"]}, CPF {variaveis_dict["estudante_cpf"]}, tenha livre acesso a todas as atividades do curso {variaveis_dict["curso_descricao"]}, que terão suas atividades ministradas de SEGUNDA A SEXTA, das 9h às 19h, compreendendo, neste período, atividades, como: aulas, plantões, simulados, orientação pedagógica individual e coletiva, assembleias, atividades socioemocionais e o curso de políticas públicas.'
    elif estudante_contratante is True:
        paragrafo_1 = f'1 –  O CURSO: O (a) contratante {variaveis_dict["contratante_nome"]}, portador (a) do RG {variaveis_dict["contratante_rg"]}, CPF {variaveis_dict["contratante_cpf"]}, residente em {variaveis_dict["contratante_endereco_lougradouro"]}, {variaveis_dict["contratante_endereco_numero"]}, {variaveis_dict["contratante_endereco_complemento"]}, {variaveis_dict["contratante_endereco_bairro"]}, {variaveis_dict["contratante_endereco_cidade"]}, {variaveis_dict["contratante_endereco_estado"]}, contrata os serviços da contratada a fim de que tenha livre acesso a todas as atividades do curso {variaveis_dict["curso_descricao"]}, que terão suas atividades ministradas de SEGUNDA A SEXTA, das 9h às 19h, compreendendo, neste período, atividades, como: aulas, plantões, simulados, orientação pedagógica individual e coletiva, assembleias, atividades socioemocionais e o curso de políticas públicas.'
    paragrafo_1_1 = f'1.1 – Excepcionalmente, poderá ocorrer atividade aos sábados quando houver aplicação de simulados. Fica assegurado aos alunos sabatistas a entrega dos simulados para serem realizados em outro período.'
    paragrafo_1_2 = f'1.2 – Excepcionalmente, por motivos de força maior, como pandemia, por exemplo, poderá haver alteração na prestação do serviço. Neste caso, garantimos manter a qualidade do serviço pedagógico oferecido pelo cursinho, contemplado no item 1, fazendo as adequações necessárias e comunicando com antecedência as alterações.'
    paragrafo_2 = f'2 – O PERÍODO: As aulas serão ministradas no período de {variaveis_dict["data_inicio"]} a {variaveis_dict["data_termino"]}, com 4 semanas de férias intercaladas na finalização de cada ciclo do currículo (4 ciclos). Todas as informações referentes ao período do curso são passíveis de alteração, sendo a contratante devidamente avisada com antecedência.'
    paragrafo_3 = f'3 – VALORES E MULTA: O valor integral do curso é {variaveis_dict["custo_total_curso"]} ({variaveis_dict["custo_total_curso_extenso"]}), podendo ser dividido em {variaveis_dict["parcelas_totais_curso"]} parcelas de {variaveis_dict["custo_total_parcelas_curso"]} ({variaveis_dict["custo_total_parcelas_curso_extenso"]}). Este valor compreende os custos de operação do curso (aulas, utilização do espaço no contraturno, simulados, mentorias, atividades com a psicóloga) e, também, os gastos correspondentes ao uso do aplicativo do PEdu. O material didático é um custo a parte, descrito no item 3.3. Ficou acordado, entre as partes, um desconto de {variaveis_dict["percentual_desconto_curso"]} no valor do curso. Assim sendo, o (a) contratante pagará à contratada o valor de {variaveis_dict["custo_final_curso"]} ({variaveis_dict["custo_final_curso_extenso"]}), dividido em {variaveis_dict["parcelas_finais_curso"]} parcelas de {variaveis_dict["custo_final_parcelas_curso"]} ({variaveis_dict["custo_final_parcelas_curso_extenso"]}).'
    paragrafo_3_1 = f'3.1 – A ausência do (a) contratante em quaisquer aulas, mesmo que justificada, não o (a) eximirá do pagamento das parcelas correspondentes e nem dá direito a reposição dessas aulas.'
    paragrafo_3_2 = f'3.2 - O pagamento por meio de boleto deverá ser realizado todo dia {variaveis_dict["dia_pagamento"]}, a contar a partir do mês de {variaveis_dict["mes_inicio_pagamento"]} de {variaveis_dict["ano_inicio_pagamento"]}. O atraso no pagamento das parcelas implicará em juros de mora de 2% após o vencimento e correção de 0,03% ao dia.'
    paragrafo_3_3 = f'3.3 - O material didático compreende 4 apostilas (bimestrais), 4 cadernos extras anuais (filosofia, sociologia, arte e questões do ENEM) e plataforma de exercícios (Studos). O custo do material é de {variaveis_dict["custo_total_material"]} ({variaveis_dict["custo_total_material_extenso"]}), podendo ser dividido em até {variaveis_dict["parcelas_totais_material"]} parcelas (com juros).'
    paragrafo_3_4 = f'3.4 - A venda dos recursos didáticos será feita de forma direta pela editora Sae Digital, em site específico do fornecedor. Qualquer adversidade surgida que venha a descumprir o pagamento do material deverá ser tratado diretamente com a editora.'
    paragrafo_4 = f'4 – CANCELAMENTO DO CONTRATO E MULTA RESCISÓRIA: caso seja necessário realizar o cancelamento deste contrato, o (a) contratante deverá informar à contratada por e-mail (endereçado a atendimento@personaleduca.com.br), Whatsapp ou presencialmente na secretaria.'
    paragrafo_4_1 = f'4.1 – Para a solicitação do cancelamento será considerada a data do comunicado, mas sua efetivação apenas ocorrerá após a assinatura do termo de cancelamento pelo (a) contratante em até 15 dias após a solicitação.'
    paragrafo_4_1_1 = f'4.1.1 – Para a realização do cancelamento, deverão estar quitadas todas as parcelas com o vencimento até a data da solicitação.'
    paragrafo_4_2 = f'4.2 – Caso o (a) contratante desista do curso, fica estipulada uma multa indenizatória correspondente a 02 (duas) parcelas de valor INTEGRAL, que deverão ser pagas na efetivação do cancelamento.'
    paragrafo_4_3 = f'4.3 – A multa prevista na cláusula anterior não incidirá no caso de o (a) contratante avisar à contratada sobre a desistência do curso com um prazo de 02 (dois) meses de antecedência, podendo assim, assistir todas as aulas desse período.'
    paragrafo_4_4 = f'4.4 – Diante da efetivação do cancelamento, o contratante poderá solicitar o estorno do valor referente ao material que ainda não tiver sido disponibilizado ao aluno até a data desta solicitação. O estorno do valor restante do material será feito diretamente pela editora Sae Digital, sendo a forma de pagamento equivalente a que foi adotada na aquisição do mesmo.'
    paragrafo_5 = f'5 – Por este contrato, o (a) contratante permite o uso de sua imagem em fotos, vídeos e outros materiais para serem usados com fins expositivos e de propaganda.'
    paragrafo_6 = f'6 – As partes elegem o foro da Comarca de São José do Rio Preto para dirimir eventuais dúvidas e controvérsias oriundas do presente contrato. E, por estarem justos e contratados, assinam o presente no verso em duas vias, de idênticos teores.'
    local_data = f'São José do Rio Preto, {variaveis_dict["data_assinatura"]}.'
    campo_assinatura = f'______________________________________________________________'
    assinatura_cliente = f'{variaveis_dict["contratante_nome"]} (CPF: {variaveis_dict["contratante_cpf"]})'
    assinatura_escola = f'{variaveis_dict["escola_nome_fantasia"]} (CNPJ: {variaveis_dict["escola_cnpj"]})'

    return GeneratePdf(
        elements_list = [
            Paragraph(titulo, styles['centered-bold']),
            Paragraph(subtitulo, styles['centered-bold']),
            Spacer(1, 12),
            Paragraph(paragrafo_1, styles['justified']),
            Paragraph(paragrafo_1_1, styles['justified-level-2']),
            Paragraph(paragrafo_1_2, styles['justified-level-2']),
            Paragraph(paragrafo_2, styles['justified']),
            Paragraph(paragrafo_3, styles['justified']),
            Paragraph(paragrafo_3_1, styles['justified-level-2']),
            Paragraph(paragrafo_3_2, styles['justified-level-2']),
            Paragraph(paragrafo_3_3, styles['justified-level-2']),
            Paragraph(paragrafo_3_4, styles['justified-level-2']),
            Paragraph(paragrafo_4, styles['justified']),
            Paragraph(paragrafo_4_1, styles['justified-level-2']),
            Paragraph(paragrafo_4_1_1, styles['justified-level-3']),
            Paragraph(paragrafo_4_2, styles['justified-level-2']),
            Paragraph(paragrafo_4_3, styles['justified-level-2']),
            Paragraph(paragrafo_4_4, styles['justified-level-2']),
            Paragraph(paragrafo_5, styles['justified']),
            Paragraph(paragrafo_6, styles['justified']),
            Spacer(1, 10),
            Paragraph(local_data, styles['right']),
            Spacer(1, 30),
            Paragraph(campo_assinatura, styles['centered']),
            Paragraph(assinatura_cliente, styles['centered']),
            Spacer(1, 30),
            Paragraph(campo_assinatura, styles['centered']),
            Paragraph(assinatura_escola, styles['centered']),
        ],
        logo=request.user.escola.logo,)
