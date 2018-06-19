import os
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument('--infile', default = os.getcwd(), help='input .C macro of the validation plot')
    args = parser.parse_args()
    
    output_dict={}
    output_dict["correct"] = {}
    output_dict["flipped"] = {}
    output_dict["wrong"] = {}
    output_dict["nomatch"] = {}
    with open(args.infile, 'r') as f:
        file_content = f.readlines() # Read whole file in the file_content string
    for line in file_content:
        if not "SetBinContent" in line: continue
        if "correct" in line:
            if "SetBinContent(1" in line: output_dict["correct"]["inclusive"] = float(line.split(",")[1].split(")")[0]) *100
            if "SetBinContent(2" in line: output_dict["correct"]["ttbb"] = float(line.split(",")[1].split(")")[0])  *100
            if "SetBinContent(3" in line: output_dict["correct"]["ttbj"] = float(line.split(",")[1].split(")")[0])  *100
            if "SetBinContent(4" in line: output_dict["correct"]["ttcc"] = float(line.split(",")[1].split(")")[0])  *100
            if "SetBinContent(5" in line: output_dict["correct"]["ttcj"] = float(line.split(",")[1].split(")")[0])  *100
            if "SetBinContent(6" in line: output_dict["correct"]["ttjj"] = float(line.split(",")[1].split(")")[0])  *100
        
        elif "flipped" in line:
            if "SetBinContent(1" in line: output_dict["flipped"]["inclusive"] = float(line.split(",")[1].split(")")[0])  *100
            if "SetBinContent(2" in line: output_dict["flipped"]["ttbb"] = float(line.split(",")[1].split(")")[0])  *100
            if "SetBinContent(3" in line: output_dict["flipped"]["ttbj"] = float(line.split(",")[1].split(")")[0])  *100
            if "SetBinContent(4" in line: output_dict["flipped"]["ttcc"] = float(line.split(",")[1].split(")")[0])  *100
            if "SetBinContent(5" in line: output_dict["flipped"]["ttcj"] = float(line.split(",")[1].split(")")[0])  *100
            if "SetBinContent(6" in line: output_dict["flipped"]["ttjj"] = float(line.split(",")[1].split(")")[0])  *100
        
        elif "wrong" in line:
            if "SetBinContent(1" in line: output_dict["wrong"]["inclusive"] = float(line.split(",")[1].split(")")[0])  *100
            if "SetBinContent(2" in line: output_dict["wrong"]["ttbb"] = float(line.split(",")[1].split(")")[0])  *100
            if "SetBinContent(3" in line: output_dict["wrong"]["ttbj"] = float(line.split(",")[1].split(")")[0])  *100
            if "SetBinContent(4" in line: output_dict["wrong"]["ttcc"] = float(line.split(",")[1].split(")")[0])  *100
            if "SetBinContent(5" in line: output_dict["wrong"]["ttcj"] = float(line.split(",")[1].split(")")[0])  *100
            if "SetBinContent(6" in line: output_dict["wrong"]["ttjj"] = float(line.split(",")[1].split(")")[0]) *100
        
        elif "nomatch" in line:
            if "SetBinContent(1" in line: output_dict["nomatch"]["inclusive"] = float(line.split(",")[1].split(")")[0])  *100
            if "SetBinContent(2" in line: output_dict["nomatch"]["ttbb"] = float(line.split(",")[1].split(")")[0])  *100
            if "SetBinContent(3" in line: output_dict["nomatch"]["ttbj"] = float(line.split(",")[1].split(")")[0])  *100
            if "SetBinContent(4" in line: output_dict["nomatch"]["ttcc"] = float(line.split(",")[1].split(")")[0])  *100
            if "SetBinContent(5" in line: output_dict["nomatch"]["ttcj"] = float(line.split(",")[1].split(")")[0])  *100
            if "SetBinContent(6" in line: output_dict["nomatch"]["ttjj"] = float(line.split(",")[1].split(")")[0]) *100
    
    output_file_name = args.infile.replace(".C",".csv")
    outfile_ = open(output_file_name, 'w')
    outfile_.write("; inclusive ; ttbb ; ttbj ; ttcc ; ttcj ; ttjj\n")
    outfile_.write("correct ; %.1f ; %.1f ;  %.1f ;  %.1f ;  %.1f ;  %.1f\n"%(output_dict["correct"]["inclusive"],output_dict["correct"]["ttbb"],output_dict["correct"]["ttbj"],output_dict["correct"]["ttcc"],output_dict["correct"]["ttcj"],output_dict["correct"]["ttjj"]))
    outfile_.write("flipped ; %.1f ; %.1f ;  %.1f ;  %.1f ;  %.1f ;  %.1f\n"%(output_dict["flipped"]["inclusive"],output_dict["flipped"]["ttbb"],output_dict["flipped"]["ttbj"],output_dict["flipped"]["ttcc"],output_dict["flipped"]["ttcj"],output_dict["flipped"]["ttjj"]))
    outfile_.write("wrong ; %.1f ; %.1f ;  %.1f ;  %.1f ;  %.1f ;  %.1f\n"%(output_dict["wrong"]["inclusive"],output_dict["wrong"]["ttbb"],output_dict["wrong"]["ttbj"],output_dict["wrong"]["ttcc"],output_dict["wrong"]["ttcj"],output_dict["wrong"]["ttjj"]))
    outfile_.write("nomatch ; %.1f ; %.1f ;  %.1f ;  %.1f ;  %.1f ;  %.1f\n"%(output_dict["nomatch"]["inclusive"],output_dict["nomatch"]["ttbb"],output_dict["nomatch"]["ttbj"],output_dict["nomatch"]["ttcc"],output_dict["nomatch"]["ttcj"],output_dict["nomatch"]["ttjj"]))
    
if __name__ == "__main__":
    main()