#include <iostream>
using namespace std;

int list[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}; // lista ordenada

int bin(int num) {
    int center;
    int leng;

    leng = sizeof(list) / sizeof(list[0]);
    center = list[leng / 2]; 

    cout << "Procurando por: " << num << endl;

    while (true) {
        if (center == num) {
            cout << "Número encontrado: " << num << endl;
            return 0;
        } 
        else if (center > num) {
            center = center - 1;
        } 
        else {
            center = center + 1;
        }
    }
}

int main() {  
    bin(11);
    return 0;  
}
