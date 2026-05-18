function encrypt(text, key) {
    if (!key) return text;
    let keyIndex = 0;
    const lowerKey = key.toLowerCase();

    return text.split('').map(char => {
        if (char.match(/[a-z]/i)) {
            let code = char.charCodeAt(0);
            let start = (code >= 65 && code <= 90) ? 65 : 97;
            
            let shiftChar = lowerKey[keyIndex % lowerKey.length];
            let shift = shiftChar.charCodeAt(0) - 97;
            if (shift < 0 || shift > 25) shift = 0;
            
            keyIndex++;
            return String.fromCharCode(((code - start + shift) % 26 + 26) % 26 + start);
        } else if (char.match(/[а-яё]/i)) {
            if (char === 'ё') char = 'е';
            if (char === 'Ё') char = 'Е';
            
            let code = char.charCodeAt(0);
            let start = (char.toLowerCase() === char) ? 1072 : 1040;
            
            let shiftChar = lowerKey[keyIndex % lowerKey.length];
            if (shiftChar === 'ё') shiftChar = 'е';
            let shift = shiftChar.charCodeAt(0) - 1072;
            if (shift < 0 || shift > 31) shift = 0;
            
            keyIndex++;
            return String.fromCharCode(((code - start + shift) % 32 + 32) % 32 + start);
        }
        return char;
    }).join('');
}

function decrypt(text, key) {
    if (!key) return text;
    let keyIndex = 0;
    const lowerKey = key.toLowerCase();

    return text.split('').map(char => {
        if (char.match(/[a-z]/i)) {
            let code = char.charCodeAt(0);
            let start = (code >= 65 && code <= 90) ? 65 : 97;
            
            let shiftChar = lowerKey[keyIndex % lowerKey.length];
            let shift = shiftChar.charCodeAt(0) - 97;
            if (shift < 0 || shift > 25) shift = 0;
            
            keyIndex++;
            return String.fromCharCode(((code - start - shift) % 26 + 26) % 26 + start);
        } else if (char.match(/[а-яё]/i)) {
            if (char === 'ё') char = 'е';
            if (char === 'Ё') char = 'Е';
            
            let code = char.charCodeAt(0);
            let start = (char.toLowerCase() === char) ? 1072 : 1040;
            
            let shiftChar = lowerKey[keyIndex % lowerKey.length];
            if (shiftChar === 'ё') shiftChar = 'е';
            let shift = shiftChar.charCodeAt(0) - 1072;
            if (shift < 0 || shift > 31) shift = 0;
            
            keyIndex++;
            return String.fromCharCode(((code - start - shift) % 32 + 32) % 32 + start);
        }
        return char;
    }).join('');
}