const questions = [

    // =========================
    // PROGRAMMATION
    // =========================

    {
        question: "Quel mot-clé permet de définir une fonction en Python ?",
        answers: [
            "function",
            "def",
            "func",
            "define"
        ],
        correct: 1
    },

    {
        question: "Quel type de donnée contient True ou False ?",
        answers: [
            "String",
            "Integer",
            "Boolean",
            "Float"
        ],
        correct: 2
    },

    {
        question: "Quel symbole est utilisé pour un commentaire en Python ?",
        answers: [
            "//",
            "#",
            "/* */",
            "<!-- -->"
        ],
        correct: 1
    },

    {
        question: "Que donne 5 + 3 * 2 en Python ?",
        answers: [
            "16",
            "11",
            "13",
            "10"
        ],
        correct: 1
    },

    {
        question: "Quelle fonction permet d'afficher quelque chose en Python ?",
        answers: [
            "show()",
            "display()",
            "print()",
            "write()"
        ],
        correct: 2
    },


    // =========================
    // STI
    // =========================

    {
        question: "Que signifie CPU ?",
        answers: [
            "Central Processing Unit",
            "Computer Personal Unit",
            "Central Program Utility",
            "Computer Processing User"
        ],
        correct: 0
    },

    {
        question: "Quelle unité mesure la capacité d'une mémoire ?",
        answers: [
            "Volt",
            "Ohm",
            "Octet",
            "Ampère"
        ],
        correct: 2
    },

    {
        question: "Quel composant permet principalement de stocker les données à long terme ?",
        answers: [
            "RAM",
            "Disque SSD",
            "CPU",
            "Carte graphique"
        ],
        correct: 1
    },

    {
        question: "Que signifie RAM ?",
        answers: [
            "Random Access Memory",
            "Read Access Machine",
            "Rapid Application Memory",
            "Random Application Module"
        ],
        correct: 0
    },

    {
        question: "Quel composant exécute principalement les instructions d'un programme ?",
        answers: [
            "CPU",
            "Clavier",
            "Écran",
            "Souris"
        ],
        correct: 0
    },


    // =========================
    // MATH
    // =========================

    {
        question: "Combien vaut 2² + 3² ?",
        answers: [
            "10",
            "11",
            "12",
            "13"
        ],
        correct: 3
    },

    {
        question: "Quelle est la dérivée de x² ?",
        answers: [
            "x",
            "2x",
            "x²",
            "2"
        ],
        correct: 1
    },

    {
        question: "Si f(x) = 2x + 3, combien vaut f(2) ?",
        answers: [
            "5",
            "6",
            "7",
            "8"
        ],
        correct: 2
    },

    {
        question: "Quelle est la valeur de √49 ?",
        answers: [
            "6",
            "7",
            "8",
            "9"
        ],
        correct: 1
    },

    {
        question: "Combien vaut 3 × 4 + 2 ?",
        answers: [
            "14",
            "20",
            "18",
            "12"
        ],
        correct: 0
    },


    // =========================
    // PHYSIQUE
    // =========================

    {
        question: "Quelle est l'unité SI de la force ?",
        answers: [
            "Joule",
            "Newton",
            "Watt",
            "Volt"
        ],
        correct: 1
    },

    {
        question: "Quelle est la relation entre vitesse, distance et temps ?",
        answers: [
            "v = d × t",
            "v = d / t",
            "v = t / d",
            "v = d + t"
        ],
        correct: 1
    },

    {
        question: "Quelle est l'unité de la tension électrique ?",
        answers: [
            "Ampère",
            "Ohm",
            "Volt",
            "Watt"
        ],
        correct: 2
    },

    {
        question: "Quelle est l'unité de la résistance électrique ?",
        answers: [
            "Volt",
            "Ohm",
            "Ampère",
            "Joule"
        ],
        correct: 1
    },

    {
        question: "Quelle grandeur est mesurée en Ampère ?",
        answers: [
            "Tension",
            "Résistance",
            "Intensité du courant",
            "Puissance"
        ],
        correct: 2
    }

];


let currentQuestion = 0;

let score = 0;

let selected = false;


// =========================
// SHUFFLE QUESTIONS
// =========================

questions.sort(() => Math.random() - 0.5);


// =========================
// SHOW QUESTION
// =========================

function showQuestion() {

    selected = false;

    const q = questions[currentQuestion];


    document.getElementById("question").textContent =
        q.question;


    document.getElementById("questionNumber").textContent =
        "Question " +
        (currentQuestion + 1) +
        " / " +
        questions.length;


    document.getElementById("score").textContent =
        "Score: " + score;


    document.getElementById("progress").style.width =
        ((currentQuestion) / questions.length * 100) + "%";


    const answersContainer =
        document.getElementById("answers");


    answersContainer.innerHTML = "";


    q.answers.forEach((answer, index) => {

        const button =
            document.createElement("button");


        button.className = "answer";

        button.textContent = answer;


        button.onclick = function() {

            selectAnswer(index, button);

        };


        answersContainer.appendChild(button);

    });


    document.getElementById("nextButton").style.display =
        "none";
}


// =========================
// SELECT ANSWER
// =========================

function selectAnswer(index, button) {

    if (selected) {
        return;
    }

    selected = true;


    const q = questions[currentQuestion];


    const buttons =
        document.querySelectorAll(".answer");


    buttons.forEach((btn, i) => {

        if (i === q.correct) {

            btn.classList.add("correct");

        }

    });


    if (index === q.correct) {

        score++;

    } else {

        button.classList.add("wrong");

    }


    document.getElementById("score").textContent =
        "Score: " + score;


    document.getElementById("nextButton").style.display =
        "block";
}


// =========================
// NEXT QUESTION
// =========================

function nextQuestion() {

    currentQuestion++;


    if (currentQuestion >= questions.length) {

        showResult();

        return;
    }


    showQuestion();
}


// =========================
// RESULT
// =========================

function showResult() {

    document.getElementById("quiz").style.display =
        "none";


    document.getElementById("result").style.display =
        "block";


    document.getElementById("finalScore").textContent =
        "Your score: " +
        score +
        " / " +
        questions.length;


    let message;


    const percentage =
        (score / questions.length) * 100;


    if (percentage >= 90) {

        message =
            "🌟 Excellent! You're a 3ème Info star!";

    } else if (percentage >= 70) {

        message =
            "👏 Very good! Keep going!";

    } else if (percentage >= 50) {

        message =
            "💪 Good job! A little more revision!";

    } else {

        message =
            "📚 Don't give up! Review your lessons and try again!";

    }


    document.getElementById("finalMessage").textContent =
        message;
}


// =========================
// RESTART
// =========================

function restartQuiz() {

    currentQuestion = 0;

    score = 0;

    questions.sort(() => Math.random() - 0.5);


    document.getElementById("quiz").style.display =
        "block";


    document.getElementById("result").style.display =
        "none";


    showQuestion();
}


// =========================
// START
// =========================

showQuestion();