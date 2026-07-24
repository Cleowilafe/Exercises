//for a while i will use this O(n²), i will improve it later 
list = [2,4,3,2,1];
target = 7;

for (var j = 0; j < list.length; j++){
    comp = target - list [j];
   
    if (list.includes(comp)){
        console.log(list[j], comp)
        break
    }  
}
