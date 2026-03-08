window.next = function () {
    const current = questions[q];
    const selected = current.querySelector("input[type='radio']:checked");

    if (!selected) {
        alert("Please select an option");
        return;
    }

    localStorage.setItem(selected.name, selected.value);

    current.classList.remove("active");
    q++;

    if (q < questions.length) {
        questions[q].classList.add("active");
    } else {
        window.location.href = "result.html";
    }
};
