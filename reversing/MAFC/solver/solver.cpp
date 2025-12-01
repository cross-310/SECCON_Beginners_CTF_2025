#include <iostream>
#include <string>
#include <vector>

#include <Windows.h>
#include <Wincrypt.h>
#include <fileapi.h>

int main() {
	HANDLE hFile = CreateFileA("flag.encrypted", GENERIC_READ, FILE_SHARE_READ, 0, 3, FILE_ATTRIBUTE_NORMAL, NULL);
	if (hFile == (HANDLE)-1) {
		printf("flag.encrypted HANDLE Error\n");
		return -1;
	}


	HCRYPTPROV prov;
	if (!CryptAcquireContextW(&prov, 0, L"Microsoft Enhanced RSA and AES Cryptographic Provider", 0x18, 0)) {
		printf("CryptAcquireContextW() Error\n");
		return -1;
	}

	HCRYPTHASH hash;
	if (!CryptCreateHash(prov, 0x800c, 0, 0, &hash)) {
		printf("CryptCreateHash() Error\n");
		return -1;
	}

	const BYTE PW[] = "ThisIsTheEncryptKey";
	if (!CryptHashData(hash, PW, (DWORD)strlen((char*)PW), 0)) {
		printf("CryptHashData() Error\n");
		return -1;
	}

	HCRYPTKEY key;
	DWORD AESlen = 0x1000000;
	if (!CryptDeriveKey(prov, 0x6610, hash, AESlen, &key)) {
		printf("CryptDeriveKey() Error\n");
		return -1;
	}

	BYTE pbData[4];
	pbData[0] = '\x01';
	pbData[1] = '\0';
	pbData[2] = '\0';
	pbData[3] = '\0';

	if (!CryptSetKeyParam(key, 3, pbData, 0)) {
		printf("CryptSetKeyParam() Error\n");
		return -1;
	}

	if (!CryptSetKeyParam(key, 1, (BYTE*)L"IVCanObfuscation", 0)) {
		printf("CryptSetKeyParam() with IV Error\n");
		return -1;
	}

	if (!CryptSetKeyParam(key, 4, pbData, 0)) {
		printf("CryptSetKeyParam() with set MODE Error\n");
		return -1;
	}


	DWORD fileSize = GetFileSize(hFile, NULL);
	std::vector<BYTE> buffer(fileSize + 16);
	DWORD bytesRead = 0;
	if (!ReadFile(hFile, buffer.data(), fileSize, &bytesRead, NULL)) {
		printf("ReadFile() Error\n");
		return -1;
	}

	if (!CryptDecrypt(key, 0, TRUE, 0, buffer.data(), &bytesRead)) {
		printf("CryptDecrypt() Error\n");
		return -1;
	}

	CloseHandle(hFile);
	if (CryptDestroyKey(key) && CryptDestroyHash(hash) && CryptReleaseContext(prov, 0)) {

	printf("here is flag:%s\n", buffer.data());
	
	return 0;
	}else{
		printf("something goes wrong!\n");
		return -1;
	}
}