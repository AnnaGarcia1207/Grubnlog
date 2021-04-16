const titleInput = document.querySelector('input[name=title]');
const slugInput = document.querySelector('input[name=slug]');

const slugify = (val) => {
    var num = Math.floor((Math.random() * 10000) + 1);
    var str = num.toString();

    return val.toString().toLowerCase().trim()
        .replace(/&/g, '-and-')         // Replace & with 'and'
        .replace(/[\s\W-]+/g, '-')      // Replace spaces, non-word characters and dashes with a single dash (-)
        .concat("-",str)

};

titleInput.addEventListener('keyup', (e) => {

    slugInput.setAttribute('value', slugify(titleInput.value));
});