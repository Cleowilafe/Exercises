#include <iostream>
int main() {
    int size = 4;
    int m[size] = {40, 30, 20, 10};

     for(int i = 1; i < size; i++){
        int j = i - 1;
        int x = m[i];
        while (j >= 0 && x < m [j]){
            m[j+1] = m[j];
            j--;
        }
       m[j+1] = x; 
     }
    for(int i = 0; i < size; i++) {        
        std::cout << m[i] << std::endl;
    }
  
    return 0;
}
