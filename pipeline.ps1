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
    exit
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

if (Get-Command "pytest" -errorAction SilentlyContinue){
    PrintSuccess "Pytest found"
} else {
    PrintError "Error: Pytest is missing"
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
Write-Host "Checking client config"
if ([System.IO.File]::Exists("client/config/account.json")){
    PrintSuccess "Client account config found"
} else {
    PrintError "ERROR: Client account config not found"
}
Write-Host "Checking verifier config"
if ([System.IO.File]::Exists("verifier/config/account.json")){
    PrintSuccess "Verifier account config found"
} else {
    PrintError "ERROR: Verifier account config not found"
}
Write-Host "Checking CA key"
if ([System.IO.File]::Exists("certificate_authority/config/key.pem")){
    PrintSuccess "CA private key found"
} else {
    PrintErrror "ERROR: CA private key not found"
}
Write-Host "Checking verifier keys"
if ([System.IO.File]::Exists("verifier/config/verifier_key/key.pem")){
    PrintSuccess "Verifier private key found"
} else {
    PrintError "ERROR: Verifier private key not found"
}
if ([System.IO.File]::Exists("certificate_authority/config/verifier_key/key.pem")){
    PrintSuccess "Verifier key found in CA"
} else {
    PrintError "ERROR: Verifier key not found in CA"
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
    Write-Host $test_result
    Set-Location ..

    if ($test_result.Contains("failing")){
        PrintError "ERROR: truffle tests failed"
    } else {
        PrintSuccess "Truffle tests passed"
    }

    Write-Host "Running client smoke tests"
    Set-Location client
    $test_result = pytest | Out-String
    Write-Host $test_result
    Set-Location ..

    if ($test_result.Contains("fail")){
        PrintError "ERROR: client smoke tests failed"
    } else {
        PrintSuccess "Client smoke tests passed"
    }

    Write-Host "Running verifier smoke tests"
    Set-Location verifier
    $test_result = pytest | Out-String
    Write-Host $test_result
    Set-Location ..

    if ($test_result.Contains("fail")){
        PrintError "ERROR: verifier smoke tests failed"
    } else {
        PrintSuccess "Verifier smoke tests passed"
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

    # Setting up abi to certificate_authority
    Write-Host "Setting up CA"
    New-Item -ItemType Directory -Force -Path certificate_authority/config/contracts/ | out-null
    Copy-Item smart_contract/build/contracts/PrivCA.json certificate_authority/config/contracts/PrivCA.json | out-null
    PrintSuccess "CA setup done"

    # Setting up abi to client
    Write-Host "Setting up client"
    New-Item -ItemType Directory -Force -Path client/config/contracts/ | out-null
    Copy-Item smart_contract/build/contracts/PrivCA.json client/config/contracts/PrivCA.json | out-null
    PrintSuccess "Client setup done"

    # Setting up abi to verifier
    Write-Host "Setting up verifier"
    New-Item -ItemType Directory -Force -Path verifier/config/contracts/ | out-null
    Copy-Item smart_contract/build/contracts/PrivCA.json verifier/config/contracts/PrivCA.json | out-null
    PrintSuccess "Verifier setup done"

    # deploying services
    Write-Host "Building docker images..."
    docker compose build
    PrintSuccess "Docker images built"
    Write-Host "Running docker containers..."
    docker compose up -d
    PrintSuccess "Deployments done"
}
EndSegment