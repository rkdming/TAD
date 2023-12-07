<?php

header('Content-Type: application/json; charset=UTF-8');


$servername = "localhost";
$username = "root";
$password = "root";
$dbname = "pbl4";

$conn = new mysqli($servername, $username, $password, $dbname);

// check DB connection
if ($conn->connect_error) {
    echo json_encode(['error' => "Connection failed: " . $conn->connect_error]);
    exit();
}

// get category and URL from  POST request
$categories = json_decode($_POST['categories']);
$vid = $_POST['videoID']; 



// SQL query
$sql = "SELECT * FROM videos WHERE vid = '".$vid."' AND category IN ('" . implode("', '", $categories) . "')";

$result = $conn->query($sql);
//$output = array(); //this will transform php to json


if ($result) {
    $output = array();
    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) {
            array_push($output,
		array('title' => $row['title'],
			'category' => $row['category']));
        }
        echo json_encode($output);
    } else {
        // no result
        echo json_encode(['message' => 'No results found']);
    }
} else {
    // query error
    echo json_encode(['error' => 'Query failed']);
}

$conn->close();
?>
