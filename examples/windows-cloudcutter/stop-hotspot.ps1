$t = [Windows.Networking.NetworkOperators.NetworkOperatorTetheringManager,Windows.Networking.NetworkOperators,ContentType=WindowsRuntime]
$p = [Windows.Networking.Connectivity.NetworkInformation,Windows.Networking.Connectivity,ContentType=WindowsRuntime]::GetInternetConnectionProfile()
$m = $t::CreateFromConnectionProfile($p)
$null = $m.StopTetheringAsync()
Start-Sleep -Seconds 5
$m = $t::CreateFromConnectionProfile($p)
Write-Output ("STATE=" + $m.TetheringOperationalState)
