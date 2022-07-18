const phone = document.getElementsByName('phone')[0];
phone.value = "+977"
const submitBtn = document.querySelector('.btn-primary');

submitBtn.addEventListener("click", (e) => {
    e.preventDefault();
    if (phone.value.length > 14 || phone.value.length < 10) {
        alert('phone number should be of length 10')
        return;
    }
    if (phone.value.slice(0, 4) != "+977") {
        alert('only nepal phone number allowed');
        return;
    }
    e.target.parentElement.submit();
})
