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
        menuActionAlterar.href = `alterar/${idValue}/`
        menuActionExcluir.href = `excluir/${idValue}/`
    })
}

/*************** GET PERSON INFO ***************/
const studentIdField = document.querySelectorAll('div.item-section-parent input.student-id')
const studentNameField = document.querySelectorAll('div.item-section-parent input.student-name')
for (let i = 0; i < studentIdField.length; i++) {
    studentIdField[i].addEventListener('blur', function () {
        idValue = studentIdField[i].value
        const url = `${window.location.origin}/administrativo/pessoas/estudantes/${idValue}`
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

/*************** ADD ANOTHER FIELD GROUP ***************/
/*var i = 1
const maxStudentsForGuardian = 5
const clickAdd = document.querySelectorAll('.light-title strong.action-add-item')
const clickRemove = document.querySelectorAll('.light-title strong.action-remove-item')
for (const item of clickAdd) {
    item.addEventListener('click', function() {
        if (i <= (maxStudentsForGuardian - 1)) {
            var originalDiv = document.querySelector('div.item-section')
            var clone = originalDiv.cloneNode(true)
            clone.children[0].children[0].setAttribute('for', 'student-id-' + i)
            clone.children[0].children[1].id = 'student-id-' + i
            clone.children[1].children[0].setAttribute('for', 'student-name-' + i)
            clone.children[1].children[1].id = 'student-name-' + i
            originalDiv.parentNode.appendChild(clone)
            i++
        }
    })
}
for (const item of clickRemove) {
    item.addEventListener('click', function () {
        if (i > 1) {
            var lastDiv = document.querySelector('div.item-section:last-child')
            lastDiv.parentNode.removeChild(lastDiv)
            i--
        }
    })
}*/