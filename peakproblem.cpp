#include <iostream>
using namespace std;


int main () {
  int len,mid,right,left;
  int arr [10] =  {3,5,2,6,3,2,7,10,6,11};
  len = sizeof(arr)/sizeof(arr[0]);
  left = 0;
  right = len - 1;

  while (right >= left){
    mid = (left + right) / 2;

   if ((mid == 0 || arr [mid] >= arr[mid+1]) && (mid == len - 1 || arr[mid] >= arr[mid - 1])){
     cout << "peak found: " << arr [mid] << endl;
     break;
   } else if ( mid == 0 || arr[mid] > arr [mid - 1]){
     left = mid + 1;
   } else {right = mid - 1;}

  }

  return 0;
}
