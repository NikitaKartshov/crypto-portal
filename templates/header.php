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
    <style>
        .profile-trigger {
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
        }
        .arrow-down-svg {
            transition: transform 0.3s ease;
        }
        .user-profile:hover .arrow-down-svg {
            transform: rotate(180deg);
        }
        .dropdown-menu {
            display: none;
            position: absolute;
            right: 0;
            top: 100%;
            z-index: 1000;
            padding-top: 10px;
            margin-top: 0;
        }
        .user-profile:hover .dropdown-menu {
            display: block;
        }
        .user-profile {
            position: relative;
            display: flex;
            align-items: center;
            height: 100%;
        }
    </style>
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
                        <span style="color: white;"><?php echo htmlspecialchars($_SESSION['username']); ?></span>
                        <svg class="arrow-down-svg" width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M6 9L12 15L18 9" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div>
                    <div class="dropdown-menu">
                        <div class="dropdown-header">
                            <div class="avatar-large"></div>
                            <p class="user-name"><?php echo htmlspecialchars($_SESSION['username']); ?></p>
                        </div>
                        <ul class="dropdown-list">
                            <li><a href="settings.php">Настройки</a></li>
                            <li><a href="help.php">Помощь</a></li>
                            <li><hr style="border: 0; border-top: 1px solid #334155; margin: 10px 0;"></li>
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