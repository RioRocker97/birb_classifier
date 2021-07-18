cls

$file_name = 'CAQ', 'Cockatiel', 'Indian_Ring', 'Wanker_bird', 'Lovebird', 'Brz_wing','Grn_amazon'
$file_htm = '5.htm', '6.htm', '7.htm', '8.htm', '9.htm', '10.htm', '11.htm'
Write-Host "Downloading file and shit..."
for($i=0;$i -lt $file_name.length;$i++){
    Write-Host "...Downloading "$file_name[$i]"..."
    $temp = "./first_gather/"+$file_htm[$i]
    py extract.py "--bird" $file_name[$i] "--htm" $temp 
}
