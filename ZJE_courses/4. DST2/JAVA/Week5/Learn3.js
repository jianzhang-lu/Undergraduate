window.alert("Do you want to go on?");
var test3 = document.getElementsByClassName("hot");
test3[0].className = "cool";
test3[1].className = "cool";

var test4 = document.getElementsByClassName("hot")
test4.className = "cool";

var test5 = document.getElementsByTagName("ul")[0];
var newli = document.createElement("li");
var bold = document.createElement("b");
var newText = document.createTextNode("javascript test");
var newboldtext = document.createTextNode("my first ");
bold.appendChild(newboldtext);
newli.appendChild(bold);
newli.appendChild(newText);
test5.appendChild(newli);

function setup(){
    var textINput;
    textINput = document.getElementById("java");
    textINput.focus();
}
window.addEventListener("load", setup, false);

// var area = (function (width, height){
//     return width * height;
// }());
// var size = area(3,4);
// function Hotel (name, rooms, booked){
//     this.name = name;
//     this.rooms = rooms;
//     this.booked = booked;
//     this.checkAvailability = function (){
//         return this.rooms - this.booked;
//     }
// }
// var hotel;
// hotel = new Hotel('doggy', 34, 20);
// hotel.dog = true;
// hotel.toUpperCase()
//
// var test = 45;
// var test2 = document.querySelectorAll("li[id]")
//

