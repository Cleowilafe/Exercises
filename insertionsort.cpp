#include <iostream>

int main() {
    
    int array [6] = {5,4,3,2,1,8};
    int len = sizeof(array)/sizeof(array[0]);


    for (int i = 1; i < len; i++){

        int chave = array[i];
        int j = i - 1;

        while (j >= 0 && array[j] > chave){
            array [j + 1] = array [j];
            j = j - 1; 
            array [j + 1] = chave;
        }
    
    }

    for (int i = 0; i < len; i++){
        std::cout << array[i] << std::endl;
    } 
    
    return 0;
}
