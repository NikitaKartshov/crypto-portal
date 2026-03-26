<?php

$host = 'localhost';
$user = 'root';
$pass = '';
$db   = 'crypto_db';

$conn = new mysqli($host, $user, $pass, $db);


if ($conn->connect_error) {
    die("<p style='color:red'>Ошибка подключения к базе: " . $conn->connect_error . "</p>");
}

$message = "";


if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $conn->real_escape_string($_POST['username']);
    // Хешируем пароль (для ИБ это критично!)
    $password = password_hash($_POST['password'], PASSWORD_BCRYPT);

    $sql = "INSERT INTO users (username, password_hash) VALUES ('$username', '$password')";

    if ($conn->query($sql) === TRUE) {
        $message = "<p style='color:green'>Пользователь $username успешно зарегистрирован!</p>";
    } else {
        $message = "<p style='color:red'>Ошибка: " . $conn->error . "</p>";
    }
}
?>

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Crypto Portal - Регистрация</title>
    <style>
        body { background: #1a1a1a; color: white; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: #2d2d2d; padding: 30px; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); text-align: center; }
        input { display: block; width: 250px; margin: 15px 0; padding: 12px; border-radius: 5px; border: 1px solid #444; background: #333; color: white; }
        button { width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Создать аккаунт</h2>
        <?php echo $message; ?>
        <form method="POST">
            <input type="text" name="username" placeholder="Логин" required>
            <input type="password" name="password" placeholder="Пароль" required>
            <button type="submit">Зарегистрироваться</button>
        </form>
    </div>
</body>
</html>