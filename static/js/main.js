const trailer = document.getElementById("trailer");

// Trailer
const animateTrailer = (e, interacting) => {
    const x = e.clientX - trailer.offsetWidth / 2,
        y = e.clientY - trailer.offsetHeight / 2;

    const keyframes = {
        transform: `translate(${x}px, ${y}px) scale(${interacting ? 2.5 : 1.5})`
    }

    trailer.animate(keyframes, {
        duration: 800,
        fill: "forwards"
    });
}

window.onmousemove = e => {
    const interactable = e.target.closest(".card"),
        interacting = interactable !== null;
    animateTrailer(e, interacting);
}

document.getElementById("cards").onmousemove = e => {
    for(const card of document.getElementsByClassName("card")) {
        const rect = card.getBoundingClientRect(),
            x = e.clientX - rect.left,
            y = e.clientY - rect.top;
    
        card.style.setProperty("--mouse-x", `${x}px`);
        card.style.setProperty("--mouse-y", `${y}px`);
    };
}

// card
window.onmousemove = e => {
    const interactable = e.target.closest(".card-template"),
        interacting = interactable !== null;
    animateTrailer(e, interacting);
}

document.getElementById("cards").onmousemove = e => {
    for(const card of document.getElementsByClassName("card-template")) {
        const rect = card.getBoundingClientRect(),
            x = e.clientX - rect.left,
            y = e.clientY - rect.top;
    
        card.style.setProperty("--mouse-x", `${x}px`);
        card.style.setProperty("--mouse-y", `${y}px`);
    };
}