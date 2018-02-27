import hashlib, json, sys
import random

def hashMe(msg=""):
    if type(msg)!=str:
        msg = json.dumps(msg,sort_keys=True)
        
    if sys.version_info.major == 2:
        return unicode(hashlib.sha256(msg).hexdigest(),'utf-8')
    else:
        return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()

random.seed(0)

def makeEntry(maxValue=10):
    
    ID = random.randint(1,maxValue)
    Quantity   = 100 * random.randint(1,maxValue)
    Price = 0.1 * random.randint(1, maxValue)
    sup = str("Supplier")
    date = str( "12/01/2018")
    
    return {u'Date': date, u'Supplier':sup , u'Product_ID':ID,u'Quantity':Quantity, u'Price': Price}

entryBuffer = [makeEntry() for i in range(5)]


def isValidEntry(entry):
    return True


name = str("bolatoglou AE")
state = {u'Company': name}  # Define the initial state
genesisBlock = state
genesisBlockContents = {u'blockNumber':0,u'parentHash':None,u'entriesCount':1,u'entry':genesisBlock}
genesisHash = hashMe( genesisBlockContents )
genesisBlock = {u'hash':genesisHash,u'contents':genesisBlockContents}
genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)

chain = [genesisBlock]
     
def makeBlock(entries,chain):
    parentBlock = chain[-1]
    parentHash  = parentBlock[u'hash']
    blockNumber = parentBlock[u'contents'][u'blockNumber'] + 1
    entryCount    = len(entries)
    blockContents = {u'blockNumber':blockNumber,u'parentHash':parentHash,
                     u'entryCount':len(entries),'entries':entries}
    blockHash = hashMe( blockContents )
    block = {u'hash':blockHash,u'contents':blockContents}
    
    return block

blockSizeLimit = 5  #number of transactions per block- 


def checkBlockHash(block):

    expectedHash = hashMe( block['contents'] )
    if block['hash']!=expectedHash:
        print('Hash does not match contents of block %s'%
                        block['contents']['blockNumber'])
        return False
        
    return True

def checkChain(chain):

    
    checkBlockHash(chain[0])
    parent = chain[0]
    for block in chain[1:]:
        state = checkBlockValidity(block,parent)
        parent = block
        
    return state

def checkBlockValidity(block,parent):
    
    parentNumber = parent['contents']['blockNumber']
    parentHash   = parent['hash']
    blockNumber  = block['contents']['blockNumber']
    
    checkBlockHash(block) # Check hash integrity; raises error if inaccurate

    state = True
    if blockNumber!=(parentNumber+1):
        print("Wrong Block Number")
        state = False

    if block['contents']['parentHash'] != parentHash:
        state = False

    return state


print("Blockchain on Node A is currently %s blocks long"%len(chain))


def writechain(chain):
    f = open("blockchain.txt", "w");
    for line in chain:
        s = str(line);
        f.write(s)
        f.write("\n")
    f.close()
writechain(chain)

def appendchain(block):
    chain.append(block)
    if checkChain(chain):
        fap = open("blockchain.txt", "a")
        blockstr = str(chain[-1])
        fap.write(blockstr)
        fap.write("\n")
        print("Blockchain on Node A is currently %s blocks long"%len(chain))
        fap.close()
    else:
        chain.pop()
        print("Enter block again")
        

entry1 = [makeEntry()]
new = makeBlock(entry1,chain)
appendchain(new)
