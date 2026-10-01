$t = [Windows.Networking.NetworkOperators.NetworkOperatorTetheringManager,Windows.Networking.NetworkOperators,ContentType=WindowsRuntime]
$p = [Windows.Networking.Connectivity.NetworkInformation,Windows.Networking.Connectivity,ContentType=WindowsRuntime]::GetInternetConnectionProfile()
$m = $t::CreateFromConnectionProfile($p)
$cfg = $m.GetCurrentAccessPointConfiguration()
$cfg.Ssid = "cloudcutterflash"
$cfg.Passphrase = "abcdabcd"
$null = $m.ConfigureAccessPointAsync($cfg)
$null = $m.StartTetheringAsync()
