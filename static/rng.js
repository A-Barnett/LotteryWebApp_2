// JavaScript function to generate 6 random unique values in order and populate form
function luckyDip() {

    // create empty set
    let draw = new Set();

    // while set does not contain 6 values, create a random value between 1 and 60
    let csRandomNumber;
    let randomBuffer;
    let i;
    while (draw.size < 6) {
        randomBuffer = new Uint32Array(1);
        window.crypto.getRandomValues(randomBuffer);
        csRandomNumber = randomBuffer[0] / (0xFFFFFFFF)
        i = Math.round(csRandomNumber * 60)
        draw.add(i)

    }

    // turn set into an array
    let a = Array.from(draw);

    // sort array into size order
    a.sort(function (a, b) {
        return a - b;
    });

    // add values to fields in create draw form
    for (let i = 0; i < 6; i++) {
        document.getElementById("no" + (i + 1)).value = a[i];
    }
}