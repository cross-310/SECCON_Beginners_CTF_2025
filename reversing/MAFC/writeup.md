
## solution
デコンパイルに投げる(ここではGhidra)
```cpp
void FUN_1400011a0(void)

{
  uint uVar1;
  code *pcVar2;
  longlong lVar3;
  BOOL BVar4;
  DWORD nNumberOfBytesToRead;
  HANDLE hFile;
  HANDLE hFile_00;
  void *pvVar5;
  longlong lVar6;
  BYTE *pbData;
  BYTE *_Memory;
  ulonglong _Size;
  longlong lVar7;
  BYTE *pBVar8;
  undefined1 auStackY_b8 [32];
  HCRYPTKEY local_78;
  HCRYPTPROV local_70;
  BYTE local_68 [8];
  DWORD local_60;
  DWORD local_5c;
  HCRYPTHASH local_58;
  BYTE local_50 [24];
  ulonglong local_38;
  
  local_38 = DAT_140005000 ^ (ulonglong)auStackY_b8;
  pbData = (BYTE *)0x0;
  hFile = CreateFileA("flag.txt",0x80000000,1,(LPSECURITY_ATTRIBUTES)0x0,3,0x80,(HANDLE)0x0);
  if (hFile == (HANDLE)0xffffffffffffffff) {
    puts("Failed to handle flag.txt\n");
  }
  else {
    hFile_00 = CreateFileA("flag.encrypted",0x40000000,0,(LPSECURITY_ATTRIBUTES)0x0,2,0x80,
                           (HANDLE)0x0);
    if (hFile_00 == (HANDLE)0xffffffffffffffff) {
      puts("Failed to handle flag.encrypted\n");
      goto LAB_140001637;
    }
    BVar4 = CryptAcquireContextW
                      (&local_70,(LPCWSTR)0x0,
                       L"Microsoft Enhanced RSA and AES Cryptographic Provider",0x18,0);
    if ((BVar4 == 0) &&
       (BVar4 = CryptAcquireContextW
                          (&local_70,(LPCWSTR)0x0,
                           L"Microsoft Enhanced RSA and AES Cryptographic Provider",0x18,8),
       BVar4 == 0)) {
      puts("CryptAcquireContext() Error\n");
      goto LAB_140001637;
    }
    BVar4 = CryptCreateHash(local_70,0x800c,0,0,&local_58);
    if (BVar4 == 0) {
      puts("CryptCreateHash() Error\n");
      goto LAB_140001637;
    }
    builtin_memcpy(local_50 + 0x10,"Key",4);
    builtin_memcpy(local_50,"ThisIsTheEncrypt",0x10);
    lVar6 = -1;
    do {
      lVar7 = lVar6 + 1;
      lVar3 = lVar6 + 1;
      lVar6 = lVar7;
    } while (local_50[lVar3] != '\0');
    BVar4 = CryptHashData(local_58,local_50,(DWORD)lVar7,0);
    if (BVar4 == 0) {
      puts("CryptHashData() Error\n");
      goto LAB_140001637;
    }
    BVar4 = CryptDeriveKey(local_70,0x6610,local_58,0x1000000,&local_78);
    if (BVar4 == 0) {
      puts("CryptDeriveKey() Error\n");
      goto LAB_140001637;
    }
    local_68[0] = '\x01';
    local_68[1] = '\0';
    local_68[2] = '\0';
    local_68[3] = '\0';
    BVar4 = CryptSetKeyParam(local_78,3,local_68,0);
    if (BVar4 == 0) {
      puts("CryptSeKeyParam() Error\n");
      goto LAB_140001637;
    }
    BVar4 = CryptSetKeyParam(local_78,1,(BYTE *)L"IVCanObfuscation",0);
    if (BVar4 == 0) {
      puts("CryptSeKeyParam() with IV Error\n");
      goto LAB_140001637;
    }
    local_68[4] = '\x01';
    local_68[5] = '\0';
    local_68[6] = '\0';
    local_68[7] = '\0';
    BVar4 = CryptSetKeyParam(local_78,4,local_68 + 4,0);
    if (BVar4 == 0) {
      puts("CryptSetKeyParam() with set MODE Error\n");
      goto LAB_140001637;
    }
    nNumberOfBytesToRead = GetFileSize(hFile,(LPDWORD)0x0);
    uVar1 = nNumberOfBytesToRead + 0x10;
    _Size = (ulonglong)uVar1;
    pBVar8 = pbData;
    if (uVar1 != 0) {
      if (_Size < 0x1000) {
        pbData = (BYTE *)operator_new(_Size);
      }
      else {
        if ((ulonglong)uVar1 + 0x27 <= _Size) {
          FUN_140001100();
          pcVar2 = (code *)swi(3);
          (*pcVar2)();
          return;
        }
        pvVar5 = operator_new((ulonglong)uVar1 + 0x27);
        if (pvVar5 == (void *)0x0) goto LAB_140001653;
        pbData = (BYTE *)((longlong)pvVar5 + 0x27U & 0xffffffffffffffe0);
        *(void **)(pbData + -8) = pvVar5;
      }
      pBVar8 = pbData + _Size;
      memset(pbData,0,_Size);
    }
    local_60 = 0;
    BVar4 = ReadFile(hFile,pbData,nNumberOfBytesToRead,&local_60,(LPOVERLAPPED)0x0);
    if (BVar4 == 0) {
      puts("ReadFile() Error\n");
    }
    else {
      lVar6 = -1;
      do {
        lVar6 = lVar6 + 1;
      } while (pbData[lVar6] != '\0');
      local_5c = (int)lVar6 + 1;
      BVar4 = CryptEncrypt(local_78,0,1,0,pbData,&local_5c,0x40);
      if (BVar4 == 0) {
        puts("CryptEncrypt() Error\n");
      }
      else {
        BVar4 = WriteFile(hFile_00,pbData,0x40,(LPDWORD)0x0,(LPOVERLAPPED)0x0);
        if (BVar4 == 0) {
          puts("WriteFile() error\n");
        }
        else {
          CloseHandle(hFile);
          CloseHandle(hFile_00);
          BVar4 = DeleteFileA("flag.txt");
          if (BVar4 == 0) {
            puts("DeleteFileA() error\n");
          }
          else {
            BVar4 = CryptDestroyKey(local_78);
            if (BVar4 == 0) {
              puts("CryptDestroyKey() error\n");
            }
            else {
              BVar4 = CryptDestroyHash(local_58);
              if (BVar4 == 0) {
                puts("CryptDestroyHash() error\n");
              }
              else {
                BVar4 = CryptReleaseContext(local_70,0);
                if (BVar4 == 0) {
                  puts("CryptReleaseContext() error\n");
                }
              }
            }
          }
        }
      }
    }
    if (pbData != (BYTE *)0x0) {
      _Memory = pbData;
      if ((0xfff < (ulonglong)((longlong)pBVar8 - (longlong)pbData)) &&
         (_Memory = *(BYTE **)(pbData + -8), (BYTE *)0x1f < pbData + (-8 - (longlong)_Memory))) {
LAB_140001653:
                    /* WARNING: Subroutine does not return */
        _invoke_watson((wchar_t *)0x0,(wchar_t *)0x0,(wchar_t *)0x0,0,0);
      }
      free(_Memory);
    }
  }
LAB_140001637:
  FUN_140001680(local_38 ^ (ulonglong)auStackY_b8);
  return;
}
```
複雑に書いてあるが、まとめると
- `ReadFile()`で`flag.txt`の内容を読み込む
- `Microsoft Enhanced RSA and AES Cryptographic Provider`を使用
- AES-CBCによる暗号化
- PKCS5によるPadding
- SHA-256によるハッシュ生成
- 共通鍵のPW:`ThisIsTheEncryptKey`
- 初期化ベクトルIV:`IVCanObfuscation`


## Writeup
```cpp
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
```
実行結果
```bash
here is flag:ctf4b{way_2_90!_y0u_suc3553d_2_ana1yz3_Ma1war3!!!}
```

