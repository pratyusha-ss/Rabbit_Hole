let score = 0;

let question = 0;


let questions = [

    "You find £10 on the floor. What do you do?",

    "Your friend forgot their homework. What do you do?",

    "You see a lost phone on a bench. What do you do?"

];


let choices = [

    [
        "🪙 Keep it",
        "🤝 Ask around",
        "🏪 Give it to a shop"
    ],

    [
        "📚 Help them",
        "😶 Do nothing",
        "😂 Make a joke"
    ],

    [
        "📱 Keep it",
        "🔎 Look for the owner",
        "👮 Give it to an adult"
    ]

];


let results = [

    [
        "You kept the money. Interesting choice! 🪙",
        "You asked around and found the owner! ⭐",
        "You gave the money to a shop. Nice choice! ✨"
    ],

    [
        "You helped your friend. ⭐",
        "You decided to stay out of it.",
        "Your friend laughed at the joke! 😂"
    ],

    [
        "You decided to keep the phone.",
        "You found the owner! 🌟",
        "You gave the phone to an adult. 👍"
    ]

];


let points = [

    [5, 15, 10],

    [15, 5, 10],

    [5, 20, 15]

];


function showQuestion() {

    document.getElementById("question").innerText =
        questions[question];

    document.getElementById("story").innerText =
        "What will you choose?";

    document.getElementById("buttons").innerHTML = "";

    for (let i = 0; i < 3; i++) {

        let button = document.createElement("button");

        button.innerText = choices[question][i];

        button.onclick = function() {

            choose(i);

        };

        document.getElementById("buttons").appendChild(button);
    }
}


function choose(number) {

    score = score + points[question][number];

    document.getElementById("score").innerText =
        "⭐ Score: " + score;

    document.getElementById("story").innerText =
        results[question][number];

    question = question + 1;

    if (question == 3) {

        document.getElementById("question").innerText =
            "🌌 ECHO Complete!";

        document.getElementById("story").innerText =
            "Your final score is " + score + "!";

        document.getElementById("buttons").innerHTML =
            "✨ Thanks for playing! ✨";

    }

    else {

        setTimeout(showQuestion, 1000);

    }
}


function restart() {

    score = 0;

    question = 0;

    document.getElementById("score").innerText =
        "⭐ Score: 0";

    showQuestion();
}


showQuestion();