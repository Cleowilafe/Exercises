nums = [2,7,11,15];
target = 18;
n = nums.length;

// Use one pointer at the beginning and the other at the end of the array.
var L = 0;
var R = n - 1;

// If L >= R, it means all possible pairs have already been checked.
while (L < R) {

    var sum = nums[L] + nums[R];

    // Move the pointers depending on the current sum.
    if (sum > target) {
        R -= 1;
    } else if (sum < target) {
        L += 1;
    } else if (sum === target) {
        console.log(L, R);
        break;
    }
}
