function gcd(a, b) {
    while (b !== 0n) {
        let t = b;
        b = a % b;
        a = t;
    }
    return a;
}

function modPow(base, exponent, modulus) {
    if (modulus === 1n) return 0n;
    let result = 1n;
    base = base % modulus;
    while (exponent > 0n) {
        if (exponent % 2n === 1n) result = (result * base) % modulus;
        exponent = exponent / 2n;
        base = (base * base) % modulus;
    }
    return result;
}

function modInverse(e, phi) {
    let m0 = phi, t, q;
    let x0 = 0n, x1 = 1n;
    if (phi === 1n) return 0n;
    while (e > 1n) {
        q = e / phi;
        t = phi;
        phi = e % phi;
        e = t;
        t = x0;
        x0 = x1 - q * x0;
        x1 = t;
    }
    if (x1 < 0n) x1 += m0;
    return x1;
}

function generateRSAKeys(pIn, qIn) {
    const p = BigInt(pIn);
    const q = BigInt(qIn);
    const n = p * q;
    const phi = (p - 1n) * (q - 1n);
    
    let e = 65537n;
    if (e >= phi || gcd(e, phi) !== 1n) {
        e = 3n;
        while (gcd(e, phi) !== 1n) {
            e += 2n;
        }
    }
    
    const d = modInverse(e, phi);
    return {
        publicKey: { e: e.toString(), n: n.toString() },
        privateKey: { d: d.toString(), n: n.toString() }
    };
}

function getHashHex(str) {
    let hash = 5381;
    for (let i = 0; i < str.length; i++) {
        hash = (hash * 33) ^ str.charCodeAt(i);
    }
    return (hash >>> 0).toString(16).padStart(8, '0');
}

function encrypt(text, key) {
    if (!key || !text) return '';
    try {
        const parts = key.split(',');
        const e = BigInt(parts[0].trim());
        const n = BigInt(parts[1].trim());
        
        const hashHex = getHashHex(text);
        const fullPayload = text + "[SIG]" + hashHex;
        
        let finalHex = '';
        const chunkSize = 40;
        
        for (let i = 0; i < fullPayload.length; i += chunkSize) {
            const chunk = fullPayload.substring(i, i + chunkSize);
            const encoder = new TextEncoder();
            const bytes = encoder.encode(chunk);
            let chunkHex = '';
            bytes.forEach(b => chunkHex += b.toString(16).padStart(2, '0'));
            
            const messageBigInt = BigInt('0x' + chunkHex);
            if (messageBigInt >= n) {
                throw new Error("Блок текста слишком велик.");
            }
            
            const cipherBigInt = modPow(messageBigInt, e, n);
            finalHex += cipherBigInt.toString(16).padStart(420, '0');
        }
        
        return BigInt('0x' + finalHex).toString();
    } catch (err) {
        return "Ошибка шифрования: " + err.message;
    }
}

function decrypt(text, key) {
    if (!key || !text) return '';
    try {
        const parts = key.split(',');
        const d = BigInt(parts[0].trim());
        const n = BigInt(parts[1].trim());
        
        let finalHex = BigInt(text.trim()).toString(16);
        const remainder = finalHex.length % 420;
        if (remainder !== 0) {
            finalHex = finalHex.padStart(finalHex.length + (420 - remainder), '0');
        }
        
        let fullPayload = '';
        for (let i = 0; i < finalHex.length; i += 420) {
            const cHex = finalHex.substring(i, i + 420);
            const ciphertextBigInt = BigInt('0x' + cHex);
            const decryptedBigInt = modPow(ciphertextBigInt, d, n);
            
            let mHex = decryptedBigInt.toString(16);
            if (mHex.length % 2 !== 0) mHex = '0' + mHex;
            
            const matches = mHex.match(/.{1,2}/g);
            if (matches) {
                const bytes = new Uint8Array(matches.map(byte => parseInt(byte, 16)));
                fullPayload += new TextDecoder().decode(bytes);
            }
        }
        
        const markerIdx = fullPayload.lastIndexOf("[SIG]");
        if (markerIdx === -1) {
            return "Ошибка: подпись неверна!";
        }
        
        const originalText = fullPayload.substring(0, markerIdx);
        const providedHashHex = fullPayload.substring(markerIdx + 5);
        const expectedHashHex = getHashHex(originalText);
        
        if (providedHashHex !== expectedHashHex) {
            return "Ошибка: подпись неверна!";
        }
        
        return originalText;
    } catch (err) {
        return "Ошибка: подпись неверна!";
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('rsa-generate-btn');
    const pubOutput = document.getElementById('rsa-pub-output');
    const privOutput = document.getElementById('rsa-priv-output');

    const insertPubBtn = document.getElementById('rsa-insert-pub');
    const insertPrivBtn = document.getElementById('rsa-insert-priv');
    
    const inputPlain = document.getElementById('rsa-input-plain');
    const inputPubKey = document.getElementById('rsa-input-pubkey');
    const encryptBtn = document.getElementById('rsa-encrypt-btn');
    const outputCipher = document.getElementById('rsa-output-cipher');

    const inputCipher = document.getElementById('rsa-input-cipher');
    const inputPrivKey = document.getElementById('rsa-input-privkey');
    const decryptBtn = document.getElementById('rsa-decrypt-btn');
    const outputPlain = document.getElementById('rsa-output-plain');
    const corruptBtn = document.getElementById('rsa-corrupt-btn');

    if (pubOutput) pubOutput.value = '';
    if (privOutput) privOutput.value = '';
    if (inputPubKey) inputPubKey.value = '';
    if (inputPrivKey) inputPrivKey.value = '';

    if (generateBtn) {
        generateBtn.addEventListener('click', () => {
            const primePairs = [
                {
                    p: 18950509464150320009302779293362499442798837980204355843607948614285285154124947594578054377448087686324641960342681663608027721631570668183224934992118635150719451760354593946400121869110000392111017708955194119055296643534168623739741259316104835333n, 
                    q: 71052858332017462452660548080668727763926987468850442478718268520323970072909680060839743252390680710722205553879561576621477827176480068025640800177646684759069653926043989585328371236960492126052067803026464487254678897602721581457107470462249718527n
                },
                {
                    p: 98288009394135790106505086095561304473183600264715831423836941823601016482546600723216015579125336677770796796316755820816918173118860510326422421229643138317351178414806989581472589911137692380369852695604980825800727371166969772451670963745983768581n, 
                    q: 18190939783163615957852656069860372159554440979043696396008378752000100312412745267035747326264166226969987111395178909371166945238919729735949877066650229614335441497417171609679878165140788146947594103705550071278639625232689206450521134067301191091n
                }
            ];
            
            const randomPair = primePairs[Math.floor(Math.random() * primePairs.length)];
            const keys = generateRSAKeys(randomPair.p, randomPair.q);
            
            pubOutput.value = keys.publicKey.e + ", " + keys.publicKey.n;
            privOutput.value = keys.privateKey.d + ", " + keys.privateKey.n;
        });
    }

    if (insertPubBtn) {
        insertPubBtn.addEventListener('click', () => {
            if (!pubOutput.value) return alert('Сначала сгенерируйте ключи!');
            inputPubKey.value = pubOutput.value;
        });
    }

    if (insertPrivBtn) {
        insertPrivBtn.addEventListener('click', () => {
            if (!privOutput.value) return alert('Сначала сгенерируйте ключи!');
            inputPrivKey.value = privOutput.value;
        });
    }

    if (encryptBtn) {
        encryptBtn.addEventListener('click', () => {
            const text = inputPlain.value.trim();
            const key = inputPubKey.value.trim();

            if (!text || !key) {
                alert("Заполните исходный текст и открытый ключ!");
                return;
            }

            const resultCipher = encrypt(text, key);
            outputCipher.value = resultCipher;
            
            if (!resultCipher.startsWith("Ошибка")) {
                inputCipher.value = resultCipher;
            }
        });
    }

    if (decryptBtn) {
        decryptBtn.addEventListener('click', () => {
            const cipherText = inputCipher.value.trim();
            const key = inputPrivKey.value.trim();

            if (!cipherText || !key) {
                alert("Заполните поле полученного шифротекста и закрытый ключ!");
                return;
            }

            const decryptionResult = decrypt(cipherText, key);
            outputPlain.value = decryptionResult;

            if (decryptionResult.startsWith("Ошибка")) {
                outputPlain.className = "form-control is-invalid text-danger fw-bold";
            } else {
                outputPlain.className = "form-control is-valid text-success fw-bold";
            }
        });
    }

    if (corruptBtn) {
        corruptBtn.addEventListener('click', () => {
            const cipherField = document.getElementById('rsa-input-cipher');
            let currentText = cipherField.value.trim();

            if (!currentText) {
                alert("Поле шифротекста пустое! Нечего повреждать.");
                return;
            }

            if (isNaN(Number(currentText)) && !/^[0-9a-fA-F]+$/.test(currentText)) {
                alert("В поле находится некорректный шифротекст.");
                return;
            }

            let chars = currentText.split('');
            const minIndex = Math.min(5, chars.length - 1); 
            const randomIndex = Math.floor(Math.random() * (chars.length - minIndex)) + minIndex;
            const currentChar = chars[randomIndex];
            let newChar = '7';

            if (currentChar === '7') {
                newChar = '3';
            } else if (/[0-9]/.test(currentChar)) {
                newChar = String((parseInt(currentChar) + 1) % 10);
            } else {
                newChar = 'a';
            }

            chars[randomIndex] = newChar;
            cipherField.value = chars.join('');

            cipherField.style.backgroundColor = 'rgba(220, 53, 69, 0.2)';
            setTimeout(() => {
                cipherField.style.backgroundColor = '';
                alert(`Данные успешно повреждены! Изменён символ на позиции ${randomIndex}. Теперь попробуйте расшифровать.`);
            }, 200);
        });
    }
});