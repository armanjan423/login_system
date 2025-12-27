document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('input');

    // Add floating effects or focus animations
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.parentElement.parentElement.querySelector('label').style.color = '#00d2ff';
            input.parentElement.parentElement.querySelector('label').style.transform = 'translateY(-2px)';
        });

        input.addEventListener('blur', () => {
            if (input.value === '') {
                input.parentElement.parentElement.querySelector('label').style.color = 'rgba(255, 255, 255, 0.8)';
                input.parentElement.parentElement.querySelector('label').style.transform = 'translateY(0)';
            }
        });
    });

    // Form submission animation
    const form = document.querySelector('form');
    const loginBtn = document.querySelector('.btn-login');

    form.addEventListener('submit', (e) => {
        if (loginBtn.innerText !== 'Signing in...') {
            loginBtn.style.width = loginBtn.offsetWidth + 'px';
            loginBtn.innerText = 'Signing in...';
            loginBtn.style.opacity = '0.7';
            loginBtn.style.cursor = 'not-allowed';
        }
    });
});
