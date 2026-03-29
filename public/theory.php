<?php include '../templates/header.php'; ?>

<main class="container">
    <section class="osnova-section">
        <div class="osnova-text">
            <h1>Основы криптографии</h1>
            <p style="color: #94a3b8; margin-top: 20px; font-size: 18px;">Изучи фундаментальные принципы защиты информации.</p>
        </div>
        <div class="osnova-icons"></div>
    </section>

    <section class="learning-section">
        <h2>Модули обучения</h2>
        <div class="cards-grid">
            <div class="card">
                <div class="progress-bar"><div class="fill" style="width: 100%"></div></div>
                <h3>Введение в криптографию</h3>
                <p style="color: #64748b; font-size: 14px; margin-top: 10px;">Основные термины, цели и история развития науки.</p>
                <a href="lesson_1.php" style="text-decoration: none;">
                    <button class="btn-primary">Изучить</button>
                </a>
            </div>

            <div class="card">
                <div class="progress-bar"><div class="fill" style="width: 10%"></div></div>
                <h3>Симметричные шифры</h3>
                <p style="color: #64748b; font-size: 14px; margin-top: 10px;">Методы шифрования с использованием одного ключа.</p>
                <a href="lesson_2.php" style="text-decoration: none;">
                    <button class="btn-primary">Изучить</button>
                </a>
            </div>

            <div class="card">
                <div class="progress-bar"><div class="fill" style="width: 0%"></div></div>
                <h3>Асимметричное шифрование</h3>
                <p style="color: #64748b; font-size: 14px; margin-top: 10px;">Принципы работы открытых и закрытых ключей.</p>
                <a href="lesson_3.php" style="text-decoration: none;">
                    <button class="btn-primary">Изучить</button>
                </a>
            </div>

            <div class="card">
                <div class="progress-bar"><div class="fill" style="width: 0%"></div></div>
                <h3>Хеширование</h3>
                <p style="color: #64748b; font-size: 14px; margin-top: 10px;">Целостность данных и алгоритмы MD5, SHA.</p>
                <a href="lesson_4.php" style="text-decoration: none;">
                    <button class="btn-primary">Изучить</button>
                </a>
            </div>
        </div>
    </section>

    <section class="sandbox-section">
        <div class="sandbox-header">
            <h3>Дополнительные материалы</h3>
            <p>Глоссарий терминов и список рекомендуемой литературы для глубокого погружения.</p>
        </div>
    </section>
</main>

<?php include '../templates/footer.php'; ?>