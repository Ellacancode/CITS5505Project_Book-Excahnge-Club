
document.addEventListener("DOMContentLoaded", function() {
    // For img1
    const image1 = document.querySelector('#img1');
    const imageSources1 = [
        '../static/home_pics/romantic1.jpg',
        '../static/home_pics/romantic2.jpg',
        '../static/home_pics/romantic3.jpg'
    ];
    let currentIndex1 = 0;

    function switchImage1() {
        currentIndex1 = (currentIndex1 + 1) % imageSources1.length;
        image1.src = imageSources1[currentIndex1];
    }

    setInterval(switchImage1, 800);

    // For img2
    const images2 = document.querySelectorAll('#img2');
    const imageSources2 = [
        '../static/home_pics/horror1.jpg',
        '../static/home_pics/horror2.jpg',
        '../static/home_pics/horror3.jpg'
    ];

    function switchImage2(image) {
        let currentIndex = 0;

        return function() {
            currentIndex = (currentIndex + 1) % imageSources2.length;
            image.src = imageSources2[currentIndex];
        };
    }

    images2.forEach(image => {
        setInterval(switchImage2(image), 800);
    });

    // For img3
    const images3 = document.querySelectorAll('#img3');
    const imageSources3 = [
        '../static/home_pics/science1.jpg',
        '../static/home_pics/science2.jpg',
        '../static/home_pics/science3.jpg'
    ];

    function switchImage3(image) {
        let currentIndex = 0;

        return function() {
            currentIndex = (currentIndex + 1) % imageSources3.length;
            image.src = imageSources3[currentIndex];
        };
    }

    images3.forEach(image => {
        setInterval(switchImage3(image), 800);
    });

    // For img4
    const images4 = document.querySelectorAll('#img4');
    const imageSources4 = [
        '../static/home_pics/mystery1.jpg',
        '../static/home_pics/mystery2.jpg',
        '../static/home_pics/mystery3.jpg'
    ];

    function switchImage4(image) {
        let currentIndex = 0;

        return function() {
            currentIndex = (currentIndex + 1) % imageSources4.length;
            image.src = imageSources4[currentIndex];
        };
    }

    images4.forEach(image => {
        setInterval(switchImage4(image), 800);
    });
});
