cls

$file_name = 'hya-m', 'scr-m', 'bg-m', 'hahn-m', 'gr-bud', 'blu-bud','male-ec','fem-ec','rb-lori','blu-parotl'
$file_htm = '1.htm', '2.htm', '3.htm', '4.htm', '5.htm', '6.htm', '7.htm', '8.htm', '9.htm', '10.htm'
Write-Host "Downloading file and shit..."
for($i=0;$i -lt $file_name.length;$i++){
    Write-Host "...Downloading "$file_name[$i]"..."
    $temp = "./image_data/"+$file_htm[$i]
    py extract.py "--bird" $file_name[$i] "--htm" $temp 
}
