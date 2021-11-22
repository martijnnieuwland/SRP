function updateValue(e) {
  log.textContent = e.target.value;
}
function myFunction() {
  alert("Hello! I am an alert box!");
}


const input = document.querySelector('input');
const log = document.getElementById('values');
input.addEventListener('input', updateValue);
function updateValue(e) {
  log.textContent = e.target.value;
}




document.getElementById("Input1").addEventListener("input", Function1);
document.getElementById("Input2").addEventListener("input", Function2);

function Function1() {
  alert("The value of the input field was changed.");
}






const uplift_exp = document.getElementById('uplift_exp').value

alert(uplift_exp)
