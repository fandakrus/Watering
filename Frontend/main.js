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

function enableControls(label_array) {
    label_array.forEach(element => {
        element.classList.remove("disabled");
    })
}

function disableControls(btn_array, label_array) {
    btn_array.forEach(element => {
        element.checked = false;
    })
    label_array.forEach(element => {
        element.classList.add("disabled");
    })
}

// waits for change in the selection of checkboxes
document.addEventListener('DOMContentLoaded', function () {
    // get all elements with id btn-check from circle values -> return Nodelist and cann't be appended
    var btn_list = document.querySelectorAll('.btn-check');
    var btn_array = Array.from(btn_list);
    var label_list = document.querySelectorAll('#btnchecklabel');
    var label_array = Array.from(label_list);
    // convert Nodelist to array
    var elements = Array.from(btn_list);
    // add values for main conrol and water source
    var main_control = document.getElementById('MainSwitchCheck');
    elements.push(main_control);
    elements.push(document.getElementById('SourceWaterCheck'));

    main_control.addEventListener('change', function() {
        if (this.checked) {
            enableControls(label_array);
        } else {
            disableControls(btn_array, label_array);
        }
    })

    elements.forEach(element => {
        element.addEventListener('click', (e)=>{
            data = checkChecker(elements);
            sendData(data);
        });
     });
  });