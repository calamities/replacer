import yaml

def yaml_loader(filepath):
    with open(filepath, 'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

def yaml_dump(filepath, data):
    with open(filepath, 'w') as file_descriptor:
        yaml.dump(data, file_descriptor)

def readfile(filepath):
    f = open(filepath, 'r')
    fileContents = f.read()
    f.close()
    return fileContents

def writefile(filepath,contents):
    f = open(filepath, 'w')
    fileContents = f.write(contents)
    f.close()

def replacer(x,variables):
    replacex = x
    for var in variables:
        if replacex.find('{{'+var['var']+'}}') != -1:
            if 'type' not in var:
                replacex = replacex.replace('{{'+var['var']+'}}', var['value'])
    return replacex

def findloop(x,params):
    if x[1].find('{{#each') != -1:
        mod = x[1]
        eachbegin = mod.index("{{#each")
        eachend = mod.index("{{/each}}")+9
        block = mod[eachbegin:]
        block = block[block.index("}}")+3:]
        block = block[:block.index("{{/each}}")]
        loopvalue = mod[eachbegin+8:]
        loopvalue = loopvalue[:loopvalue.index("}}")]
        variables = params.get('variables')
        looplist = []
        for var in variables:
            if var['var'] == loopvalue and var['type'] == '#each':
                looplist = var['value']
        blockreplace = ''
        for i in looplist:
            blockreplace += replacer(block,i['variables'])
        x[1]=mod[:eachbegin] + blockreplace + mod[eachend+1:]
        findloop(x,params)

if __name__ == '__main__':
    params = yaml_loader('params.yml')
    fileloc = params.get('fileToReplace')
    origfile = readfile(fileloc)
    fileMod = [origfile,origfile]
    if fileMod[1].find('{{#each') != -1:
        findloop(fileMod,params)
    #print(fileMod)
    variables = params.get('variables')
    for var in variables:
        if fileMod[1].find('{{'+var['var']+'}}') != -1:
            if 'type' not in var:
                fileMod[1] = fileMod[1].replace('{{'+var['var']+'}}', var['value'])
    writefile(params.get('newFileLocation'),fileMod[1])
