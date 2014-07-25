
function toggleRotate() {
    $("#joker").toggleClass("rotate");
    $("#black_joker").toggleClass("rotate");
}

setInterval(toggleRotate, 200);