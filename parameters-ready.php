<?php
$filestring = "/home/aduffy/public_html/fs-parameters/" . $_POST['versionID'];
$filehandle = fopen($filestring, 'w') or die("Can't open file");
$allkeys = array_keys($_POST);
foreach($allkeys as $key)
{   
    fwrite($filehandle, $_POST[$key] . "\n");
}
fclose($filehandle);
?>

<p><span style="font-size: larger;">The parameters are ready to load.</span></p>
<p>To load the parameters:</p>
<p><ul><li>Move your avatar into the region where you would like to load them.</li><li>Paste the following text into the chat window:</li></ul></p>
<p><blockquote style="font-size: larger;"><b>/15 <?php echo $_POST['versionID'];?></b></blockquote></p>
<p>Once loaded, each plant will begin using the new parameters on its next cycle</p>
