const nav = document.querySelector('nav')


/*************** SHOW MENU ***************/
const logo = document.querySelectorAll('.logo')
for (const item of logo) {
    item.addEventListener('click', function () {
        nav.classList.toggle('show-menu')
    })
}



/*************** SHOW PESQUISAR ***************/
const page_actions_pesquisar = document.querySelectorAll('div.page-actions .page-actions-pesquisar')
for (const item of page_actions_pesquisar) {
    item.addEventListener('click', function () {
        nav.classList.toggle('show-pesquisar')
    })
}



/*************** ADD SEARCH FILTER ***************/
const search_input = document.querySelectorAll('div.pesquisar form input#search')
const search_form = document.querySelectorAll('div.pesquisar form')
for (const item of search_input) {
    item.addEventListener('blur', function () {
        for (const form of search_form) {
            form.action = `?search=${item.value}`
        }
    })
}



/*************** HIDE PESQUISAR ***************/
const pesquisar_actions_close = document.querySelectorAll('div.pesquisar .pesquisar-actions-close')
for (const item of pesquisar_actions_close) {
    item.addEventListener('click', function () {
        nav.classList.toggle('show-pesquisar')
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
for (const item of menuActionsId) {
    const menuActionAlterar = document.querySelector('.page-actions-alterar')
    const menuActionExcluir = document.querySelector('.page-actions-excluir')
    const menuActionImprimir = document.querySelectorAll('.page-actions-imprimir')
    const menuActionDigitalizar = document.querySelectorAll('.page-actions-digitalizar')
    item.addEventListener('click', function () {
        idValue = item.value
        menuActionAlterar.href = `alterar/${idValue.replace('/', '_')}/`
        menuActionExcluir.href = `excluir/${idValue.replace('/', '_')}/`
        if (menuActionImprimir) {
            for (const item of menuActionImprimir) {
                const imprimirUrl = document.querySelector(`input.select-value#contract-file-url[type=hidden][name=contract-file-url-${idValue}]`).value
                item.href = imprimirUrl
            }
        }
        if (menuActionDigitalizar) {
            for (const item of menuActionDigitalizar) {
                item.href = `digitalizar/${idValue.replace('/', '_')}/`
            }
        }
    })
}



/*************** GET STUDENT INFO ***************/
const studentIdField = document.querySelectorAll('div.item-section-parent input.student-id')
const studentNameField = document.querySelectorAll('div.item-section-parent input.student-name')
for (let i = 0; i < studentIdField.length; i++) {
    function findStudentName () {
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
    }
    findStudentName()
    studentIdField[i].addEventListener('blur', function () {
        findStudentName()
    })
}



/*************** GET GUARDIAN INFO ***************/
const guardianIdField = document.querySelectorAll('div.item-section-parent input.guardian-id')
const guardianNameField = document.querySelectorAll('div.item-section-parent input.guardian-name')
for (let i = 0; i < guardianIdField.length; i++) {
    function findGuardianName () {
        idValue = guardianIdField[i].value
        const url = `${window.location.origin}/api/pessoas/responsavel/${idValue}/`
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
    }
    findGuardianName()
    guardianIdField[i].addEventListener('blur', function () {
        findGuardianName()
    })
}



/*************** ADD FIELDS SUBJECTS ***************/
var i = 1
const clickAddSubjects = document.querySelectorAll('.subjects .light-title strong.action-add-item')
const clickRemoveSubjects = document.querySelectorAll('.subjects .light-title strong.action-remove-item')
for (const item of clickAddSubjects) {
    item.addEventListener('click', function() {
        if (i <= 14) {
            var originalDiv = document.querySelector('div.item-section')
            var clone = originalDiv.cloneNode(true)
            clone.children[0].children[0].setAttribute('for', 'subject-code-' + i)
            clone.children[0].children[1].id = 'subject-code-' + i
            clone.children[0].children[1].name = 'subject-code-' + i
            clone.children[1].children[0].setAttribute('for', 'subject-description-' + i)
            clone.children[1].children[1].id = 'subject-description-' + i
            clone.children[1].children[1].name = 'subject-description-' + i
            clone.children[2].children[0].setAttribute('for', 'subject-teacher-' + i)
            clone.children[2].children[1].id = 'subject-teacher-' + i
            clone.children[2].children[1].name = 'subject-teacher-' + i
            clone.children[3].children[0].setAttribute('for', 'subject-weekday-' + i)
            clone.children[3].children[1].id = 'subject-weekday-' + i
            clone.children[3].children[1].name = 'subject-weekday-' + i
            clone.children[4].children[0].setAttribute('for', 'subject-start-time-' + i)
            clone.children[4].children[1].id = 'subject-start-time-' + i
            clone.children[4].children[1].name = 'subject-start-time-' + i
            clone.children[5].children[0].setAttribute('for', 'subject-end-time-' + i)
            clone.children[5].children[1].id = 'subject-end-time-' + i
            clone.children[5].children[1].name = 'subject-end-time-' + i
            originalDiv.parentNode.appendChild(clone)
            i++
        }
    })
}
for (const item of clickRemoveSubjects) {
    item.addEventListener('click', function () {
        if (i >= 2) {
            var lastDiv = document.querySelector('div.item-section:last-child')
            lastDiv.parentNode.removeChild(lastDiv)
            i--
        }
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
const id_escola = document.querySelector('form div.form-section input[type=hidden][name=id-escola]')
if (id_escola) {
    for (escola of id_escola) {
        const description = document.querySelector('form div.form-section select#description')
        const checkboxes = document.querySelectorAll('form div.form-section.permissions input[type=checkbox]')
    
        if (menuActionExcluir) {
            menuActionExcluir.href = `excluir/${description.value}/`
            description.addEventListener('change', function () {
                menuActionExcluir.href = `excluir/${description.value}/`
            })
        }
    
        const url = `${window.location.origin}/api/escola/${escola.value}/usuarios_permissoes/`
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
}



/*************** SCHOOL PERMISSIONS ***************/
const school_id = document.querySelectorAll('form div.form-section div.input-unit input#school-id')
const checkboxes = document.querySelectorAll('form div.form-section.modules input[type=checkbox]')
if (school_id) {
    for (const school of school_id) {
        const url = `${window.location.origin}/api/modulos_escola/${school.value}/`
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
                for (const item of checkboxes) {
                    perm = item.id
                    item.checked = data[perm]
                }
            }
        )
    }
}



/*************** GET CLASSES FROM COURSE OF SCHOOL ***************/
const coursesField = document.querySelectorAll('div.form-section div.input-unit.course-classes select#course-id')
const classesField = document.querySelectorAll('div.form-section div.input-unit.course-classes select#class-id')
for (let i = 0; i < coursesField.length; i++) {
    function findCourseClasses () {
        course_id = coursesField[i].value
        const url = `${window.location.origin}/api/curso/${course_id}/turmas/?deleted=false`
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
                for (const item of data) {
                    let option = document.createElement('option')
                    option.value = item.id
                    option.text = item.descricao
                    classesField[i].add(option)
                }
            }
        )
    }
    findCourseClasses()
    coursesField[i].addEventListener('change', function () {
        var classesFieldLength = classesField[i].options.length - 1
        for (let j = classesFieldLength; j >= 0; j--) {
            classesField[i].remove(j)
        }
        findCourseClasses()
    })
}



/*************** GET SELECT INFO ***************/
const select_value = document.querySelectorAll('form div.form-section div.input-unit input.select-value[type=hidden]')
if (select_value) {
    for (const item of select_value) {
        const option = document.querySelector(`form div.form-section div.input-unit select#${item.id} option[value="${item.value}"]`)
        option.selected = true
    }
}



/*************** GET EDUCATIONAL PLATFORMS ***************/
const school_id_menu = document.querySelectorAll('nav input[type=hidden][name="school-id"]')
if (school_id_menu) {
    const educational_platforms_anchor_search = document.querySelectorAll('nav div.menu div.link-section div.dropdown-section a.dropdown-button')
    for (const item of educational_platforms_anchor_search) {
        if (item.innerText == "Plataformas") {
            var educational_platforms_anchor = item
        }
    }

    for (let school of school_id_menu) {
        const url = `${window.location.origin}/api/escola/${school.value}/plataformas/?is_active=true`
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
                for (const item of data) {
                    let anchor = document.createElement('a')
                    anchor.innerText = item.descricao
                    anchor.href = `${window.location.origin}/pedagogico/plataforma/${item.id}/`
                    anchor.setAttribute('class', 'body-black-text')
                    educational_platforms_anchor.nextElementSibling.appendChild(anchor)
                }
            }
        )
    }
}



/*************** ALLOW TAB IN TEXTAREA ***************/
/*const tab_textareas_list = document.querySelectorAll('.tab-textarea')
for (let tab_textarea of tab_textareas_list) {
    tab_textarea.addEventListener('keydown', function(e) {
        if (e.key == 'Tab') {
            e.preventDefault();
            var start = this.selectionStart;
            var end = this.selectionEnd;
    
            // set textarea value to: text before caret + tab + text after caret
            this.value = this.value.substring(0, start) +
                "\t" + this.value.substring(end);
    
            // put caret at right position again
            this.selectionStart =
                this.selectionEnd = start + 1;
        }
    })
}*/
