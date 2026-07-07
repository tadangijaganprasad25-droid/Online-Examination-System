const questions = [
    {q:"2+2?", options:["2","4","5"], answer:1},
    {q:"HTML stands for?", options:["Hyper Text Markup Language","High Text Machine","None"], answer:0}
];

function loadQuiz() {
    let html = "";

    questions.forEach((q, i) => {
        html += `
        <div class="mb-4">
            <h5>${i+1}. ${q.q}</h5>
        `;

        q.options.forEach((opt, j) => {
            html += `
            <div class="option" onclick="selectOption(this, 'q${i}', ${j})">
                <input type="radio" name="q${i}" value="${j}" hidden>
                ${opt}
            </div>
            `;
        });

        html += `</div>`;
    });

    document.getElementById("quiz").innerHTML = html;
}

function selectOption(element, name, value) {
    document.querySelectorAll(`[name=${name}]`).forEach(el => {
        el.parentElement.classList.remove("selected");
    });

    element.classList.add("selected");
    element.querySelector("input").checked = true;
}

function submitQuiz() {
    let score = 0;

    questions.forEach((q, i) => {
        let ans = document.querySelector(`input[name=q${i}]:checked`);
        if (ans && parseInt(ans.value) === q.answer) {
            score++;
        }
    });

    document.getElementById("score").value = score;
    document.getElementById("form").submit();
}

window.onload = loadQuiz;