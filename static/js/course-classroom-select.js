document.addEventListener("DOMContentLoaded", () => {
    const schoolSelect = document.getElementById("id_school");
    const classroomSelect = document.getElementById("id_classroom");

    if (!schoolSelect || !classroomSelect) {
        return;
    }

    const classroomsUrl =
        classroomSelect.dataset.classroomsUrl || schoolSelect.dataset.classroomsUrl;
    const placeholder = classroomSelect.dataset.placeholder || "Seleziona un’aula";
    const helpText = document.getElementById("id_classroom_helptext");

    if (!classroomsUrl) {
        return;
    }

    function setClassroomOptions(classrooms, selectedId = "") {
        classroomSelect.replaceChildren(new Option(placeholder, ""));

        for (const classroom of classrooms) {
            classroomSelect.add(new Option(classroom.name, classroom.id));
        }

        classroomSelect.value = selectedId;
        classroomSelect.disabled = classrooms.length === 0;

        if (helpText && classrooms.length === 0) {
            helpText.textContent = schoolSelect.value
                ? "Questa sede non ha ancora aule associate."
                : "Scegli prima una sede per visualizzare le sue aule.";
        } else if (helpText) {
            helpText.textContent = "Seleziona un’aula appartenente alla sede scelta.";
        }
    }

    async function loadClassrooms(schoolId, selectedId = "") {
        if (!schoolId) {
            setClassroomOptions([]);
            return;
        }

        classroomSelect.disabled = true;
        if (helpText) {
            helpText.textContent = "Caricamento delle aule…";
        }

        const url = new URL(classroomsUrl, window.location.origin);
        url.searchParams.set("school_id", schoolId);

        try {
            const response = await fetch(url, {
                headers: { Accept: "application/json" },
            });
            if (!response.ok) {
                throw new Error("Impossibile caricare le aule.");
            }

            const data = await response.json();
            setClassroomOptions(data.classrooms, selectedId);
        } catch (error) {
            setClassroomOptions([]);
            if (helpText) {
                helpText.textContent = "Errore nel caricamento delle aule. Riprova.";
            }
            console.error(error);
        }
    }

    const initialClassroom = classroomSelect.value;
    schoolSelect.addEventListener("change", () => {
        loadClassrooms(schoolSelect.value);
    });
    loadClassrooms(schoolSelect.value, initialClassroom);
});
