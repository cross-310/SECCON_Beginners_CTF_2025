function decryptFlag(encryptedFlag, secretKey) {
  try {
    const key = atob(secretKey);
    const encryptedBytes = atob(encryptedFlag);
    let decrypted = "";
    for (let i = 0; i < encryptedBytes.length; i++) {
      const keyChar = key.charCodeAt(i % key.length);
      const encryptedChar = encryptedBytes.charCodeAt(i);
      decrypted += String.fromCharCode(encryptedChar ^ keyChar);
    }
    return decrypted;
  } catch (error) {
    return "decrypt error";
  }
}

const encryptedFlag = "CB0IUxsUCFhWEl9RBUAZWBM=";
const secretKey = "a2luZ3lvZmxhZzIwMjU=";

console.log(decryptFlag(encryptedFlag, secretKey));