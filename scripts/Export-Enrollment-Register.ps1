# PowerShell 7. Requires an authorised Microsoft Graph connection with User.Read.All.
# This exports verified records only. It does not create users or change memberships.
$ErrorActionPreference = 'Stop'
$TenantId = 'c6e4f48c-aba5-42e6-a95b-b54205d7490f'
if ((Get-MgContext).TenantId -ne $TenantId) { throw 'Connect Microsoft Graph to the Philexcel tenant first.' }
$Roster = @'
Ian|Ian|IanPackham@PhilexcelBusinessPark.onmicrosoft.com|Executive
Tess|Tess|mcunanan@philexcel.com|Administration-HR
Aliza|Aliza|acalaguas@philexcel.com|Administration-HR
Seatiel|Seatiel|slumbang@philexcel.com|Administration-HR
Camille|Camille|cnaguit@philexcel.com|Marketing
Chloe|Chloe|ccastillo@philexcel.com|Administration-Marketing
Clark|Clark|cgutierrez@philexcel.com|Administration-Marketing
Jhojie|Jhojie|jsoriano@philexcel.com|Finance-Purchasing
Kevin|Kevin|kgutierrez@philexcel.com|Finance-Purchasing
Anne|Ann|agozum@philexcel.com|Finance-Purchasing
Rose|Rose|rmacaraeg@philexcel.com|Finance-Purchasing
Nello|Nello|npineda@philexcel.com|Finance-Purchasing
Rommel|Rommel|rpanganiban@philexcel.com|Engineering
Rowell|Rowell|rtalens@philexcel.com|Engineering
Mavel|Mavel|mbarcia@philexcel.com|Engineering
Evann|Evain|lasencio@philexcel.com|Engineering
James|James|jpureza@philexcel.com|Engineering
Cris|Cris|myumul@philexcel.com|Engineering
Hub Administrator|philexcelhub|hub@philexcel.com|Executive
'@ | ConvertFrom-Csv -Delimiter '|' -Header Name,Nas,Login,Department
$Records = @(foreach ($Row in $Roster) {
    $User = Get-MgUser -UserId $Row.Login -Property Id,DisplayName,UserPrincipalName,Mail,AccountEnabled,UserType -ErrorAction Stop
    if (-not $User.AccountEnabled -or $User.UserType -ne 'Member' -or $User.UserPrincipalName -ine $Row.Login) {
        throw "STOP: directory verification failed for $($Row.Name). No export written."
    }
    [ordered]@{
        object_id=$User.Id;display_name=$Row.Name;nas_username=$Row.Nas
        user_principal_name=$User.UserPrincipalName;mail=$User.Mail;departments=@($Row.Department)
        nas_access_level=$(if ($Row.Nas -in @('Ian','philexcelhub')) {'executive'} else {'department'})
        enabled=$true
    }
})
if (@($Records.object_id | Sort-Object -Unique).Count -ne 19) { throw 'Duplicate or missing identities. No export written.' }
$OutputPath = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'Philexcel-Enrollment-Register.json'
$Records | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $OutputPath -Encoding utf8NoBOM
Write-Host "PASS: 18 staff and Hub verified and exported to $OutputPath"
Write-Host 'Transfer privately to the hosting account. Never put this file in public_html or Git.'
Write-Host 'No Microsoft, NAS, SharePoint or portal administrator privileges were granted by this export.'
