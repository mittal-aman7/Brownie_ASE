def test_check_upkeep(accounts, UpkeepContract):
    # Deploy the contract
    upkeep_contract = UpkeepContract.deploy({"from": accounts[0]})

    # Convert an integer to a 32 byte long hexadecimal representation
    tournamentIdBytes = '0x' + '00' * 31 + '01'


    # Call the function
    needs_upkeep, performData = upkeep_contract.checkUpkeep(tournamentIdBytes)

    # Add assertions (as required)
    assert needs_upkeep == True
    assert performData == tournamentIdBytes
