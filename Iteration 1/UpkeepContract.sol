// SPDX-License-Identifier: MIT
pragma solidity ^0.8.15;

contract UpkeepContract {

    function checkUpkeep(bytes calldata tournamentIdBytes) external view returns (bool upkeepNeeded, bytes memory performData) {
        uint tournamentId = abi.decode(tournamentIdBytes, (uint));
        // ... your logic here ...
        return (true, tournamentIdBytes); // example return
    }
}
