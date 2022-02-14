<?php

include("./connect.php");

$sql = "SELECT * FROM `個案管理師_基本資料`";
$result = mysqli_query($link,$sql);
$result_row_num= mysqli_num_rows($result); #query到的資料比數

for ($i=0; $i<$result_row_num; $i++)
{
    $row_data = mysqli_fetch_array($result);
    print($row_data['個管師_姓名']);
    print("<br>");
    print($row_data['個管師_line-user-id']);
    print("<br>");
    print($row_data['記錄時間']);

}
mysqli_free_result($result);

