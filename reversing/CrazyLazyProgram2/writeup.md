
## solution
`gcc`にて実行形式ファイルに変換し、Ghidraに投げると`main`内に以下の処理があります
```c
  if (((((((((local_38 == 'c') && (local_c = 1, cStack_37 == 't')) &&
           (local_c = 2, cStack_36 == 'f')) &&
          (((local_c = 3, cStack_35 == '4' && (local_c = 4, cStack_34 == 'b')) &&
           ((local_c = 5, cStack_33 == '{' &&
            ((local_c = 6, cStack_32 == 'G' && (local_c = 7, cStack_31 == 'O')))))))) &&
         (local_c = 8, cStack_30 == 'T')) &&
        (((((local_c = 9, cStack_2f == 'O' && (local_c = 10, cStack_2e == '_')) &&
           (local_c = 0xb, cStack_2d == 'G')) &&
          ((local_c = 0xc, cStack_2c == '0' && (local_c = 0xd, cStack_2b == 'T')))) &&
         (local_c = 0xe, cStack_2a == '0')))) &&
       (((local_c = 0xf, cStack_29 == '_' && (local_c = 0x10, cStack_28 == '9')) &&
        (((local_c = 0x11, cStack_27 == '0' &&
          (((local_c = 0x12, cStack_26 == 't' && (local_c = 0x13, cStack_25 == '0')) &&
           (local_c = 0x14, cStack_24 == '_')))) &&
         (((local_c = 0x15, cStack_23 == 'N' && (local_c = 0x16, cStack_22 == '0')) &&
          (local_c = 0x17, cStack_21 == 'm')))))))) &&
      (((local_c = 0x18, cStack_20 == '0' && (local_c = 0x19, cStack_1f == 'r')) &&
       ((local_c = 0x1a, cStack_1e == '3' &&
        (((local_c = 0x1b, cStack_1d == '_' && (local_c = 0x1c, cStack_1c == '9')) &&
         (local_c = 0x1d, cStack_1b == '0')))))))) &&
     (((local_c = 0x1e, cStack_1a == 't' && (local_c = 0x1f, cStack_19 == '0')) &&
      (local_c = 0x20, cStack_18 == '}')))) {
    puts("Flag is correct!");
  }
```
local_38のcという文字列と、local_cがインデックス・cStack_XXが値であると分かります

