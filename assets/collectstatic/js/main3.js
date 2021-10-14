/*************** GET CLASSES FROM COURSE ***************/
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
        findCourseClasses()
    })
}
