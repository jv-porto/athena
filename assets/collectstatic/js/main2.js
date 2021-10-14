/*************** GET SELECT INFO ***************/
const select_value = document.querySelectorAll('form div.form-section div.input-unit input.select-value[type=hidden]')
if (select_value) {
    for (const item of select_value) {
        const option = document.querySelector(`form div.form-section div.input-unit select#${item.id} option[value=${item.value}]`)
        option.selected = true
    }
}

/*************** SCHOOL PERMISSIONS ***************/
const school_id = document.querySelector('form div.form-section div.input-unit input#school-id').value
const checkboxes = document.querySelectorAll('form div.form-section.modules input[type=checkbox]')
if (school_id) {
    const url = `${window.location.origin}/api/modulos_escola/${school_id}/`
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

/*************** ADD FIELDS SUBJECTS ***************/
var i = 1
const clickAddSubjects = document.querySelectorAll('.subjects .light-title strong.action-add-item')
const clickRemoveSubjects = document.querySelectorAll('.subjects .light-title strong.action-remove-item')
for (const item of clickAddSubjects) {
    item.addEventListener('click', function() {
        if (i <= 14) {
            var originalDiv = document.querySelector('div.item-section')
            var clone = originalDiv.cloneNode(true)
            console.log(clone.children[0])
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
