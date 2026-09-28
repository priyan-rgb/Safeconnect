console.log("SafeConnect Loaded");

const button = document.querySelector("button");

button.addEventListener("click", () => {

alert("Welcome to SafeConnect!");

});
function sendMessage(){

let input=document.getElementById("userInput");

let chat=document.getElementById("chatBox");


if(input.value.trim()=="")
return;


let user=document.createElement("div");

user.className="user-message";

user.innerHTML=input.value;


chat.appendChild(user);



setTimeout(()=>{


let bot=document.createElement("div");


bot.className="bot-message";


bot.innerHTML=
"Thank you for sharing. SafeConnect AI is analyzing your request and providing assistance.";


chat.appendChild(bot);


chat.scrollTop=chat.scrollHeight;


},800);



input.value="";


}