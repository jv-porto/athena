const telefone = document.querySelectorAll('.telephone')
const cep = document.querySelectorAll('#postal-code')
const cpf = document.querySelectorAll('#cpf')
const rg = document.querySelectorAll('#rg')
const cnpj = document.querySelectorAll('#cnpj')
const matricula = document.querySelectorAll('#registration-number')
const id_estudante = document.querySelectorAll('.student-id')
const modelo_monetario = document.querySelectorAll('.money')
const conta_bancaria = document.querySelectorAll('#bank-account')
const numero_endereco = document.querySelectorAll('#address-number')
const codigo_contrato = document.querySelectorAll('#contract-code')



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