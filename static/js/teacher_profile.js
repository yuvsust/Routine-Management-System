// If any error messages occur while submitting the form
// this will hide the info div at very first and take user to the form.
{% if messages or informationForm.errors %}
hideInfo()
{% endif %}
// Error show ends //


//------ Toggle show info and update info div strats--------//
show_info = document.getElementById("show_info")
update_info = document.getElementById("update_info")

function hideInfo() {
    show_info.style.display = "none"
    update_info.style.display = "block"
}

function hideForm() {
    show_info.style.display = "block"
    update_info.style.display = "none"
}
//------ Toggle show info and update info div ends --------//


//------ Enable Submit button if at-least one field is updated starts------//
submit = document.getElementById("submit_info")
let form = document.getElementById("myForm");
form.addEventListener("input", function () {
    submit.disabled = false
});
//------ Enable Submit button if at-least one field is updated ends ------//


//------ Mark Teachers engagement status as Danger in the cell starts------//
const id_list = ["SUN8", "SUN9", "SUN10", "SUN11", "SUN12", "SUN2", "SUN3", "SUN4", "MON8", "MON9", "MON10", "MON11", "MON12", "MON2", "MON3", "MON4", "TUE8", "TUE9", "TUE10", "TUE11", "TUE12", "TUE2", "TUE3", "TUE4", "WED8", "WED9", "WED10", "WED11", "WED12", "WED2", "WED3", "WED4", "THU8", "THU9", "THU10", "THU11", "THU12", "THU2", "THU3", "THU4"]
form_field = []
$("#id_time_table option").each(function () {
    form_field.push($(this).filter(':selected').text())
})
for (let i = 0; i < id_list.length; i++) {
    cell = document.getElementById(id_list[i])
    for (let j = 0; j < form_field.length; j++) {
        if (form_field[j] == id_list[i]) {
            console.log(form_field[j])
            cell.classList.add("bg-danger")
            break;
        }
    }
}
//------ Mark Teachers engagement status as Danger in the cell ends ------//


//------ Update Engagement Schedule in the Run-Time starts ------//
update = document.getElementById("updateSchedule")
upload = document.getElementById("uploadToAdmin")
saved = document.getElementById("saveUpdate")
footer = document.getElementById("cardFooter")
title = document.getElementById("engagementTitle")

function startUpdate() {
    update.style.display = "none"
    upload.style.display = "none"
    saved.style.display = "inline-block"
    footer.style.display = "inline-block"
    title.innerText = "Update Your Engagement"

    for (let i = 0; i < id_list.length; i++) {
        let cell = document.getElementById(id_list[i])
        cell.style.cursor = "pointer"
        cell.innerText = ""
        cell.addEventListener("click", showAlert);
    }
}

showAlert = function (event) {
    cell_id = event.target.id
    classList = event.target.classList
    if (classList.contains("bg-danger")) {
        classList.remove("bg-danger");
        $("#id_time_table option:contains(" + cell_id + ")").prop('selected', false)
    }
    else {
        classList.add("bg-danger");
        $("#id_time_table option:contains(" + cell_id + ")").prop('selected', true)
    }
}

function cancelUpdate() {
    update.style.display = "inline-block"
    upload.style.display = "inline-block"
    saved.style.display = "none"
    footer.style.display = "none"
    title.innerText = "Your Engagement"

    for (let i = 0; i < id_list.length; i++) {
        cell = document.getElementById(id_list[i])
        cell.style.cursor = "default"
        cell.innerText = ""
        cell.removeEventListener("click", showAlert);
    }
}
//------ Update Engagement Schedule in the Run-Time ends ------//