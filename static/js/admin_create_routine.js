//-------- Show all courses and teachers of the semester that is selected currently starts ---------//

// Initially semester 11 selected //
showAllSemesterCourses("11");
showAllTeachersofThisSemester("11");

// Function that actually shows courses
function showAllSemesterCourses(tab_id) {
    {% for course in courses %}
    course_element = document.getElementById("{{ course.course_code|cut:' ' }}")
    if ({{ course.semester }
} != tab_id) {
    course_element.setAttribute("style", "display: none;")
}
            else {
    course_element.setAttribute("style", "display: block;")
}
{% endfor %}
    }


//Function that actually shows teachers
function showAllTeachersofThisSemester(tab_id) {
    {% for teacher in teachers %}
    var isShown = false
    {% for course in teacher.course_set.all %}
    teacher_element = document.getElementById("teacher{{teacher.pk}}")

    // Show teacher or not
    if ({{ course.semester }
} != tab_id ) {
    if (isShown == false) {
        teacher_element.setAttribute("style", "display: none;")
    }

    // Hide courses that are not of this semester
    teacher_course_id = "{{ course.course_code }} + {{ course.course_type|lower }}"
    course_of_teacher = document.getElementById(teacher_course_id)
    course_of_teacher.setAttribute("style", "display: none;")
}
                else if ({{ course.semester }} == tab_id) {
    teacher_element.setAttribute("style", "display: block;");

    // show courses of this teacher only of this semester
    teacher_course_id = "{{ course.course_code }} + {{ course.course_type|lower }}"
    course_of_teacher = document.getElementById(teacher_course_id)
    course_of_teacher.setAttribute("style", "display: block;")
    isShown = true;

}
{% endfor %}
{% endfor %}
    }

//-------- Show all courses and teachers of the semester that is selected currently ends ---------//



//----------------- Funtion for selected tab starts---------------------//
var triggerTabList = [].slice.call(document.querySelectorAll('#routine button'));

triggerTabList.forEach(function (selectedTab) {
    var tabTrigger = new bootstrap.Tab(selectedTab);

    selectedTab.addEventListener('click', function (event) {
        // Mark the selected tab as primary button
        event.preventDefault();
        tabTrigger.show();


        // Show all courses of the selected semester
        var tab_id = $(this).attr('id');
        tab_id = tab_id.slice(6, 8);
        showAllSemesterCourses(tab_id);

        // Show all teachers who are taking course in the selected semester
        showAllTeachersofThisSemester(tab_id);

    })
})
//----------------- Funtion for selected tab ends---------------------//

console.log("Cell")
cell_parent = document.getElementById("pills-11")
cell = cell_parent.querySelector("#SUN8")
console.log(cell)

for (let i = 0; i < 1; i++) {
    initialForm = document.getElementById("id_form-INITIAL_FORMS").value
    {% for form in formset %}
    outerLoopCounter = {{ forloop.counter0 }
}
if (outerLoopCounter == initialForm) {
    break;
}
{% for field in form %}
cell_id = document.getElementById("{{ field.id_for_label }}")
try {
    cell_id = cell_id.options[cell_id.selectedIndex].text;
}
catch {
    cell_id = cell_id.value;
}
console.log(cell_id)
{% endfor %}
{% endfor %}
    }
