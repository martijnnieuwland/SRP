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
  document.getElementById("ac_hrs_new").value = ac_hrs;
  document.getElementById("ac_min_new").value = ac_min;
}


function getFuel() {
  let main_l = document.getElementById("main_l").value;
  let main_r = document.getElementById("main_r").value;
  let aux_l = document.getElementById("aux_l").value;
  let aux_r = document.getElementById("aux_r").value;
  let other_l = document.getElementById("other_l").value;
  let other_r = document.getElementById("other_r").value;
  $("#landing_fuel").text(+main_l + +main_r + +aux_l + +aux_r + +other_l + +other_r);
}


function getCurrentCycles() {
  let cycles_bfwd = document.getElementById("cycles_bfwd").textContent;
  let cycles = document.getElementById("cycles").value;
  document.getElementById("current_cycles").textContent = +cycles_bfwd + +cycles;
}


function getDayLandings() {
  let total_day_ldg = document.getElementById("total_day_ldg").textContent;
  let landings_day = document.getElementById("landings_day").value;
  document.getElementById("total_day_ldg").textContent = +total_day_ldg + +landings_day;
}


function getNightLandings() {
  let total_night_ldg = document.getElementById("total_night_ldg").textContent;
  let landings_night = document.getElementById("landings_night").value;
  document.getElementById("total_night_ldg").textContent = +total_night_ldg + +landings_night;
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

$("#defectCb").change (function() {
  $("#defect").attr("disabled", !this.checked);
});

$("#postflightConfirmCb").change (function() {
  $("#postflightConfirmBtn").attr("disabled", !this.checked)
});

$('#postflightSubmit').on('click', function(){
  let offhrs = $("#offhrs").val()
  let offmin = $("#offmin").val()
  let tohrs = $("#tohrs").val()
  let tomin = $("#tomin").val()
  let ldghrs = $("#ldghrs").val()
  let ldgmin = $("#ldgmin").val()
  let onhrs = $("#onhrs").val()
  let onmin = $("#onmin").val()
  let block_hrs = $("#block_hrs").text()
  let block_min = $("#block_min").text()
  let flt_hrs = $("#flt_hrs").text()
  let flt_min = $("#flt_min").text()
  let current_hrs = $("#ac_hrs").text()
  let current_min = $("#ac_min").text()
  let rem_hrs = $("#rem_hrs").text()
  let rem_min = $("#rem_min").text()
  landing_fuel = $("#landing_fuel").text()

  if ((offhrs != null) && (offmin != null)) {
    $("#off_time").text(offhrs + ":" + offmin).css("color", "initial");
  } else {
    $("#off_time").text("This data is required").css("color", "red");
    };
  if ((tohrs != null) && (tomin != null)) {
    $("#to_time").text(tohrs + ":" + tomin).css("color", "initial");
  } else {
    $("#to_time").text("This data is required").css("color", "red");
    };

  if ((ldghrs != null) && (ldgmin != null)) {
    $("#ldg_time").text(ldghrs + ":" + ldgmin).css("color", "initial");
  } else {
    $("#ldg_time").text("This data is required").css("color", "red");
    };
  if ((onhrs != null) && (onmin != null)) {
    $("#on_time").text(onhrs + ":" + onmin).css("color", "initial");
  } else {
    $("#on_time").text("This data is required").css("color", "red");
    };

  if ((block_hrs != "--") && (block_min != "--" )) {
    $("#block_time").text(block_hrs + ":" + block_min).css("color", "initial");
  } else {
    $("#block_time").text("This data is required").css("color", "red");
    };
  if ((flt_hrs != "--") && (flt_min != "--")) {
    $("#flight_time").text(flt_hrs + ":" + flt_min).css("color", "initial");
  } else {
    $("#flight_time").text("This data is required").css("color", "red");
    };

  $("#time_current").text(current_hrs + ":" + current_min);
  $("#time_remaining").text(rem_hrs + ":" + rem_min);
  console.log(landing_fuel)
  if (landing_fuel != "") {
    $("#landing_fuel_total").text(landing_fuel).css("color", "initial");
  } else {
    $("#landing_fuel_total").text("This data is required").css("color", "red");
  }

  $("#landing_fuel_req").val(parseInt(landing_fuel));

  if (($("#defect")).val() != "") {
      $("#defect_data").text($("#defect").val());
  } else {
    $("#defect_data").text("None");
  }
});