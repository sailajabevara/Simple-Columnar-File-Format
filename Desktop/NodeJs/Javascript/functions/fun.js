//default parameter
function hello(){
    console.log("Welcome to javascript");
    
}
hello();
//function with return 
//in return function we must write the log to print the results
function hi(a){
  return a;
}

console.log(7);


function add(a, b) {
  return a + b; // returns the sum
}

let result = add(5, 10);
console.log(result); // 15

//Types of functions
//1. Named Function
function greet() {
  return "Hello!";
}
console.log(greet()); // Hello!

//2. Anonymous Function
//A function that does not have a name. It is usually assigned to a variable or used as a callback. Since it has no name, it cannot be called directly.
const Normal= function() {
  return "Hi there!";
};
console.log(greet()); // Hi there!

// 3. Function Expression
//  When you assign a function (can be named or anonymous) to a variable. The function can then be used by calling that variable.
const addition = function(a, b) {
  return a + b;
};
console.log(add(2, 3)); // 5



