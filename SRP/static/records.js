$(document).ready(function () {
  var sectorTable = $('#sector').DataTable({
    ajax: "/api/sector_records",
    serverSide: true,
    scrollX: true,
    scrollY: "55vh",
    bStateSave: true,
    fixedHeader: true,
    dom: "<'row'<'col-sm-12 col-md-4'l><'col-sm-12 col-md-4 tableSelect'><'col-sm-12 col-md-4'f>>" +
        "<'row'<'col-sm-12'tr>>" +
        "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
    columns: [
      {data: "flight_id", visible: false},
      {data: "ac"},
      {data: "callsign"},
      {data: "p1"},
      {data: "p2"},
      {data: "crew"},
      {data: "airport_dep"},
      {data: "airport_des"},
      {data: "srp"},
      {data: "date"},
      {data: "task", visible: false},
      {data: "task_desc", orderable: false, searchable: false, visible: false},
      {data: "fuel_bfwd", orderable: false, searchable: false, visible: false},
      {data: "depfuel_uplift_exp", orderable: false, searchable: false, visible: false},
      {data: "depfuel_uplift_act", orderable: false, searchable: false, visible: false},
      {data: "depfuel_total", orderable: false, searchable: false, visible: false},
      {data: "oil_uplift_l", orderable: false, searchable: false, visible: false},
      {data: "oil_uplift_r", orderable: false, searchable: false, visible: false},
      {data: "oil_dep_l", orderable: false, searchable: false, visible: false},
      {data: "oil_dep_r", orderable: false, searchable: false, visible: false},
      {data: "tks_preflight", orderable: false, searchable: false, visible: false},
      {data: "deantiice_type", orderable: false, searchable: false, visible: false},
      {data: "deantiice_temp", orderable: false, searchable: false, visible: false},
      {data: "deantiice_time", orderable: false, searchable: false, visible: false},
      {data: "deantiice_mix", orderable: false, searchable: false, visible: false},
      {data: "holdovertime", orderable: false, searchable: false, visible: false},
      {data: "takeoff_mass", orderable: false, searchable: false},
      {data: "preflight_signature", visible: false},
      {data: "preflight_callsign", visible: false},
      {data: "landfuel_main_l", orderable: false, searchable: false, visible: false},
      {data: "landfuel_main_r", orderable: false, searchable: false, visible: false},
      {data: "landfuel_aux_l", orderable: false, searchable: false, visible: false},
      {data: "landfuel_aux_r", orderable: false, searchable: false, visible: false},
      {data: "landfuel_other_l", orderable: false, searchable: false, visible: false},
      {data: "landfuel_other_r", orderable: false, searchable: false, visible: false},
      {data: "tks_postflight", orderable: false, searchable: false, visible: false},
      {data: "blockoff", orderable: false, searchable: false},
      {data: "takeoff", orderable: false, searchable: false},
      {data: "landing", orderable: false, searchable: false},
      {data: "blockon", orderable: false, searchable: false},
      {data: "landing_day", orderable: false, searchable: false, visible: false},
      {data: "landing_night", orderable: false, searchable: false, visible: false},
      {data: "postflight_signature", visible: false},
      {data: "postflight_callsign", visible: false}
      ],
  });

//  ---------------------  Variables  -----------------------------------------
  let totalSectorColumns = sectorTable.columns().nodes();
  let visibleSectorColumns = [];
  let allCB = document.getElementById("sector_data").getElementsByClassName("toggle-vis");
  $("#checkall").prop("indeterminate", true);

//  ----------  sync checkboxes with column visibility -----------
  sectorTable.columns().visible().each(function(value, index){
    if (value === true){
      visibleSectorColumns.push(index)
    }
  });

  for (let col = 0; col < totalSectorColumns.length; col++) {
    if (visibleSectorColumns.includes(parseInt(allCB[col].getAttribute("data-column")))) {
      $(allCB[col]).prop("checked", true);
    } else {
      $(allCB[col]).prop("checked", false);
    }
  }

//  ------------  set visibility to checked boxes  -------------------------
  $(".toggle-vis").change(function(){
    $("#checkall").prop("indeterminate", true);
    let colId = parseInt($(this).attr("data-column"))
    if ($(this).is(":checked")) {
      visibleSectorColumns.push(colId)
      console.log(visibleSectorColumns)
      sectorTable.columns(visibleSectorColumns).visible(true);
    } else {
      visibleSectorColumns.splice(visibleSectorColumns.indexOf(colId), 1)
      console.log(visibleSectorColumns)
      sectorTable.column(colId).visible(false);
      }
  });

  $('#checkall').on("click", function () {
    for (let col=0; col < totalSectorColumns.length; col+=1){
      if (!visibleSectorColumns.includes(col)) {
        visibleSectorColumns.push(col);
      };
    };
    if (($(this).is(":checked")) && (!$(this).is("indeterminate"))) {
      $('.toggle-vis').each(function () {this.checked = true;});
      console.log(visibleSectorColumns);
      sectorTable.columns(visibleSectorColumns).visible(true);
    } else if (!$(this).is(":checked")) {
      $('.toggle-vis').each(function () {this.checked = false; });
      sectorTable.columns(visibleSectorColumns).visible(false);
      visibleSectorColumns.splice(0);
      console.log(visibleSectorColumns);
    } else {
    }
  });

//  ----------- Aircraft data  -------------------------------------------------------------
  var aircraftTable = $('#aircraft').DataTable({
    ajax: "/api/aircraft_records",
    severSide: true,
    scrollX: true,
    scrollY: "55vh",
    bStateSave: true,
    fixedHeader: true,
    dom: "<'row'<'col-sm-12 col-md-4'l><'col-sm-12 col-md-4 tableSelect'><'col-sm-12 col-md-4'f>>" +
        "<'row'<'col-sm-12'tr>>" +
        "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
    columns: [
      {data: "aircraft_id", visible: false},
      {data: "registration"},
      {data: "defect", orderable: false},
      {data: "servicetime", orderable: false, searchable: false},
      {data: "hours", searchable: false},
      {data: "landing_day_total", searchable: false},
      {data: "landing_night_total", searchable: false},
      {data: "status"},
      {data: "fuel", orderable: false, searchable: false},
      {data: "oil_l", orderable: false, searchable: false},
      {data: "oil_r", orderable: false, searchable: false},
      {data: "tks", orderable: false, searchable: false},
      {data: "srp"},
      {data: "callsign"},
      {data: "location"},
      {data: "cycles", searchable: false}
      ],
    });
})

sectorTable = $("#sector").DataTable

function toggleTable () {
let selected_table = document.getElementById("table").value;
let sectors = (document.getElementById("sector_table"));
let aircraft = (document.getElementById("aircraft_table"));
let sector_data = (document.getElementById("sector_data"));
let aircraft_data = (document.getElementById("aircraft_data"));
  if (selected_table == "sector") {
    sectors.style.display = "block";
    aircraft.style.display = "none";
    aircraft_data.style.display = "none";
    sector_data.style.display = "block";
  } else if (selected_table == "aircraft") {
      aircraft.style.display = "block";
      sectors.style.display = "none";
      sector_data.style.display = "none";
      aircraft_data.style.display = "block";
    }
}

