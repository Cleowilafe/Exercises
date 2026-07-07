#include <iostream>
#include <string>
using namespace std;

int main() {
    
    string ano = "2018";

    int ftd = 
    int ltd = ((ano [2] - '0')*10 + (ano[3]) - '0'); // last two digits

     if (ltd % 2 != 0){
        ltd += 11; 
    }
    if (ltd % 2 == 0) {
        ltd *= 0.5; 
    }
    if (ltd % 2 != 0){
        ltd += 11; 
    }

    ltd %= 7;

    
  
    
    cout << ltd<< endl;
    return 0;
}
