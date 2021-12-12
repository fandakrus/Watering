// send checkboxes to php server on given url
function sendData(data) {
    var xhr = new XMLHttpRequest();
    // uses http get reqeuest and sends data threw given url
    const url = "reqreceiver.php?changed=true&circle1=" + data["circle1"] + "&circle2=" + data["circle2"] + "&circle3=" + data["circle3"] + "&circle4=" + data["circle4"];
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    console.log('sending');
    /*
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
    };
    console.log(data);
    return data;
}

// waits for change in the selection of checkboxes
document.addEventListener('DOMContentLoaded', function () {
    const elements = document.querySelectorAll('.btn-check');

  
    elements.forEach(element => {
        element.addEventListener('click', (e)=>{
            data = checkChecker(elements);
            sendData(data);
        });
     });
  });