<?php
session_start();
$host = 'localhost';
$user = 'root';
$pass = ''; 
$db   = 'crypto_db';

mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
try {
    $conn = new mysqli($host, $user, $pass, $db);
} catch (mysqli_sql_exception $e) {
    die("Ошибка подключения: " . $e->getMessage());
}

$message = "";
$active_tab = 'login'; 

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];
    if (isset($_POST['action']) && $_POST['action'] == 'register') {
        $active_tab = 'register';
        $hash = password_hash($password, PASSWORD_BCRYPT);
        try {
            $stmt = $conn->prepare("INSERT INTO users (username, password_hash) VALUES (?, ?)");
            $stmt->bind_param("ss", $username, $hash);
            $stmt->execute();
            $message = "<div style='background:#065f46; color:#a7f3d0; padding:10px; border-radius:8px; margin-bottom:15px; text-align:center;'>Регистрация успешна! Войдите.</div>";
            $active_tab = 'login';
        } catch (mysqli_sql_exception $e) {
            $message = ($e->getCode() === 1062) ? "<div style='background:#7f1d1d; color:#fecaca; padding:10px; border-radius:8px; margin-bottom:15px; text-align:center;'>Логин занят.</div>" : "Ошибка БД.";
        }
    } elseif (isset($_POST['action']) && $_POST['action'] == 'login') {
        $active_tab = 'login';
        $stmt = $conn->prepare("SELECT id, password_hash FROM users WHERE username = ?");
        $stmt->bind_param("s", $username);
        $stmt->execute();
        $res = $stmt->get_result();
        $u = $res->fetch_assoc();
        if ($u && password_verify($password, $u['password_hash'])) {
            $_SESSION['user_id'] = $u['id'];
            $_SESSION['username'] = $username;
            header("Location: index.php");
            exit();
        } else {
            $message = "<div style='background:#7f1d1d; color:#fecaca; padding:10px; border-radius:8px; margin-bottom:15px; text-align:center;'>Неверный логин или пароль.</div>";
        }
    }
}

include '../templates/header.php'; 
?>

<main class="container" style="min-height: 75vh; display: flex; flex-direction: column; justify-content: center;">
    <section class="auth-container" style="max-width: 450px; width: 100%; margin: 50px auto; background: #1e293b; border-radius: 15px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.3);">
        <div class="auth-tabs" style="display: flex; cursor: pointer; border-bottom: 1px solid #334155;">
            <div id="tab-login" onclick="switchTab('login')" style="flex: 1; padding: 15px; text-align: center; color: <?php echo $active_tab == 'login' ? 'white' : '#94a3b8'; ?>; background: <?php echo $active_tab == 'login' ? '#334155' : 'transparent'; ?>; font-weight: bold;">Вход</div>
            <div id="tab-register" onclick="switchTab('register')" style="flex: 1; padding: 15px; text-align: center; color: <?php echo $active_tab == 'register' ? 'white' : '#94a3b8'; ?>; background: <?php echo $active_tab == 'register' ? '#334155' : 'transparent'; ?>; font-weight: bold;">Регистрация</div>
        </div>

        <div style="padding: 30px;">
            <?php echo $message; ?>
            <form id="form-login" action="auth.php" method="POST" style="display: <?php echo $active_tab == 'login' ? 'block' : 'none'; ?>;">
                <input type="hidden" name="action" value="login">
                <div style="margin-bottom: 15px;">
                    <label style="color: #94a3b8; display: block; margin-bottom: 5px;">Логин</label>
                    <input type="text" name="username" required style="width: 100%; padding: 10px; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 8px;">
                </div>
                <div style="margin-bottom: 20px;">
                    <label style="color: #94a3b8; display: block; margin-bottom: 5px;">Пароль</label>
                    <input type="password" name="password" required style="width: 100%; padding: 10px; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 8px;">
                </div>
                <button type="submit" class="btn-primary" style="width: 100%; padding: 12px; background: #3b82f6; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer;">Войти</button>
            </form>

            <form id="form-register" action="auth.php" method="POST" style="display: <?php echo $active_tab == 'register' ? 'block' : 'none'; ?>;">
                <input type="hidden" name="action" value="register">
                <div style="margin-bottom: 15px;">
                    <label style="color: #94a3b8; display: block; margin-bottom: 5px;">Логин</label>
                    <input type="text" name="username" required style="width: 100%; padding: 10px; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 8px;">
                </div>
                <div style="margin-bottom: 20px;">
                    <label style="color: #94a3b8; display: block; margin-bottom: 5px;">Пароль</label>
                    <input type="password" name="password" required style="width: 100%; padding: 10px; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 8px;">
                </div>
                <button type="submit" class="btn-primary" style="width: 100%; padding: 12px; background: #10b981; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer;">Создать аккаунт</button>
            </form>
        </div>
    </section>
</main>

<script>
function switchTab(type) {
    const lF = document.getElementById('form-login'), rF = document.getElementById('form-register');
    const lT = document.getElementById('tab-login'), rT = document.getElementById('tab-register');
    if (type === 'login') {
        lF.style.display = 'block'; rF.style.display = 'none';
        lT.style.background = '#334155'; lT.style.color = 'white';
        rT.style.background = 'transparent'; rT.style.color = '#94a3b8';
    } else {
        lF.style.display = 'none'; rF.style.display = 'block';
        rT.style.background = '#334155'; rT.style.color = 'white';
        lT.style.background = 'transparent'; lT.style.color = '#94a3b8';
    }
}
</script>
<?php include '../templates/footer.php'; ?>