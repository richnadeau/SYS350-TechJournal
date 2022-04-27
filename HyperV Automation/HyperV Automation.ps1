Clear-Host
Write-Host "Welcome to HyperV!"
Function menu()
{
Write-Host ""
Write-Host "1) Summary of VMs"
Write-Host "2) Detailed Info of VM"
Write-Host "3) Power On a VM"
Write-Host "4) Power Off a VM"
Write-Host "5) Create a Checkpoint for VM"
Write-Host "6) Restore to a Checkpoint for VM"
Write-Host "7) Change VMs Network Adapter"
Write-Host "8) Remove a VM From Disk"
Write-Host "0) Exit"
}

do
 {
    menu
    $select = Read-Host "Select an Option"
    Write-Host ""
    switch ($select)
    {
    '1'{
    $VMs = Get-VM -Name *
    Write-Host "   VM   |   State   |   IP Address"
    ForEach ($VM in $VMs){
        if($VM.VMName -inotmatch "base"){
            $Adapters=($VM | Get-VMNetworkAdapter)
            ForEach($Adapter in $Adapters){
                Write-Host($VM.VMName,' | ',$VM.State, '  |  ', $Adapter.IPAddresses[0])
    }
    }
    }
    } '2' {
    $numba = 0
    $VMs = Get-VM -Name *
    ForEach ($VM in $VMs)
    {
        $numba = $numba + 1
        Write-Host "$numba. " $VM.Name
    }
    $selectVM = Read-Host "Select a VM"
    $selectVM = $selectVM - 1
    $thevm = $VMs[$selectVM]
    $memingib = $thevm.MemoryStartup/1073741824
    Write-Host "   Virtual Machine   |   CPUs   |   Memory   |   Path to Files   |   Uptime   |   Creation Date    |"
    Write-Host $thevm.VMName, "   |   ", $thevm.ProcessorCount, "   |   ", $memingib, "GB   |   ", $thevm.Path, "   |   ",  $thevm.Uptime,  "   |   ", $thevm.Creationtime,  "   |"
    } '3' {
    $numba = 0
    $VMs = Get-VM -Name *
    ForEach ($VM in $VMs)
    {
        $numba = $numba + 1
        Write-Host "$numba. " $VM.Name
    }
    $selectVM = Read-Host "Select a VM to Power On"
    $selectVM = $selectVM - 1
    $thevm = $VMs[$selectVM]
    Start-VM -Name $thevm.VMName
    } '4' {
    $numba = 0
    $VMs = Get-VM -Name *
    ForEach ($VM in $VMs)
    {
        $numba = $numba + 1
        Write-Host "$numba. " $VM.Name
    }
    $selectVM = Read-Host "Select a VM to Power Off"
    $selectVM = $selectVM - 1
    $thevm = $VMs[$selectVM]
    Stop-VM -Name $thevm.VMName
    } '5' {
    $numba = 0
    $VMs = Get-VM -Name *
    ForEach ($VM in $VMs)
    {
        $numba = $numba + 1
        Write-Host "$numba. " $VM.Name
    }
    $selectVM = Read-Host "Select a VM to Take a Checkpoint of"
    $selectVM = $selectVM - 1
    $thevm = $VMs[$selectVM]
    $snapshotname = Read-Host "What would you like the checkpoint to be named?"
    Get-VM -Name $thevm.VMName | Checkpoint-VM -SnapshotName $snapshotname
    } '6' {
    $numba = 0
    $VMs = Get-VM -Name *
    ForEach ($VM in $VMs)
    {
        $numba = $numba + 1
        Write-Host "$numba. " $VM.Name
    }
    $selectVM = Read-Host "Select a VM to Restore to its latest Checkpoint"
    $selectVM = $selectVM - 1
    $thevm = $VMs[$selectVM]
    Restore-VMSnapshot -VMName $thevm.VMName -Name $thevm.ParentCheckpointName
    } '7' {
    $numba = 0
    $VMs = Get-VM -Name *
    ForEach ($VM in $VMs)
    {
        $numba = $numba + 1
        Write-Host "$numba. " $VM.Name
    }
    $selectVM = Read-Host "Select a VM to Change its Network Adapter"
    $selectVM = $selectVM - 1
    $thevm = $VMs[$selectVM]
    $Switches = Get-VMSwitch -Name *
    $numba = 0
    ForEach ($Switch in $Switches)
    {
        $numba = $numba + 1
        Write-Host "$numba. " $Switch.Name
    }
    $selectSwitch = Read-Host "Select a Switch to put your Selected Network Adapter on"
    $selectSwitch = $selectSwitch - 1
    $theswitch = $Switches[$selectSwitch]
    Connect-VMNetworkAdapter -VMName $thevm.VMName -SwitchName $theswitch.Name
    } '8' {
    $numba = 0
    $VMs = Get-VM -Name *
    ForEach ($VM in $VMs)
    {
        $numba = $numba + 1
        Write-Host "$numba. " $VM.Name
    }
    $selectVM = Read-Host "Select a VM to Delete From Disk"
    $selectVM = $selectVM - 1
    $thevm = $VMs[$selectVM]
    Stop-VM -Name $thevm.VMName
    $harddisk = Get-VM -Name $thevm.Name | Select-Object -ExpandProperty HardDrives
    $harddiskpath = $harddisk.Path
    Remove-VM -Name $thevm.VMName
    Remove-Item -Path $harddiskpath
    }
    }
 }
 until ($select -eq '0')

Write-Host "Exiting HyperV Program"
Write-Host ""
Write-Host "Goodbye"
Write-Host ""
