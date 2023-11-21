
document.addEventListener("DOMContentLoaded", () => {
    const labelsYinputs = document.querySelectorAll('.registration-form label , .registration-form input')
    labelsYinputs.forEach((element) => {
        if (element.tagName === 'LABEL' ){
            element.classList.add('form-label')
        }
        else if (element.tagName === 'INPUT'){
            element.classList.add('form-input')
        }
    })

})