
with open('./posts.jl', 'r') as file, open('./posts_out.jl', 'w') as out_file:
    for i, line in enumerate(file, start=1):
        out_file.write('{ "index" : { "_index": "posts", "_id" : "' + str(i) + '" } }\n')
        out_file.write(line)
        #print(str(i) + " " + line, end='')
