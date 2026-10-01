$connected = $false
for ($i = 0; $i -lt 15 -and -not $connected; $i++) {
  netsh.exe wlan disconnect interface=Wi-Fi | Out-Null
  netsh.exe wlan connect name=A-7083 interface=Wi-Fi | Out-Null
  Start-Sleep -Seconds 2
  $state = netsh.exe wlan show interfaces
  $connected = [bool]($state | Where-Object {$_ -match 'SSID\s*:\s*A-7083'})
}
if (-not $connected) { throw 'Could not associate with A-7083' }

& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'start-hotspot-async.ps1')
& python (Join-Path $PSScriptRoot 'send_cloudcutter_udp.py') wifi --ip 192.168.175.1
Write-Output 'FINAL_HANDOFF_SENT'
