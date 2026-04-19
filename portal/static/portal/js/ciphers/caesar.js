function encrypt(text, key) {
    let shift = parseInt(key) || 0;
    return text.split('').map(char => {
        if (char.match(/[a-z]/i)) {
            let code = char.charCodeAt(0);
            let start = (code >= 65 && code <= 90) ? 65 : 97;
            return String.fromCharCode(((code - start + shift) % 26 + 26) % 26 + start);
        } else if (char.match(/[а-яё]/i)) {
            let code = char.charCodeAt(0);
            let start = (char.toLowerCase() === char) ? 1072 : 1040;
            if (char === 'ё') return 'ж'; 
            if (char === 'Ё') return 'Ж';
            return String.fromCharCode(((code - start + shift) % 32 + 32) % 32 + start);
        }
        return char;
    }).join('');
}

function decrypt(text, key) {
    return encrypt(text, -key);
}