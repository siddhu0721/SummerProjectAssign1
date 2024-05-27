import os
import json
import hashlib
import time

# function for validating transaction
def validateTx(tx):
    prevoutValue=0
    voutValue=0
    isTxid=1

    for i in tx['vin']:
        prevoutValue=prevoutValue+i['prevout']['value']   #Sum of value in prevout

    for j in tx['vout']:
        voutValue=voutValue+j['value']    #Sum of value in vout

    for k in tx['vin']:
        isTxid=isTxid and k['txid']    #Checking if txid is empty or not in vin

    return prevoutValue>voutValue and isTxid

# Reading and Validating Transactions from mempool and adding the valid ones transaction ID in transactionIds list 
def validTxns(mempoolFolder):
    transactionIds=[]
    for filename in os.listdir(mempoolFolder):
        txid=filename[:-5]
        with open(os.path.join(mempoolFolder,filename),'r') as file:
            data=json.load(file)
            if isinstance(data,list):  #If file have more than one transaction ID's in vin
                for tx in data:
                    if validateTx(tx):
                        continue
                transactionIds.append(txid)
            elif isinstance(data,dict): #If file have only one transaction ID's in vin
                if validateTx(data):
                    transactionIds.append(txid)
    return transactionIds

#Recursive function for calculating merkle root
def calculateMerkleRoot(txids):
    if len(txids)==0:
        return ''
    elif len(txids)==1:
        return txids[0]
    newTxids=[]
    for i in range(0,len(txids)-1,2):            #Looping through whole list and finding hash of pairs of transaction IDs
        newTxids.append(hashlib.sha256((txids[i]+txids[i+1]).encode()).hexdigest())
    
    #If number of Transaction ID's in list is odd
    if len(txids)%2 ==1:                                                               
        newTxids.append(hashlib.sha256((txids[-1]+txids[-1]).encode()).hexdigest())
    return calculateMerkleRoot(newTxids)

# function for mining the block
def mine(header):
    nonce=0
    target="0000ffff00000000000000000000000000000000000000000000000000000000"
    while True:
        blockHeader=header+str(nonce)                                #Concatenating input header string and nonce
        blockHash=hashlib.sha256(blockHeader.encode()).hexdigest()
        if blockHash<target:     
            return nonce,blockHash
        nonce=nonce+1

#creating block
def createBlock(mempoolFolder):

    #Finding valid transaction and store their Transaction ID in transactionIds list
    transactionIds = validTxns(mempoolFolder)
    
    #Defining Coinbase Transaction with predefined values
    coinbaseTxn={
                    "txid": "4a7b8a1f3f6b3a9b8a1f3f6b3a9b8a1f3f6b3a7b8a1f3f6b3a9b8a1f3f6b3a9b",
                    "vin": [
                    {
                        "coinbase": "04ffff001d0104455468652054696d65732030332f4a616e2f32303233204368616e63656c6c6f72206f6e20626974636f696e2062756c6c",
                        "sequence": 4294967295
                    }
                    ],
                    "vout": [
                    {
                        "value": 5000000000,
                        "scriptPubKey": "4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac"
                    }
                    ]
                }
    
    #Inserting Coinbase Transaction ID in the starting of Transaction ID list
    transactionIds.insert(0,coinbaseTxn["txid"])

    #Calculating Merkle Root and assign the value to merkleRoot variable 
    merkleRoot=calculateMerkleRoot(transactionIds)
    
    #Defining block header 
    header={
            "version": 1,
            "block_hash":"",
            "previous_block_hash": "0000000000000000000000000000000000000000000000000000000000000000",
            "merkle_root": merkleRoot,
            "timestamp": int(time.time()),
            "difficulty_target": "0000ffff00000000000000000000000000000000000000000000000000000000",
            "nonce": 0
        }
    
    #Concatenating Block Header fields
    headerConcatStr=str(header["version"])+header["previous_block_hash"]+header["merkle_root"]+str(header["timestamp"])+header["difficulty_target"]

    #adding nonce and blockHash value in block header
    nonce,blockHash=mine(headerConcatStr)
    header["nonce"]=nonce
    header["block_hash"]=blockHash

    #Creating output.txt and writing Block Header,coinbase and transaction ID's in it 
    with open('output.txt','w') as f:
        f.write(f"Block Header:\n{json.dumps(header,indent=2)}\n\n")
        f.write(f"Serialized Coinbase Transaction:\n{json.dumps(coinbaseTxn, indent=2)}\n\n")
        f.write("Transaction IDs:\n")
        for txid in transactionIds:
            f.write(f"{txid}\n")

# calling createBlock function
createBlock('mempool')