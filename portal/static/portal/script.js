function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const themeButtons = document.querySelectorAll('[data-theme-value]');

themeButtons.forEach(button => {
    button.addEventListener('click', function() {
        const theme = this.getAttribute('data-theme-value');
        document.documentElement.setAttribute('data-bs-theme', theme);

        themeButtons.forEach(btn => btn.classList.remove('active'));
        this.classList.add('active');

        fetch('/settings/update-theme/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ 'theme': theme })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status !== 'ok') console.error("Ошибка сохранения темы");
        })
        .catch(err => console.error("Ошибка сети:", err));
    });
});