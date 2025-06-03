const gameArea = document.getElementById("game-area");
const scoreDisplay = document.getElementById("score");
let score = 0;

function spawnTarget() {
  const target = document.createElement("div");
  target.className = "target";

  const x = Math.floor(Math.random() * (gameArea.clientWidth - 30));
  const y = Math.floor(Math.random() * (gameArea.clientHeight - 30));

  target.style.left = x + "px";
  target.style.top = y + "px";

  target.onclick = () => {
    score++;
    scoreDisplay.innerText = score;
    target.remove();
    spawnTarget(); // cria outro
  };

  gameArea.appendChild(target);
}

// Inicia o jogo
spawnTarget();
