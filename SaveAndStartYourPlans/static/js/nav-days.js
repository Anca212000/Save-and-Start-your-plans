var lastDay = new Date(dt.getYear(), dt.getMonth() + 1, 0);
var nbMaxDays = lastDay.getDate();
console.log(nbMaxDays);

daysMonth = new Array(nbMaxDays);
for (var i = 0; i < nbMaxDays; i++) {
  daysMonth[i] = i + 1;
}
console.log(daysMonth);

var checkIndex = false;
var indexCurrent = null;
var posCenter = null;

if (checkIndex == false) {
  indexCurrent = daysMonth.indexOf(dayCur);
  posCenter = indexCurrent;
  checkIndex = true;
}

function changeDayNext() {
  if (posCenter != indexCurrent) {
    indexCurrent = posCenter;
  }
  document.getElementById("dayPrev").innerHTML = daysMonth[indexCurrent];
  indexCurrent++;
  posCenter = indexCurrent;
  document.getElementById("dayCurrent").innerHTML = daysMonth[posCenter];
  var x = document.getElementById("dayPrev");
  var y = document.getElementById("butDayBack");
  if (x.style.visibility === "hidden" && y.style.visibility === "hidden") {
    document.getElementById("dayPrev").style.visibility = "visible";
    document.getElementById("butDayBack").style.visibility = "visible";
  }
  if (posCenter === nbMaxDays - 1) {
    document.getElementById("dayNext").style.visibility = "hidden";
    document.getElementById("butDayNext").style.visibility = "hidden";
  } else if (posCenter < nbMaxDays) {
    indexCurrent++;
    document.getElementById("dayNext").innerHTML = daysMonth[indexCurrent];
  }
}

function changeDayPrevious() {
  if (posCenter != indexCurrent) {
    indexCurrent = posCenter;
  }
  document.getElementById("dayNext").innerHTML = daysMonth[indexCurrent];
  indexCurrent--;
  posCenter = indexCurrent;
  document.getElementById("dayCurrent").innerHTML = daysMonth[posCenter];
  var x = document.getElementById("dayNext");
  var y = document.getElementById("butDayNext");
  if (x.style.visibility === "hidden" && y.style.visibility === "hidden") {
    document.getElementById("dayNext").style.visibility = "visible";
    document.getElementById("butDayNext").style.visibility = "visible";
  }
  if (posCenter === 0) {
    document.getElementById("dayPrev").style.visibility = "hidden";
    document.getElementById("butDayBack").style.visibility = "hidden";
  } else if (posCenter > 0) {
    indexCurrent--;
    document.getElementById("dayPrev").innerHTML = daysMonth[indexCurrent];
  }
}
