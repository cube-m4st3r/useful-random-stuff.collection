input_file = input("Please specify an input file: ")
output_file = input("Please specify an output file: ")
string_to_delete = input("Please specify what you want to delete: ")

delete_list = [string_to_delete]
with open(input_file) as fin, open(output_file, "w+") as fout:
    for line in fin:
        for word in delete_list:
            line = line.replace(word, "")
        fout.write(line)
    
print(f"Deleted all specified: {delete_list} items")