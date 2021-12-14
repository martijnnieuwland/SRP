// ----------------------------- Preflight ------------------------------------

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


// ----------------------------- Postflight ------------------------------------

function setOff() {
  let off_date = new Date();
  let hrs = off_date.getUTCHours();
  let min = off_date.getUTCMinutes();
  let min5 = Math.round(min/5)*5;
  if (min5 == 60) {
    min5 = 0
    hrs = hrs + 1
  }
  let min05 = min5.toString().padStart(2, 0);
  let hrs00 = hrs.toString().padStart(2, 0);
  document.getElementById("offhrs").value = hrs00
  document.getElementById("offmin").value = min05
}


function setTO() {
  let to_date = new Date();
  let hrs = to_date.getUTCHours();
  let min = to_date.getUTCMinutes();
  let min5 = Math.round(min/5)*5;
  if (min5 == 60) {
    min5 = 0
    hrs = hrs + 1
  }
  let min05 = min5.toString().padStart(2, 0);
  let hrs00 = hrs.toString().padStart(2, 0);
  document.getElementById("tohrs").value = hrs00
  document.getElementById("tomin").value = min05
}


function setOn() {
  let on_date = new Date();
  let hrs = on_date.getUTCHours();
  let min = on_date.getUTCMinutes();
  let min5 = Math.round(min/5)*5;
  if (min5 == 60) {
    min5 = 0
    hrs = hrs + 1
  }
  let min05 = min5.toString().padStart(2, 0);
  let hrs00 = hrs.toString().padStart(2, 0);
  document.getElementById("onhrs").value = hrs00
  document.getElementById("onmin").value = min05
}


function setLdg() {
  let ldg_date = new Date();
  let hrs = ldg_date.getUTCHours();
  let min = ldg_date.getUTCMinutes();
  let min5 = Math.round(min/5)*5;
  if (min5 == 60) {
    min5 = 0
    hrs = hrs + 1
  }
  let min05 = min5.toString().padStart(2, 0);
  let hrs00 = hrs.toString().padStart(2, 0);
  document.getElementById("ldghrs").value = hrs00
  document.getElementById("ldgmin").value = min05
}


function getBlockTime() {
  let block_hrs = document.getElementById("onhrs").value - document.getElementById("offhrs").value;
  let block_min = document.getElementById("onmin").value - document.getElementById("offmin").value;
  let on_d1 = document.getElementById("on_d1").checked;
  let to_d1 = document.getElementById("to_d1").checked;
  let ldg_d1 = document.getElementById("ldg_d1").checked;
  let blocktime = document.getElementsByClassName("blocktime");
  if (to_d1 == true || ldg_d1 == true || on_d1 == true) {
    block_hrs = block_hrs + 24;
  }
  if (block_min < 0 && block_hrs > 0) {
    block_min = block_min + 60;
    block_hrs = block_hrs - 1;
  }
  if (block_min > 0 && block_hrs < 0) {
    block_min = block_min - 60;
    block_hrs = block_hrs + 1;
  }
  document.getElementById("block_hrs").textContent = block_hrs;
  document.getElementById("block_min").textContent = block_min.toString().padStart(2, 0);
  if (block_hrs < 0 || block_min < 0) {
    if (block_hrs == 0) {
      document.getElementById("block_hrs").textContent = "-" + block_hrs;
    }
    document.getElementById("block_min").textContent = block_min.toString().replace("-", "").padStart(2, 0);
    for (let e = 0; e < blocktime.length; e++) {
      blocktime[e].style.color = "red";
    }
  } else {
      for (let e = 0; e < blocktime.length; e++) {
        blocktime[e].style.color = "black";
      }
    }
}


function getFlightTime() {
  let flt_hrs = document.getElementById("ldghrs").value - document.getElementById("tohrs").value;
  let flt_min = document.getElementById("ldgmin").value - document.getElementById("tomin").value;
  let to_d1 = document.getElementById("to_d1").checked;
  let ldg_d1 = document.getElementById("ldg_d1").checked;
  let flighttime = document.getElementsByClassName("flighttime");
  if (flt_hrs < 0 && to_d1 == true || ldg_d1 == true) {
    flt_hrs = flt_hrs + 24;
  }
  if (flt_min < 0 && flt_hrs > 0) {
    flt_min = flt_min + 60;
    flt_hrs = flt_hrs - 1;
  }
  if (flt_min > 0 && flt_hrs < 0) {
    flt_min = flt_min - 60;
    flt_hrs = flt_hrs + 1;
  }
  document.getElementById("flt_hrs").textContent = flt_hrs;
  document.getElementById("flt_min").textContent = flt_min.toString().padStart(2, 0);
  // ----------------------------- Style ------------------------------------
  if (flt_hrs < 0 || flt_min < 0) {
    if (flt_hrs == 0) {
      document.getElementById("flt_hrs").textContent = "-" + flt_hrs;
    }
    document.getElementById("flt_min").textContent = flt_min.toString().replace("-", "").padStart(2, 0);
    for (let e = 0; e < flighttime.length; e++) {
      flighttime[e].style.color = "red";
    }
  } else {
      for (let e = 0; e < flighttime.length; e++) {
        flighttime[e].style.color = "black";
      }
    }
}


function setAcTime () {
  let flt_hrs = document.getElementById("flt_hrs").innerHTML;
  let flt_min = document.getElementById("flt_min").innerHTML;
  let ac_hrs_bfwd_hrs = document.getElementById("ac_hrs_bfwd_hrs").innerHTML
  let ac_hrs_bfwd_min = document.getElementById("ac_hrs_bfwd_min").innerHTML
  if (flt_hrs >= 0) {
    ac_hrs = +ac_hrs_bfwd_hrs + +flt_hrs;
    ac_min = +ac_hrs_bfwd_min + +flt_min;
    if (ac_min >= 60) {
      ac_min = ac_min - 60;
      ac_hrs = ac_hrs + 1
    }
    if (ac_min < 0 && ac_hrs > 0) {
      ac_min = ac_min + 60;
      ac_hrs = hrs - 1;
    }
  }
  if (flt_hrs.startsWith("-")) {
    ac_hrs = ac_hrs_bfwd_hrs
    ac_min = ac_hrs_bfwd_min.toString().padStart(2, 0);
  } else {
      ac_hrs = ac_hrs.toString()
      ac_min = ac_min.toString().padStart(2, 0);
    }
  document.getElementById("ac_hrs").textContent = ac_hrs;
  document.getElementById("ac_min").textContent = ac_min;
}


function getFuel() {
  let main_l = document.getElementById("main_l").value;
  let main_r = document.getElementById("main_r").value;
  let aux_l = document.getElementById("aux_l").value;
  let aux_r = document.getElementById("aux_r").value;
  let other_l = document.getElementById("other_l").value;
  let other_r = document.getElementById("other_r").value;
  document.getElementById("landing_fuel").value = +main_l + +main_r + +aux_l + +aux_r + +other_l + +other_r;
}


function getCurrentCycles() {
  let cycles_bfwd = document.getElementById("cycles_bfwd").textContent;
  let cycles = document.getElementById("cycles").value;
  document.getElementById("current_cycles").textContent = +cycles_bfwd + +cycles;
}


let total_day_ldg = document.getElementById("total_day_ldg").textContent;
function getDayLandings() {
  let landings_day = document.getElementById("landings_day").value;
  document.getElementById("total_day_ldg").textContent = +total_day_ldg + +landings_day;
}


let total_night_ldg = document.getElementById("total_night_ldg").textContent;
function getNightLandings() {
  let landings_night = document.getElementById("landings_night").value;
  document.getElementById("total_night_ldg").textContent = +total_night_ldg + +landings_night;
}

//const ac_time_rem = document.getElementById("ac_hrs");
//ac_time_rem.addEventListener("load", test)

function test() {
  console.log("testing")
}


function getTimeRemaining () {
  let service_hrs = document.getElementById("service_hrs").innerHTML;
  let service_min = document.getElementById("service_min").innerHTML;
  let ac_hrs = document.getElementById("ac_hrs").innerHTML;
  let ac_min = document.getElementById("ac_min").innerHTML;
  let rem_hrs = +service_hrs - +ac_hrs;
  let rem_min = +service_min - +ac_min;
  let rem_time = document.getElementsByClassName("rem_time")
  if (rem_hrs >= 0 && rem_min < 0) {
    rem_min = rem_min + 60;
    rem_hrs = rem_hrs -1;
  }
  if (rem_hrs < 0 && rem_min > 0) {
    rem_min = rem_min - 60;
    rem_hrs = rem_hrs + 1;
  }
  // ----------------------------- Style ------------------------------------
  if (rem_min < 0) {
    document.getElementById("rem_min").textContent = rem_min.toString().replace("-", "").padStart(2, 0);
    if (rem_hrs == 0) {
      document.getElementById("rem_hrs").textContent = "-" + rem_hrs.toString();
    } else if (rem_hrs < 0) {
      document.getElementById("rem_hrs").textContent = rem_hrs;
    }
  if (rem_hrs <= 0) {
    for (let e = 0; e < rem_time.length; e++) {
      rem_time[e].style.color = "red"}
  }
  } else {
      document.getElementById("rem_min").textContent = rem_min.toString().padStart(2, 0);
      document.getElementById("rem_hrs").textContent = rem_hrs;
      document.getElementById("rem_min").textContent = rem_min.toString().padStart(2, 0);
      document.getElementById("rem_hrs").textContent = rem_hrs;
      for (let e = 0; e < rem_time.length; e++) {
        rem_time[e].style.color = "black"}
  }
}
