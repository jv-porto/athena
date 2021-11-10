const cepInputs = document.querySelectorAll('input#postal-code')
for (const item of cepInputs) {
    item.addEventListener('blur', function () {
        buscacep(item)
    })
}



function buscacep(input) {
    const cep = input.value
    const url = `https://brasilapi.com.br/api/cep/v2/${cep}`
    const options = {
        method: 'GET',
        mode: 'cors',
        headers: {
            'content-type': 'application/json;charset=utf-8'
        }
    }

    if(!input.validity.valueMissing) {
        fetch(url, options).then(
            response => response.json()
        ).then(
            data => {
                buscacep_fill(data)
                return
            }
        )
    }
}



function buscacep_fill(data) {
    const lougradouro = document.querySelector('#address-street')
    const bairro = document.querySelector('#address-neighborhood')
    const cidade = document.querySelector('#address-city')
    const estado = document.querySelector('#address-state')
    const pais = document.querySelector('#address-country')

    lougradouro.value = data.street
    /*lougradouro.readOnly = true
    lougradouro.tabIndex = '-1'*/

    bairro.value = data.neighborhood
    /*bairro.readOnly = true
    bairro.tabIndex = '-1'*/

    cidade.value = data.city
    cidade.readOnly = true
    cidade.tabIndex = '-1'

    estado.value = data.state
    estado.readOnly = true
    estado.tabIndex = '-1'

    pais.value = 'Brasil'
    pais.readOnly = true
    pais.tabIndex = '-1'
}
