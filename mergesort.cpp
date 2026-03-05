#include <iostream>
using namespace std;

// Função que mescla dois subarrays ordenados
void merge(int array[], int left, int mid, int right) {
    // Tamanhos dos subarrays esquerdo e direito
    int len_nl = mid - left + 1;   // tamanho da esquerda
    int len_nr = right - mid;      // tamanho da direita

    int nl[len_nl];  // subarray da esquerda
    int nr[len_nr];  // subarray da direita

    // Copiar os elementos do subarray esquerdo
    for (int i = 0; i < len_nl; i++) {
        nl[i] = array[left + i];
    }

    // Copiar os elementos do subarray direito
    for (int i = 0; i < len_nr; i++) {
        nr[i] = array[mid + 1 + i];
    }

    // Juntar os subarrays ordenados de volta no array original
    int i = 0, j = 0, k = left;  // Índices para os subarrays e array original

    // Comparar os elementos e copiar o menor para o array original
    while (i < len_nl && j < len_nr) {
        if (nl[i] <= nr[j]) {
            array[k] = nl[i];
            i++;
        } else {
            array[k] = nr[j];
            j++;
        }
        k++;
    }

    // Copiar os elementos restantes do subarray esquerdo
    while (i < len_nl) {
        array[k] = nl[i];
        i++;
        k++;
    }

    // Copiar os elementos restantes do subarray direito
    while (j < len_nr) {
        array[k] = nr[j];
        j++;
        k++;
    }

    // Imprimir os subarrays depois da mesclagem
    cout << "Subarray ordenado: ";
    for (int i = left; i <= right; i++) {
        cout << array[i] << " ";
    }
    cout << endl;
}

// Função recursiva de Merge Sort
void mergeSort(int array[], int left, int right) {
    if (left < right) {

        int mid = left + (right - left) / 2;  // Calcula o meio

        // Recursão para dividir o array
        mergeSort(array, left, mid);
        mergeSort(array, mid + 1, right);

        // Chama a função merge para juntar os subarrays ordenados
        merge(array, left, mid, right);
    }
}

int main() {
    int array[5] = {5, 4, 3, 2, 1};
    int len = sizeof(array) / sizeof(array[0]);

    // Chama o Merge Sort no array inteiro
    mergeSort(array, 0, len - 1);

    // Imprimir o array final ordenado
    cout << "Array final ordenado: ";
    for (int i = 0; i < len; i++) {
        cout << array[i] << " ";
    }
    cout << endl;

    return 0;
}
