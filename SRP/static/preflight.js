let upliftAct = document.getElementById("uplift_act");
let fuelBfwd = document.getElementById("fuel_bfwd");
let depFuel = document.getElementById("departure_fuel");


function updateUpliftExp() {
  document.getElementById("uplift_exp").value = upliftAct.value;
}


function updateDepFuel() {
  document.getElementById("departure_fuel").value = +upliftAct.value + +fuelBfwd.value;
}


function updateUpliftAct() {
  document.getElementById("uplift_act").value = +depFuel.value - +fuelBfwd.value;
}
