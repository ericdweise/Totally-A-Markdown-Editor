if(!empty($_POST['data'])){
    $data = $_POST['data'];
    $fname = $_POST['file'];

    $file = fopen($fname, 'w');
    fwrite($file, $data);
    fclose($file);
}
