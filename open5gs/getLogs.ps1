$pods = kubectl get pods

foreach($p in $pods)
{
    $pod = $p.Split(" ")[0]
    $app = $p.Split("-")[1]
    
    if( -not ($app -eq "mongodb" -or $app -eq "my5grantester" -or $app -eq "test" -or $app -eq "ueransim" -or $app -eq "webui"))
    {
        Write-Host "$pod" + "[$app]"
        kubectl cp ${pod}:/var/log/open5gs/$app.log  .\logs\$app.log
    }
}