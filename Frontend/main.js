function sendData(data) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "localhost/reqreceiver.php", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
    data
}));
}

function checkChecker(elements) {
    data = {
        circle1: elements[0].checked,
        circle2: elements[1].checked,
        circle3: elements[2].checked,
        circle4: elements[3].checked,
    };
    console.log(data);
}

document.addEventListener('DOMContentLoaded', function () {
    const elements = document.querySelectorAll('.btn-check');

  
    elements.forEach(element => {
        element.addEventListener('click', (e)=>{
            checkChecker(elements);
        });
     });
  });