const TZ_OFFSET_IN_HOURS = new Date().getTimezoneOffset() / 60;

let dateInput = document.getElementById('date');
let time = document.getElementById('time');
let message = document.getElementById('message');

function httpGet(theUrl, date) {
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", theUrl, false); // false for synchronous request
    xmlHttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xmlHttp.send('date=' + date);
    return xmlHttp.responseText;
};

function returnTimesInBetween(start, end) {
    let timesInBetween = [];
    let startH = parseInt(start.split(":")[0]);
    const startM = parseInt(start.split(":")[1]);
    const endH = parseInt(end.split(":")[0]);
    const endM = parseInt(end.split(":")[1]);
    if (startM == 30) {
        timesInBetween.push(startH < 10 ? "0" + startH + ":30" : startH + ":30");
        startH++;
    }
    for (let i = startH; i < endH; i++) {
        timesInBetween.push(i < 10 ? "0" + i + ":00" : i + ":00");
        timesInBetween.push(i < 10 ? "0" + i + ":30" : i + ":30");
    }
    if (endM == 30) {
        timesInBetween.push(endH < 10 ? "0" + endH + ":00" : endH + ":00");
    }

    return timesInBetween;
}

let getScheduleTimes = (event) => {
    message.innerHTML = "";
    time.innerHTML = "";

    if (!dateInput.value) {
        dateInput.value = new Date().toISOString().split("T")[0];
    }
    
    const schedules = httpGet('/schedule', dateInput.value);
    let scheduleRes = JSON.parse(schedules);

    /** Display error if the selected date is not available.
     * The reason for the setTimeout is to remove the message after some seconds, otherwise it'd remain there
     */
    if(!scheduleRes[0]){
       message.innerHTML = `<div class="alert alert-danger" role="alert">Not Available on the selected date. Choose Another Date</div>`;
        setTimeout(() => {
            message.removeChild(message.childNodes[0]);
        }, 4000);
    }

    for (let i = 0; i < scheduleRes.length; i++) {
        const {
            start_datetime,
            stop_datetime,
            picked_times
        } = scheduleRes[i];

        if (start_datetime !== 'False') {
            /*
            Create list of already booked times then remove them
            from the dropdown so that the user doesn't select one
            of them.
            */
            const startTime = start_datetime.split(' ')[1];
            const stopTime = stop_datetime.split(' ')[1];
            let alreadyBookedTimes = [];

            for (let j = 0; j < picked_times.length; j++) {
                const event_start = picked_times[j];
                let bookedTime = event_start.split(' ')[1].slice(0, 5);
                alreadyBookedTimes.push(bookedTime);
            }
            
            const times = returnTimesInBetween(startTime, stopTime);

            times.forEach((val) => {
                if (alreadyBookedTimes.includes(val)) {
                    return;
                }

                // Times from the back end are in UTC. Subtracting the timezone offset displays the time in the proper time zone.
                time.innerHTML += `<option value=${val}>${String(Number(val.split(":")[0]) - TZ_OFFSET_IN_HOURS) + ":" + val.split(":")[1]}</option>`
            });

        }
    }
};

dateInput.addEventListener('change', getScheduleTimes);
getScheduleTimes(null); // Get the available times for booking "today" when the page loads.