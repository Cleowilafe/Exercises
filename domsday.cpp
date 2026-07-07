#include <iostream>
using namespace std;

void X_n (int b, int t, int m, int v, int n){
    int xn;   // resp
    
    xn = (( n * v) + b) % m;      
    cout << xn << endl;
    
    if (t != 0) {
        X_n (b, t-1, m, v, xn);
    }
}

int main() {
    int b = 3;  // incremento
    int t = 10; // times
    int m = 100; // mod
    int v = 3; // multiplicador 
    int n = 20; // seed

 X_n( b, t, m, v, n);
    return 0;
}

