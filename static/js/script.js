function startCountdown() {
    const countdown = document.getElementById("countdown");
    let count = 3;

    countdown.innerText = "Captura em " + count + "...";
    const interval = setInterval(() => {
        count--;
        if (count > 0){
            countdown.innerText = "Captura em " + count + "...";
        } else {
            countdown.innerText = "Diga 'Xis' FABRÍCIO";
            clearInterval(interval);
            document.getElementById("registerForm").submit();
        }
    }, 1000);
}