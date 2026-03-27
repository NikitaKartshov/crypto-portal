<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
$host = 'localhost';
$db   = 'crypto_db';
$user = 'root';
$pass = '';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$db;charset=utf8", $user, $pass);
} catch (PDOException $e) {
    die("Ошибка подключения: " . $e->getMessage());
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];

    
    $stmt = $pdo->prepare("SELECT * FROM users WHERE username = ?");
    $stmt->execute([$username]);
    $user_data = $stmt->fetch();

   
    if ($user_data && password_verify($password, $user_data['password_hash'])) {
       
        $_SESSION['user_id'] = $user_data['id'];
        $_SESSION['username'] = $user_data['username'];
        
        header("Location: index.php"); // Уходим на главную
        exit();
    } else {
        echo "Неверный логин или пароль! <a href='login.php'>Назад</a>";
    }
}