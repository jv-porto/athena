############### Contrato de Prestação de Serviços Educacionais ###############
def contrato_educacional(variaveis_dict):
    titulo = f'CONTRATO DE PRESTAÇÂO DE SERVIÇOS EDUCACIONAIS'
    subtitulo = f'CLÁUSULAS DO CONTRATO - CURSO ENGAJA'

    paragrafo_1 = f'1 – O CURSO: O (a) contratante {contratante}, residente em {endereco_lougradouro}, n {endereco_numero}, bairro {endereco_bairro}, complemento {endereco_complemento}, CEP {endereco_cep} contrata os serviços da contratada a fim de que a (o) aluna (o) {estudante}, RG {rg_estudante} tenha livre acesso a todas as atividades do curso {curso}, que terão suas atividades ministradas de {dias_letivos}, das {horário_letivo}, compreendendo, neste período: aulas, plantões, simulados, orientação pedagógica individual e coletiva, assembleias, atividades socioemocionais e o curso de políticas públicas.'

    paragrafo_1_1 = f'1.1 – Excepcionalmente, poderá ocorrer atividade aos sábados quando houver aplicação de simulados. Fica assegurado aos alunos sabatistas a entrega dos simulados para serem realizados em outro período.'
    paragrafo_1_2 = f'1.2 – Excepcionalmente, por motivos de força maior, como pandemia, por exemplo, poderá haver alteração na prestação do serviço. Neste caso, garantimos manter a qualidade do serviço pedagógico oferecido pelo cursinho, contemplado no item 1, fazendo as adequações necessárias e comunicando com antecedência as alterações.'

    paragrafo_2 = f'2 – O PERÍODO: As aulas serão ministradas no período de {data_inicial} a {data_final}, com 4 semanas de férias intercaladas na finalização de cada ciclo do currículo (4 ciclos). Todas as informações referentes ao período do curso são passíveis de alteração, sendo a contratante devidamente avisada com antecedência.'

    paragrafo_3 = f'3 – VALORES E MULTA: O valor integral do curso é {valor_integral} ({valor_integral_extenso}), podendo ser dividido em {numero_integral_parcelas} parcelas de {valor_integral_parcelas}. Este valor compreende os custos de operação do curso (aulas, utilização do espaço no contraturno, simulados, mentorias, atividades com a psicóloga) e, também,  os gastos correspondentes ao uso do aplicativo do PEdu. O material didático é um custo a parte, descrito no item 3.3. Ficou acordado, entre as partes, um desconto de {percentual_desconto} no valor do curso. Assim sendo,  o (a) contratante pagará ao contratado o valor de {valor_final} dividido em {numero_final_parcelas} parcelas de {valor_final_parcelas} ({valor_final_extenso}).'

    paragrafo_3_1 = f'3.1 – A ausência do (a) contratante em quaisquer aulas, mesmo que justificada, não o (a) eximirá do pagamento das parcelas correspondentes e nem dá direito a reposição dessas aulas.'
    paragrafo_3_2 = f'3.2 - O pagamento por meio de boleto deverá ser realizado todo dia {dia_pagamento}, a contar a partir do mês de {inicio_pagamento}. O atraso no pagamento das parcelas implicará em juros de mora de 2% após o vencimento e correção de 0,03% ao dia.'
    paragrafo_3_3 = f'3.3 - O material didático compreende 4 apostilas (bimestrais), 4 cadernos extras anuais (filosofia, sociologia, arte e questões do enem) e plataforma de exercícios (Studos). O custo do material é de {custo_material} ({custo_material_extenso}), podendo ser dividido em até {numero_parcelas_material} parcelas (com juros) de {custo_parcelas_material} ({custo_parcelas_material_extenso}).'
    paragrafo_3_4 = f'3.4 - A venda dos recursos didáticos será feita de forma direta pela editora SAE Digital, em site específico do fornecedor. Qualquer adversidade surgida que venha a descumprir o pagamento do material deverá ser tratado diretamente com a editora.'

    paragrafo_4 = f'4 – CANCELAMENTO DO CONTRATO E MULTA RESCISÓRIA: caso seja necessário realizar o cancelamento deste contrato, o (a) contratante deverá informar a contratada por e-mail (endereçado a atendimento@personaleduca.com.br), Whatsapp ou presencialmente na secretaria.'

    paragrafo_4_1 = f'4.1 – Para a solicitação do cancelamento será considerada a data do comunicado, mas sua efetivação apenas ocorrerá após a assinatura do termo de cancelamento pelo (a) contratante em até 15 dias após a solicitação.'

    paragrafo_4_1_1 = f'4.1.1 – Para a realização do cancelamento, deverão estar quitadas todas as parcelas com o vencimento até a data da solicitação.'

    paragrafo_4_2 = f'4.2 – Fica assegurado ao contratante, devido às incertezas e instabilidades decorrentes da pandemia, o cancelamento sem multa deste contrato, até {data_final_cancelamento}, caso o aluno seja aprovado em vestibular para ingresso no primeiro semestre de 2021, mediante apresentação de documento que comprove a matrícula do aluno na Instituição em que foi aprovado.'
    paragrafo_4_3 = f'4.3 – Após o prazo mencionado no item anterior ({data_final_cancelamento}), caso o (a) contratante desista do curso, fica estipulada uma multa indenizatória correspondente a 02 (duas) parcelas de valor INTEGRAL, que deverão ser pagas na efetivação do cancelamento.'

    paragrafo_5 = f'5 – Por este contrato, o (a) contratante permite o uso de sua imagem em fotos, vídeos e outros materiais para serem usados com fins expositivos e de propaganda.'

    paragrafo_6 = f'6 – As partes elegem o foro da Comarca de São José do Rio Preto para dirimir eventuais dúvidas e controvérsias oriundas do presente contrato. E, por estarem justos e contratados, assinam o presente no verso em duas vias, de idênticos teores.'

    local_data = f'São José do Rio Preto, {data_assinatura}.'

    assinatura_cliente = f'Cliente: {contratante}	CPF: {cpf_contratante}'

    assinatura_escola = f'Personal Educa (CNPJ: 24.350.003.0001-13)'
