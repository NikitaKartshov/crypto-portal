<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Криптография - Обучающий портал</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="main-header">
        <div class="container header-content">
            <div class="logo">
                <a href="index.php">
                    <span class="logo-icon">🔒</span> Криптография
                </a>
            </div>
            <nav class="main-nav">
                <ul>
                    <li><a href="theory.php">Теория</a></li>
                    <li><a href="practice.php">Практика</a></li>
                    <li><a href="tools.php">Инструменты</a></li>
                </ul>
            </nav>
            <div class="user-profile">
                <?php if (isset($_SESSION['user_id'])): ?>
                    <div class="profile-trigger">
                        <div class="avatar-placeholder"></div>
                        <img src="icons/chevron-down.svg" class="arrow-down" alt="Открыть меню">
                    </div>
                    <div class="dropdown-menu">
                        <div class="dropdown-header">
                            <div class="avatar-large"></div>
                            <p class="user-name"><?php echo htmlspecialchars($_SESSION['username']); ?></p>
                        </div>
                        <ul class="dropdown-list">
                            <li><a href="settings.php">Настройки</a></li>
                            <li><hr></li>
                            <li><a href="logout.php" class="logout">Выйти</a></li>
                        </ul>
                    </div>
                <?php else: ?>
    <div class="auth-buttons">
        <a href="auth.php" class="btn-primary" style="text-decoration: none; padding: 10px 20px; background: #3b82f6; color: white; border-radius: 8px; font-weight: 500;">Войти / Регистрация</a>
    </div>
<?php endif; ?>
            </div>
        </div>
    </header>