document.addEventListener("DOMContentLoaded", function() {
    const backgrounds = [
        "../static/images/resultsImg1.jpg",
        "../static/images/resultsImg2.jpg",
        "../static/images/resultsImg3.jpg",
        "../static/images/resultsImg4.jpg",
        "../static/images/resultsImg5.jpg"
    ];

    let imgIndex = Math.floor(Math.random() * backgrounds.length);
    let newBackground = backgrounds[imgIndex];

    document.body.style.backgroundImage = `url('${newBackground}')`;
});