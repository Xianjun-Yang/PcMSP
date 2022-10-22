#!/usr/bin/env python
# coding: utf-8

# In[29]:


def TSV_transfer(filelocation):
    with open(filelocation, 'r') as f:
        data = f.readlines()

    data_first = []

    i = 0
    while i < len(data):
        one_count = 0
        oneline = {}
        if data[i][:5] == '#Text':
            labels = []

            temp_sen = data[i][6:][:-1]
            lines = 0
            for j in range(i+1, len(data)):
                if data[j][:5] == '#Text':
                    lines += 1
                    temp_sen += ' '
                    temp_sen += data[j][6:][:-1]

                    one_count += 1
                else:

                    break

            if lines == 0:
                oneline['sen'] = data[i][6:]
            else:
                oneline['sen'] = temp_sen + '\n'      


            for j in range(i + 1 + lines, len(data)):


                if data[j] != '\n': #or data[j] !='\t\t\t\t\t\t\n':
                    labels.append(data[j])
                    one_count += 1
                else:
                    break
            oneline['labels'] = labels
            data_first.append(oneline) 

        one_count += 1
        i += one_count 

    res = []
    for p in range(len(data_first)):

        one_line_word = []
        for x in data_first[p]['labels']:
            split_res = x.split('\t')
            temp = {'token_pos': split_res[0], 'char_pos': split_res[1], 'text': split_res[2], 'entity': split_res[3], 
                    'relation type': split_res[4], 'relation of': split_res[5]}
            one_line_word.append(temp)

        sen = []
        for x in one_line_word:
            sen.append(x['text'])

        entities = []
        for x in one_line_word:
            if x['entity'] != '_':
                pos = int (x['token_pos'].split('-')[1] ) - 1
                entities.append({'pos': pos, 'text': x['text'], 'char_pos': x['char_pos'], 'entity': x['entity'] })

        entities_merged = []

        i = 0
        while i < len(entities):
            if entities[i]['entity'][-1] != ']':
                entities_merged.append({'tokenpositions': [entities[i]['pos'] ], 'lexicalInput':  entities[i]['text'], 
                                       'char_pos': entities[i]['char_pos'], 'kbID': entities[i]['entity']})
                i += 1
            else:
                temp = []
                Len = 0
                for j in range(len(entities)):
                    if entities[j]['entity'][-2:] == entities[i]['entity'][-2:]:
                        temp.append(entities[j])
                        Len += 1
                i += Len

                text = ''
                pos= []
                char_pos = temp[0]['char_pos'].split('-')[0] + '-' + temp[-1]['char_pos'].split('-')[1]
                for y in temp:
                    pos.append(y['pos'])
                    if y != temp[-1]:
                        text += y['text']
                        text += ' '
                    else:
                        text += y['text']
                entities_merged.append({'tokenpositions': pos, 'lexicalInput': text, 'char_pos': char_pos, 'kbID': temp[0]['entity'].split('[')[0]})


        relations = []
        for x in one_line_word:
            if x['relation type'] != '_':
                relations.append({'subj': x['token_pos'], 'text': x['text'], 'entity': x['entity'], 'relation type': x['relation type'], 'relation of': x['relation of'] })

        relations_new = []
        for x in relations:
            Res =  x['relation type'].split('|') 
            Reof = x['relation of'].split('|') 
            if len(Res) == 1:
                relations_new.append(x)
            else:
                for i in range(len(Res)):
                    relations_new.append({'subj':x['subj'], 'text': x['text'], 'entity': x['entity'], 
                             'relation type': Res[i], 'relation of': Reof[i] })

        relations_new2 = []
        for i, re in enumerate(relations_new):

            if re['relation of'][-1] == ']':
                index = int(re['relation of'].split('[')[0].split('-')[1] ) - 1 
                for j, en in enumerate(entities_merged):
                    if en['tokenpositions'][0] == index:
                        relations_new2.append(  {'subj': re['subj'], 'text': re['text'], 'entity': re['entity'], 
                             'relation type': re['relation type'], 'relation of': en['tokenpositions'] } )
                        break
            else:
                index = int( re['relation of'].split('-')[1] ) - 1
                for j, en in enumerate(entities_merged):
                    if en['tokenpositions'][0] == index:
                        relations_new2.append(  {'subj': re['subj'], 'text': re['text'], 'entity': re['entity'], 
                             'relation type': re['relation type'], 'relation of': en['tokenpositions'] } )
                        break

        relations_final = []
        for re in relations_new2:
            temp = re['relation of']
            right = int( re['subj'].split('-')[1]) - 1 
            for en in entities_merged:
                if en['tokenpositions'][0] == right:
                    right = en['tokenpositions']
            if type(right) == int:
                right = [right]

            relations_final.append({'kbID': re['relation type'], 'left': temp, 
                                    'right': right })
        res.append({ 'tokens': sen, 'vertexSet': entities_merged, 'edgeSet': relations_final })
    return res

