// send checkboxes to php server on given url
function sendData(data) {
    var xhr = new XMLHttpRequest();
    // uses http get reqeuest and sends data threw given url
    const url = "reqreceiver.php?changed=true&circle1=" + data["circle1"] + "&circle2=" + data["circle2"] + "&circle3=" + data["circle3"] + "&circle4=" + data["circle4"] + "&main-control=" + data["main_control"] + "&water-source=" + data["water_source"];
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    console.log('sending');
    /*
    function for displayin php response dont delete !!!!!!!
    xhr.onreadystatechange = function() {//Call a function when the state changes.
        if(xhr.readyState == 4 && xhr.status == 200) {
            alert(xhr.responseText);
        }
    }*/
    xhr.send(data);
}


// make a json from checkboxes
function checkChecker(elements) {
    data = {
        circle1: elements[0].checked,
        circle2: elements[1].checked,
        circle3: elements[2].checked,
        circle4: elements[3].checked,
        main_control: elements[4].checked,
        water_source: elements[5].checked,
    };
    console.log(data);
    return data;
}

// waits for change in the selection of checkboxes
document.addEventListener('DOMContentLoaded', function () {
    // get all elements with id btn-check from circle values -> return Nodelist and cann't be appended
    var btn_list = document.querySelectorAll('.btn-check');
    // convert Nodelist to array
    var elements = Array.from(btn_list);
    // add values for main conrol and water source
    elements.push(document.getElementById('MainSwitchCheck'));
    elements.push(document.getElementById('SourceWaterCheck'));

    elements.forEach(element => {
        element.addEventListener('click', (e)=>{
            data = checkChecker(elements);
            sendData(data);
        });
     });
  });