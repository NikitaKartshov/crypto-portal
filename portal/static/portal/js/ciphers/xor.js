function processXOR(text, key, mode) {
    if (!text || !key) return '';

    if (mode === 'binary') {
        const cleanText = text.replace(/\s+/g, '');
        const cleanKey = key.replace(/\s+/g, '');
        
        if (!/^[01]+$/.test(cleanText) || !/^[01]+$/.test(cleanKey)) {
            throw new Error("В двоичном режиме разрешены только 0 и 1!");
        }
        
        let result = '';
        for (let i = 0; i < cleanText.length; i++) {
            const textBit = parseInt(cleanText[i]);
            const keyBit = parseInt(cleanKey[i % cleanKey.length]);
            result += (textBit ^ keyBit).toString();
        }
        return result;
        
    } else {
        let result = '';
        for (let i = 0; i < text.length; i++) {
            const textCharCode = text.charCodeAt(i);
            const keyCharCode = key.charCodeAt(i % key.length);
            result += String.fromCharCode(textCharCode ^ keyCharCode);
        }
        return result;
    }
}