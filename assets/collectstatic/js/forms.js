const telefone = document.querySelectorAll('.telephone')
const cep = document.querySelectorAll('#postal-code')
const cpf = document.querySelectorAll('#cpf')
const rg = document.querySelectorAll('#rg')
const cnpj = document.querySelectorAll('#cnpj')
const matricula = document.querySelectorAll('#registration-number')
const id_estudante = document.querySelectorAll('.student-id')
const modelo_monetario = document.querySelectorAll('.money')
const agencia_bancaria = document.querySelectorAll('#bank-branch')
const conta_bancaria = document.querySelectorAll('#bank-account')
const numero_endereco = document.querySelectorAll('#address-number')
const codigo_contrato = document.querySelectorAll('#contract-code')
const id_responsavel = document.querySelectorAll('.guardian-id')
const desconto = document.querySelectorAll('#discount')
const ano_academico = document.querySelectorAll('#academic-year-id')
const codigo_maiusculo_7 = document.querySelectorAll('.uppercase-code-7')
const codigo_maiusculo_11 = document.querySelectorAll('.uppercase-code-11')
const codigo_numerico_4 = document.querySelectorAll('.numeric-code-4')
const codigo_numerico_9 = document.querySelectorAll('.numeric-code-9')
const codigo_numerico_2 = document.querySelectorAll('.numeric-code-2')



for (const item of telefone) {
    new Cleave(item, {
        phone: true,
        phoneRegionCode: 'BR'
    })
}

for (const item of cep) {
    new Cleave(item, {
        blocks: [5, 3],
        delimiters: ['-'],
        numericOnly: true
    })
}

for (const item of cpf) {
    new Cleave(item, {
        blocks: [3, 3, 3, 2],
        delimiters: ['.', '.', '-'],
        numericOnly: true
    })
}

for (const item of rg) {
    new Cleave(item, {
        blocks: [2, 3, 3, 1],
        delimiters: ['.', '.', '-'],
        numericOnly: true
    })
}

for (const item of cnpj) {
    new Cleave(item, {
        blocks: [2, 3, 3, 4, 2],
        delimiters: ['.', '.', '/', '-'],
        numericOnly: true
    })
}

for (const item of matricula) {
    new Cleave(item, {
        blocks: [5],
        numericOnly: true
    })
}

for (const item of id_estudante) {
    new Cleave(item, {
        blocks: [9],
        numericOnly: true
    })
}

for (const item of modelo_monetario) {
    new Cleave(item, {
        numeral: true,
        numeralDecimalMark: ',',
        delimiter: '.',
        prefix: 'R$ '
    });
}

for (const item of agencia_bancaria) {
    new Cleave(item, {
        blocks: [4],
        numericOnly: true
    })
}

for (const item of conta_bancaria) {
    item.addEventListener('focus', function () {
        new Cleave(item, {
            blocks: [11],
            numericOnly: true
        })
    });
    item.addEventListener('blur', function () {
        firstBlockLength = item.value.length - 1
        new Cleave(item, {
            blocks: [firstBlockLength, 1],
            delimiters: ['-'],
            numericOnly: true
        })
    });
}

for (const item of numero_endereco) {
    new Cleave(item, {
        blocks: [5],
        numericOnly: true
    })
}

for (const item of codigo_contrato) {
    new Cleave(item, {
        blocks: [6],
        numericOnly: true
    })
}

for (const item of id_responsavel) {
    new Cleave(item, {
        blocks: [9, 2],
        delimiters: ['r'],
        numericOnly: true
    })
}

for (const item of desconto) {
    new Cleave(item, {
        blocks: [2, 2],
        delimiters: ['.'],
        numericOnly: true
    });
}

for (const item of ano_academico) {
    new Cleave(item, {
        blocks: [4, 1],
        delimiters: ['/'],
        numericOnly: true
    })
}

for (const item of codigo_maiusculo_7) {
    new Cleave(item, {
        blocks: [7],
        uppercase: true,
    })
}

for (const item of codigo_maiusculo_11) {
    new Cleave(item, {
        blocks: [11],
        uppercase: true,
    })
}

for (const item of codigo_numerico_4) {
    new Cleave(item, {
        blocks: [4],
        numericOnly: true,
    })
}

for (const item of codigo_numerico_9) {
    new Cleave(item, {
        blocks: [9],
        numericOnly: true,
    })
}

for (const item of codigo_numerico_2) {
    new Cleave(item, {
        blocks: [2],
        numericOnly: true,
    })
}