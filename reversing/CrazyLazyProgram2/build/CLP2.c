#include <stdio.h>
#include <string.h>


void main(){
    char flag[33];
    printf("Enter the flag: ");
    scanf("%33c",flag);
    int c=0;

    goto check0;



check6:if(flag[c]!=0x47){return;}else{c++;goto check7;}                                                                                 
check7:if(flag[c]!=0x4f){return;}else{c++;goto check8;}                                                                                 
check8:if(flag[c]!=0x54){return;}else{c++;goto check9;}                                                                                 
check9:if(flag[c]!=0x4f){return;}else{c++;goto check10;} 
 
                                                                            
check26:if(flag[c]!=0x33){return;}else{c++;goto check27;}

check2:if(flag[c]!=0x66){return;}else{c++;goto check3;}                                                                                 
check3:if(flag[c]!=0x34){return;}else{c++;goto check4;}              


check11:if(flag[c]!=0x47){return;}else{c++;goto check12;}                                                                               
check12:if(flag[c]!=0x30){return;}else{c++;goto check13;}                                                                               
check13:if(flag[c]!=0x54){return;}else{c++;goto check14;}   


check19:if(flag[c]!=0x30){return;}else{c++;goto check20;}                                                                               
check20:if(flag[c]!=0x5f){return;}else{c++;goto check21;}                                                                               
check21:if(flag[c]!=0x4e){return;}else{c++;goto check22;}                                                                               
check22:if(flag[c]!=0x30){return;}else{c++;goto check23;}                                                                              

check31:if(flag[c]!=0x30){return;}else{c++;goto check32;}                                                                               
check0:if(flag[c]!=0x63){return;}else{c++;goto check1;}                                                                                 
                                                                               
check10:if(flag[c]!=0x5f){return;}else{c++;goto check11;}                                                                              



check32:if(flag[c]!=0x7d){return;}else{printf("Flag is correct!\n"); return; }
 
check17:if(flag[c]!=0x30){return;}else{c++;goto check18;}      

check24:if(flag[c]!=0x30){return;}else{c++;goto check25;}                                                                               
check25:if(flag[c]!=0x72){return;}else{c++;goto check26;}   
 
check23:if(flag[c]!=0x6d){return;}else{c++;goto check24;}                                                                                                                                                           
check14:if(flag[c]!=0x30){return;}else{c++;goto check15;}                                                                               
check15:if(flag[c]!=0x5f){return;}else{c++;goto check16;}  

check16:if(flag[c]!=0x39){return;}else{c++;goto check17;}                                                                               
                                                                               
check27:if(flag[c]!=0x5f){return;}else{c++;goto check28;}                                                                               
check28:if(flag[c]!=0x39){return;}else{c++;goto check29;}                                                                               
check29:if(flag[c]!=0x30){return;}else{c++;goto check30;}                                                                               
check30:if(flag[c]!=0x74){return;}else{c++;goto check31;}                                                                              

check1:if(flag[c]!=0x74){return;}else{c++;goto check2;}                                                                                
check18:if(flag[c]!=0x74){return;}else{c++;goto check19;}                                                                              

                                                                   
check4:if(flag[c]!=0x62){return;}else{c++;goto check5;}                                                                                 
check5:if(flag[c]!=0x7b){return;}else{c++;goto check6;}                                                                                 
                                                                         




}
