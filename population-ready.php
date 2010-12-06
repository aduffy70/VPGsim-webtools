<?php
function ValidateNumeric($value, $minimum, $maximum)
{
    //Verify that a value is an integer in the range minimum to maximum (inclusive)
    if (is_numeric($value))
    {
        if (($value >= $minimum) && ($value <= $maximum))
        {
            return TRUE;
        }
        else
        {
            return FALSE;
        }
    }
    else
    {
        return FALSE;
    }
}

$errorMessage = '';
$h1L5 = $_POST['hap1Locus5'];
$h1L4 = $_POST['hap1Locus4'];
$h1L3 = $_POST['hap1Locus3'];
$h1L2 = $_POST['hap1Locus2'];
$h1L1 = $_POST['hap1Locus1'];
$h2L5 = $_POST['hap2Locus5'];
$h2L4 = $_POST['hap2Locus4'];
$h2L3 = $_POST['hap2Locus3'];
$h2L2 = $_POST['hap2Locus2'];
$h2L1 = $_POST['hap2Locus1'];
$xMin = trim($_POST['xMin']);
$xMax = trim($_POST['xMax']);
$yMin = trim($_POST['yMin']);
$yMax = trim($_POST['yMax']);
$qty = trim($_POST['qty']);
if ($_POST['retries'] == 'on')
{
    $retries = '1';
}
else
{
    $retries = '0';
}
if ($xMin == '')
{
    $errorMessage = 'Error: No X Min value!<br>';
}
else if (!ValidateNumeric($xMin, 0, 256))
{
    $errorMessage = 'Error: X Min out of range<br>';
}
else if ($xMax == '')
{
    $errorMessage = 'Error: No X Max value!<br>';
}
else if (!ValidateNumeric($xMax, 0, 256))
{
    $errorMessage = 'Error: X Max out of range!<br>';
}
else if ($xMin >= $xMax)
{
    $errorMessage = 'Error: X Min larger than X Max!<br>';
}
else if ($yMin == '')
{
    $errorMessage = 'Error: No Y Min value!<br>';
}
else if (!ValidateNumeric($yMin, 0, 256))
{
    $errorMessage = 'Error: Y Min out of range!<br>';
}
else if ($yMax == '')
{
    $errorMessage = 'Error: No Y Max value!<br>';
}
else if (!ValidateNumeric($yMax, 0, 256))
{
    $errorMessage = 'Error: Y Max out of range!<br>';
}
else if ($yMin >= $yMax)
{
    $errorMessage = 'Error: Y Min larger than Y Max!<br>';
}

else if ($qty == '')
{
    $errorMessage = 'Error: No Qty value!<br>';
}
else if (!ValidateNumeric($qty, 1, 500))
{
    $errorMessage = 'Error: Qty out of range!<br>';
}
else if (ceil($qty) != $qty)
{
    $errorMessage = 'Error: Qty is not an integer!';
}
else if ((($h2L5 == 'b') || ($h2L4 == 'b') || ($h2L3 == 'b') || ($h2L2 == 'b') || ($h2L1 == 'b')) && (($h2L5 != 'b') || ($h2L4 != 'b') || ($h2L3 != 'b') || ($h2L2 != 'b') || ($h2L1 != 'b')))
{
    $errorMessage = 'Error: Allele not specified for some Loci of Haplotype 2!';
}
if ($errorMessage != '')
{
    die($errorMessage);
}
$lifeStage = 'sporophytes';
if ($h2L5 == 'b')
{
    $lifeStage = 'spores';
}
$genotype = $h1L5 . $h1L4 . $h1L3 . $h1L2 . $h1L1;
if ($h2L5 != 'b')
{
    $genotype = $genotype . $h2L5 . $h2L4 . $h2L3 . $h2L2 . $h2L1;
}
$commandString = '/4 ' . $genotype . ',' . $xMin . ',' . $xMax . ',' . $yMin . ',' . $yMax . ',' . $qty . ',' . $retries;    
?>
<p><span style="font-size: larger;">The <?php echo $lifeStage; ?> are ready to load.</span></p>
<p>To generate the population:</p>
<p><ul><li>Move your avatar into the region where you would like to load them.</li><li>Paste the following text into the chat window:</li></ul></p>
<p><blockquote style="font-size: larger;"><b><?php echo $commandString;?></b></blockquote></p>
