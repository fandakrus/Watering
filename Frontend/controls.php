<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-+0n0xVW2eSR5OomGNYDnhzAbDsOXxcvSN1TPprVMTNDbiYZCxYbOOl7+AMvyTG2x" crossorigin="anonymous">
    <link href="./style.css" rel="stylesheet">
    <title>Voda</title>
</head>

<body>
    <?php
    function OpenDbCon() {
        $servername = getenv('DB_SERVER');
        $username = getenv('DB_USER');
        $password = getenv('DB_PASSWD');
        $dbname = getenv('DB_NAME');
        // Create connection 
        $conn = new mysqli($servername, $username, $password, $dbname);

        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: ". $conn->connect_error);
        }

        return $conn;
    }

    //open object with database
    $conn = OpenDbCon();

    $prevaules = $conn->query("SELECT id, circle1, circle2, circle3, circle4, main_control, water_source FROM controls ORDER BY id DESC LIMIT 1");
    $dbvalue = $prevaules->fetch_row();
    ?>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav">
                    <a class="nav-link" href="./index.php">Domov</a>
                    <a class="nav-link active" aria-current="page" href="./controls.php">Ovládání</a>
                    <a class="nav-link" href="#">Historie</a>
                </div>
            </div>
        </div>
    </nav>
    <div class="position-relative my-btn-container">
        <div class="btn-group position-absolut top-0 start-50 translate-middle-x" role="group" aria-label="Basic checkbox toggle button group">
            <input type="checkbox" class="btn-check" id="btncheck1" autocomplete="off" <?php echo ($dbvalue[1]==1 ? 'checked' : '');?>>
            <label class="btn btn-outline-primary" for="btncheck1">Okruh 1</label>
            
            <input type="checkbox" class="btn-check" id="btncheck2" autocomplete="off" <?php echo ($dbvalue[2]==1 ? 'checked' : '');?>>
            <label class="btn btn-outline-primary" for="btncheck2">Okruh 2</label>
            
            <input type="checkbox" class="btn-check" id="btncheck3" autocomplete="off" <?php echo ($dbvalue[3]==1 ? 'checked' : '');?>>
            <label class="btn btn-outline-primary" for="btncheck3">Okruh 3</label>
            
            <input type="checkbox" class="btn-check" id="btncheck4" autocomplete="off" <?php echo ($dbvalue[4]==1 ? 'checked' : '');?>>
            <label class="btn btn-outline-primary" for="btncheck4">Okruh 4</label>
        </div>
    </div> 
    <div id="my-outer">
        <div id="my-inner">
            <div class="form-check form-switch">
                <input class="form-check-input" type="checkbox" role="switch" id="MainSwitchCheck" <?php echo ($dbvalue[5]==1 ? 'checked' : '');?>>
                <label class="form-check-label" for="MainSwitchCheck">Hlavní vypínač</label>
            </div>
            <div class="form-check form-switch">
                <input class="form-check-input" type="checkbox" role="switch" id="SourceWaterCheck" <?php echo ($dbvalue[6]==1 ? 'checked' : '');?>>
                <label class="form-check-label" for="SourceWaterCheck">Napajení z vodovodu</label>
            </div>
        </div>
    </div>
    <script src="./main.js" type="text/javascript"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
</body>

</html>