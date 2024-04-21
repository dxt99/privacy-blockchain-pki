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

# Check and install Dependencies
PrintSegment "Dependecy Check"
if (Get-Command "py" -errorAction SilentlyContinue){
    PrintSuccess "Python found"
    Write-Host "Installing python dependencies"
    py -m pip install -r "certificate_authority/requirements.txt" | out-null
    Write-Host "Finished installing python dependencies"
} else {
    PrintError "Error: Python is missing"
}

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

# Check manual configs
PrintSegment "Configs"
Write-Host "Checking truffle config"
if ([System.IO.File]::Exists("smart_contract/truffle-config.js")){
    PrintSuccess "Truffle config found"
} else {
    PrintError "ERROR: Truffle config not found"
}
Write-Host "Checking CA config"
if ([System.IO.File]::Exists("certificate_authority/config/account.json")){
    PrintSuccess "CA account config found"
} else {
    PrintError "ERROR: CA account config not found"
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
    # resetting CA database
    Write-Host "Resetting certificate authority..."
    if ([System.IO.File]::Exists("certificate_authority/db/certificate_authority.db")){
        PrintSuccess "Deleting existing database ..."
        Remove-Item "certificate_authority/db/certificate_authority.db"
    } else {
        PrintSuccess "No reset needed"
    }
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

    # deploying services
    Write-Host "Building docker images..."
    docker compose build
    PrintSuccess "Docker images built"
    Write-Host "Deploying other services..."
    docker compose up -d
    PrintSuccess "Service deployments done"
}
EndSegment