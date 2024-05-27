<strong>Design Approach:</strong>
For creating a block, I firstly create a list of all valid transactions by checking that transaction ID in vin is empty or not and also checking that value in prevout is greater than or equal to vout.
Then I define coinbase transaction with predefined reward and insert its transaction ID in the list of transaction ID in zeroth index.
Then I find the merkle root of transaction ID's in the list.
Then I define the block header and concatenate the fields of header to make a string and passed that string in mine block function which returns the nonce for the given header.
Then write the block header, coinbase and transaction ID's in output file.

<strong>Implementation Details:</strong>
Transaction validation and adding it to block:
If sum of value in prevout is greater than or equal to value in vout and transaction ID's in vin are non empty then the transaction is valid, then transaction ID's of the valid transaction are added to the block.

Merkle Root:
Merkle Root is calculated from the Transaction ID's.Firstly we take hash of first two transaction , then next two and so on , then secondly we take the hash of first two hashes from first level and carry on this process until only value remain.
In case of odd number I take the hash of concatenation of last transaction ID with itself.

Mining:
In this block we are using Proof-of-Work algorithm for block mining.
In mining firstly we take concatenation of block header fields then we define a variable nonce and take the hash of concatenated string with the nonce and check whether it is less than the target or not which is given in block header, and if it is not less than it then I increment the nonce and again repeat the process until we get the hash value than the target.Once we found out the nonce we add nonce value in the block header and block is mined and ready to add in blockchain.

<strong>Results and Performance:</strong>
In solution we firstly get the block header which contains all data related to the block in the fields.Then a coinbase transaction with its information and lastly the transaction ID's of the valid transactions.

Performance wise it is a very effecient and simple code.

<strong>Conclusion:</strong>
It is a basic and simple approach for mining process and in future we need to more optimise it.
