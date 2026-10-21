# PhilexcelHUB - individual Windows SMB mappings. Preview by default.
[CmdletBinding()]
param(
 [Parameter(Mandatory)][string]$NasHost,
 [ValidateSet('Executive','AdminHR','Marketing','AdminMarketing','FinancePurchasing','Engineering')]
 [string[]]$Departments=@(),
 [switch]$IncludeShared,
 [switch]$Apply,
 [switch]$PromptForCredentials
)
$ErrorActionPreference='Stop'
$shares=@{
 Executive=@('X','Executive')
 AdminHR=@('H','AdminHR')
 Marketing=@('M','Marketing')
 AdminMarketing=@('R','AdminMarketing')
 FinancePurchasing=@('F','FinancePurchasing')
 Engineering=@('E','Engineering')
 CompanyShared=@('Z','CompanyShared')
}
$selected=@($Departments)
if($IncludeShared){$selected+= 'CompanyShared'}
if($selected.Count -eq 0){throw 'Choose at least one approved department or IncludeShared'}
$plans=@(foreach($name in ($selected|Select-Object -Unique)){
 $info=$shares[$name]
 [pscustomobject]@{Name=$name;Letter=($info[0]+':');Remote=('\\'+$NasHost+'\'+$info[1])}
})
$plans|Format-Table -AutoSize
if(-not $Apply){Write-Host 'PREVIEW ONLY. Verify department approvals and legacy Z: mapping before applying.';return}
$reachable=Test-NetConnection -ComputerName $NasHost -Port 445 -InformationLevel Quiet -WarningAction SilentlyContinue
if(-not $reachable){throw 'NAS SMB port 445 unavailable'}
foreach($p in $plans){
 $letter=$p.Letter.Substring(0,1)
 if(Get-PSDrive -Name $letter -ErrorAction SilentlyContinue){throw "Drive $letter already exists. No changes made."}
}
$cred=$null
if($PromptForCredentials){$cred=Get-Credential -Message 'Personal NAS credentials only'}
foreach($p in $plans){
 $params=@{Name=$p.Letter.Substring(0,1);PSProvider='FileSystem';Root=$p.Remote;Persist=$true;Scope='Global'}
 if($cred){$params.Credential=$cred}
 New-PSDrive @params | Out-Null
 Write-Host "Mapped $($p.Letter) to $($p.Remote)"
}
