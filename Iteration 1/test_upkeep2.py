def test_check_upkeep(accounts, UpkeepContract):
    # Deploy the contract
    upkeep_contract = UpkeepContract.deploy({"from": accounts[0]})

    # Define the input for the checkUpkeep function
    tournamentIdBytes = '0x01'

    # Call the function
    needs_upkeep, performData = upkeep_contract.checkUpkeep(tournamentIdBytes)

    # Add assertions (as required)
    assert needs_upkeep == True
    assert performData == tournamentIdBytes
