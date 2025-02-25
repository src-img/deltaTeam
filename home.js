document.addEventListener("DOMContentLoaded", function () {
    const startButton = document.getElementById("startButton");
    const p5Container = document.getElementById("p5-container");

    startButton.addEventListener("click", function () {
        startButton.style.display = "none"; // Hide the button
        p5Container.style.display = "block"; // Show the p5.js container

        new p5(sketch, "p5-container"); // Initialize p5.js sketch
    });
});

function sketch(p) {
    p.setup = function () {
        p.createCanvas(400, 400).parent("p5-container");
        p.background(220);
    };

    p.draw = function () {
        p.fill(0);
        p.ellipse(p.mouseX, p.mouseY, 30, 30);
    };
}
