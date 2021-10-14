/*************** SHOW MENU ***************/
const nav = document.querySelector('nav')
const logo = document.querySelectorAll('.logo')
for (const item of logo) {
    item.addEventListener('click', function () {
        nav.classList.toggle('show')
    })
}

/*************** SHOW DROPDOWN MENU ***************/
const dropdown = document.getElementsByClassName("dropdown-button")
for (let i = 0; i < dropdown.length; i++) {
    dropdown[i].addEventListener('click', function () {
        this.classList.toggle('active')
        var dropdownContent = this.nextElementSibling
        if (dropdownContent.style.display === 'block') {
            dropdownContent.style.display = 'none'
        } else {
            dropdownContent.style.display = 'block'
        }
    })
}

/*************** SHOW PROFILE ***************/
const profileSection = document.getElementsByClassName("profile-image")
for (const item of profileSection) {
    item.addEventListener('click', function () {
        item.classList.toggle('open')
    })
}

/*************** SHOW PAGE ACTIONS DROPDOWN SECTION ***************/
const pageActionsDropdownSection = document.getElementsByClassName("page-actions-incluir")
for (const item of pageActionsDropdownSection) {
    item.addEventListener('click', function () {
        item.classList.toggle('open')
    })
}

/*************** CHOOSE ID FOR MENU ACTIONS ***************/
const menuActionsId = document.querySelectorAll('.choose-menu-id')
const menuActionAlterar = document.querySelector('.page-actions-alterar')
const menuActionExcluir = document.querySelector('.page-actions-excluir')
for (const item of menuActionsId) {
    item.addEventListener('click', function () {
        idValue = item.value
        menuActionAlterar.href = `alterar/${idValue.replace('/', '_')}/`
        menuActionExcluir.href = `excluir/${idValue.replace('/', '_')}/`
    })
}

/*************** GET STUDENT INFO ***************/
const studentIdField = document.querySelectorAll('div.item-section-parent input.student-id')
const studentNameField = document.querySelectorAll('div.item-section-parent input.student-name')
for (let i = 0; i < studentIdField.length; i++) {
    studentIdField[i].addEventListener('blur', function () {
        idValue = studentIdField[i].value
        const url = `${window.location.origin}/api/pessoas/estudante/${idValue}/`
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
                    studentNameField[i].value = data.nome
                    studentNameField[i].readOnly = true
                    studentNameField[i].tabIndex = '-1'
                }
            )
    })
}

/*************** GET GUARDIAN INFO ***************/
const guardianIdField = document.querySelectorAll('div.item-section-parent input.guardian-id')
const guardianNameField = document.querySelectorAll('div.item-section-parent input.guardian-name')
for (let i = 0; i < guardianIdField.length; i++) {
    guardianIdField[i].addEventListener('blur', function () {
        idValue = guardianIdField[i].value
        const url = `${window.location.origin}/api/pessoas/responsavel/${idValue}`
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
                    guardianNameField[i].value = data.nome
                    guardianNameField[i].readOnly = true
                    guardianNameField[i].tabIndex = '-1'
                }
            )
    })
}

/*************** REMOVE FIELD GROUP ***************/
const maxStudentsForGuardian = 5
var i = maxStudentsForGuardian
const clickRemove = document.querySelectorAll('.light-title strong.action-remove-item')
for (const item of clickRemove) {
    item.addEventListener('click', function () {
        if (i > 1) {
            var lastDiv = document.querySelector('div.item-section:last-child')
            lastDiv.parentNode.removeChild(lastDiv)
            i--
        }
    })
}

/*************** PERMISSIONS FORM ***************/
const id_escola = document.querySelector('form div.form-section input[type=hidden][name=id-escola]').value
if (id_escola) {
    const description = document.querySelector('form div.form-section select#description')
    const checkboxes = document.querySelectorAll('form div.form-section.permissions input[type=checkbox]')

    if (menuActionExcluir) {
        menuActionExcluir.href = `excluir/${description.value}/`
        description.addEventListener('change', function () {
            menuActionExcluir.href = `excluir/${description.value}/`
        })
    }

    const url = `${window.location.origin}/api/escola/${id_escola}/usuarios_permissoes/`
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
            function find_permissions(data) {
                selection = data.find(obj => {
                    return obj.descricao === description.value
                })
                for (const item of checkboxes) {
                    verification = item.id
                    item.checked = selection[verification]
                }
            }
            find_permissions(data)
            description.addEventListener('change', function() {
                find_permissions(data)
            })
        }
    )
}
