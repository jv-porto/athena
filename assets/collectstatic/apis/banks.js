const url = 'https://brasilapi.com.br/api/banks/v1'
const options = {
    method: 'GET',
    mode: 'cors',
    headers: {
        'content-type': 'application/json;charset=utf-8'
    }
}
fetch(url, options).then(
    response => response.json()
).then(
    data => {
        fillBanks(data)
        return
    }
)

const selectBank = document.querySelector('select#bank')
function fillBanks(data) {
    for (const bank of data) {
        if (Number.isInteger(bank.code)) {
            const option = document.createElement('option')
            bank.code = `${bank.code}`.padStart(4, '0')
            option.value = bank.code
            option.text = `${bank.code} - ${bank.name}`
            
            selectBank.add(option)
        }
    }
}