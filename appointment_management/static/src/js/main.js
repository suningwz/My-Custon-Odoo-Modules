let dateInput = document.getElementById('date');
let time = document.getElementById('time');
let message = document.getElementById('message');
const httpGet = (theUrl, date) => {

    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", theUrl, false ); // false for synchronous request
    xmlHttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xmlHttp.send('date='+date);
    return xmlHttp.responseText;
};


let getGenTime = (timeString) => {
  let H = +timeString.substr(0, 2);
  let h = (H % 12) || 12;
  let ampm = H < 12 ? " AM" : " PM";
  return timeString = h + timeString.substr(2, 3) + ampm;
};
function returnTimesInBetween(start, end) {
    let timesInBetween = [];
    let startH = parseInt(start.split(":")[0]);
    const startM = parseInt(start.split(":")[1]);
    const endH = parseInt(end.split(":")[0]);
    const endM = parseInt(end.split(":")[1]);
    if (startM == 30) {
          startH++;
      }
      for (let i = startH; i < endH; i++) {
        timesInBetween.push(i < 10 ? "0" + i + ":00" : i + ":00");
        timesInBetween.push(i < 10 ? "0" + i + ":30" : i + ":30");
      }
      timesInBetween.push(endH + ":00");
      if (endM == 30) {
          timesInBetween.push(endH + ":30")
      }
      return timesInBetween.map(getGenTime);
}



dateInput.addEventListener('change', (event) => {
    const schedules  = httpGet('/schedule', event.target.value);
    console.log(schedules);
    const {
        start_date,
        stop_date,
        start_datetime,
        stop_datetime,
        duration,
        info
    } = JSON.parse(schedules);
    if(start_datetime !== 'False'){
        const DT =  start_datetime.split(' ');
        const [startDate, startTime] = DT;

        const DT2 = stop_datetime.split(' ');
        const [stopDate, stopTime] = DT2;
        const times = returnTimesInBetween(startTime, stopTime);

        times.forEach((val) => {
            time.innerHTML += `<option value=${val}>${val}</option>`
        });

    }else if(start_date !== 'False'){
        const times = returnTimesInBetween('09:00:00', '19:00:00');

        times.forEach((val) => {
            time.innerHTML += `<option value=${val}>${val}</option>`
        });
    }else {
        message.innerHTML = `<div class="alert alert-danger" role="alert">Not Available on the selected date. Choose Another Date</div>`;
        setTimeout(() => {
            message.removeChild(message.childNodes[0]);
        }, 3000);

    }
});