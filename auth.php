<?php include 'header.php'; ?>

<main class="container">
    <section class="auth-container" style="max-width: 450px; margin: 50px auto; background: #1e293b; border-radius: 15px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.3);">
        
        <div class="auth-tabs" style="display: flex; cursor: pointer; border-bottom: 1px solid #334155;">
            <div id="tab-login" onclick="switchTab('login')" style="flex: 1; padding: 15px; text-align: center; color: white; background: #334155; font-weight: bold;">Вход</div>
            <div id="tab-register" onclick="switchTab('register')" style="flex: 1; padding: 15px; text-align: center; color: #94a3b8; font-weight: bold;">Регистрация</div>
        </div>

        <div style="padding: 30px;">
            <form id="form-login" action="login_handler.php" method="POST">
                <div style="margin-bottom: 15px;">
                    <label style="color: #94a3b8; display: block; margin-bottom: 5px;">Логин</label>
                    <input type="text" name="username" required style="width: 100%; padding: 10px; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 8px;">
                </div>
                <div style="margin-bottom: 20px;">
                    <label style="color: #94a3b8; display: block; margin-bottom: 5px;">Пароль</label>
                    <input type="password" name="password" required style="width: 100%; padding: 10px; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 8px;">
                </div>
                <button type="submit" class="btn-primary" style="width: 100%; padding: 12px; background: #3b82f6; color: white; border: none; border-radius: 8px; font-weight: bold;">Войти</button>
            </form>

            <form id="form-register" action="registration_handler.php" method="POST" style="display: none;">
                <div style="margin-bottom: 15px;">
                    <label style="color: #94a3b8; display: block; margin-bottom: 5px;">Придумайте логин</label>
                    <input type="text" name="username" required style="width: 100%; padding: 10px; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 8px;">
                </div>
                <div style="margin-bottom: 20px;">
                    <label style="color: #94a3b8; display: block; margin-bottom: 5px;">Пароль</label>
                    <input type="password" name="password" required style="width: 100%; padding: 10px; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 8px;">
                </div>
                <button type="submit" class="btn-primary" style="width: 100%; padding: 12px; background: #10b981; color: white; border: none; border-radius: 8px; font-weight: bold;">Создать аккаунт</button>
            </form>
        </div>
    </section>
</main>

<script>
function switchTab(type) {
    const loginForm = document.getElementById('form-login');
    const registerForm = document.getElementById('form-register');
    const loginTab = document.getElementById('tab-login');
    const registerTab = document.getElementById('tab-register');

    if (type === 'login') {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
        loginTab.style.background = '#334155';
        loginTab.style.color = 'white';
        registerTab.style.background = 'transparent';
        registerTab.style.color = '#94a3b8';
    } else {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
        registerTab.style.background = '#334155';
        registerTab.style.color = 'white';
        loginTab.style.background = 'transparent';
        loginTab.style.color = '#94a3b8';
    }
}
</script>

<?php include 'footer.php'; ?>