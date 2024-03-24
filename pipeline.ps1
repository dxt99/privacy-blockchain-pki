param(
    [Parameter(Mandatory = $false)]
    [switch]${no-deploy} = $false,
    [Parameter(Mandatory = $false)]
    [switch]${no-test} = $false
)

function PrintSuccess {
    param (
        [Parameter(Mandatory = $true)]
        [string]$message
    )

    Write-Host -ForegroundColor Green $message
}

function PrintError {
    param (
        [Parameter(Mandatory = $true)]
        [string]$message
    )

    Write-Host -ForegroundColor Red $message
}

function PrintSegment {
    param (
        [Parameter(Mandatory = $true)]
        [string]$segment
    )
    Write-Host "--------------------------"
    Write-Host -ForegroundColor Yellow $segment
}

function EndSegment {
    Write-Host "--------------------------"
}

# Check Dependencies
PrintSegment "Dependecy Check"
if (Get-Command "truffle" -errorAction SilentlyContinue){
    PrintSuccess "Truffle found"
} else {
    PrintError "Error: Truffle is missing"
}

if (Get-Command "docker" -errorAction SilentlyContinue){
    PrintSuccess "Docker found"
} else {
    PrintError "Error: Docker is missing"
}
EndSegment

# Tests
PrintSegment "Tests"
if (${no-test}){
    Write-Host "Skipping tests ..."
} else {
    Write-Host "Running truffle tests"
    Set-Location smart_contract
    $test_result = truffle test | Out-String
    Set-Location ..

    if ($test_result.Contains("failing")){
        PrintError "ERROR: truffle tests failed"
        exit
    } else {
        PrintSuccess "Truffle tests passed"
    }
}
EndSegment

# Deployments
PrintSegment "Deployments"
if (${no-deploy}){
    Write-Host "Skipping deployment ..."
} else {
    # deploying smart contract
    Write-Host "Compiling and deploying contracts..."
    Set-Location smart_contract
    truffle deploy | out-null
    Set-Location ..
    PrintSuccess "Contract deployments done"

    # setting up abi to smart_contract
    Write-Host "Setting up CA"
    New-Item -ItemType Directory -Force -Path certificate_authority/smart_contract/ | out-null
    Copy-Item smart_contract/build/contracts/PrivCA.json certificate_authority/config/contracts/PrivCA.json | out-null
    PrintSuccess "CA Setup done"
}
EndSegment

# Check manual configs
PrintSegment "Configs"
Write-Host "Checking CA config"
if ([System.IO.File]::Exists("certificate_authority/config/account.json")){
    PrintSuccess "CA account config exists"
} else {
    PrintError "ERROR: CA account config missing"
}
EndSegment