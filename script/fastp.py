import os
import subprocess
import argparse
import json

docker="edna:latest"
def run(pe1,outdir,prefix,pe2=None):
    pe1 = os.path.abspath(pe1)
    in_dir = os.path.dirname(pe1)
    outdir = os.path.abspath(outdir)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    a = pe1.split("/")[-1]

    cmd = "docker run -v %s:/raw_data/ -v %s:/outdir/ %s " % (in_dir,outdir, docker)
    cmd += ("sh -c \'export PATH=/opt/conda/envs/edna/bin/:$PATH && fastp -i /raw_data/%s -o /outdir/%s.clean_R1.fastq "
            "--disable_quality_filtering --length_required 100 --dont_eval_duplication "
            "--thread 16 --cut_front --cut_front_window_size 1 --cut_front_mean_quality 20 "
            "--cut_tail --cut_front_window_size 1 --cut_tail_mean_quality 20 "
            "--html /outdir/%s.fastp.html --json /outdir/%s.fastp.json ") % (a, prefix, prefix, prefix)
    if pe2 is not None:
        pe2=os.path.abspath(pe2)
        if in_dir != os.path.dirname(pe2):
            print("read1 and reads2 must be in the same directory.")
            exit()
        b = pe2.split("/")[-1]
        cmd += ("-I /raw_data/%s -O /outdir/%s.clean_R2.fastq\'") % (b,prefix)
    else:
        cmd+='\''
    print(cmd)
    subprocess.check_call(cmd, shell=True)
    out=outdir+'/'+prefix
    outfile = open("%s.fastp.tsv" % (out), "w")
    outfile.write("SampleID\tRaw_reads\tTotal_bases\tQ20_rate\tQ30_rate\tGC_content\tClean_reads\tClean_bases\tQ20_rate\tQ30_rate\tGC_content\n")
    with open("%s.fastp.json"%out, "r") as load_f:
        load_dict = json.load(load_f)
        outfile.write("%s\t" % (prefix))
        outfile.write("%s\t%s\t%s\t%s\t%s\t"
                      % (load_dict['summary']['before_filtering']['total_reads'],
                         load_dict['summary']['before_filtering']['total_bases'],
                         load_dict['summary']['before_filtering']['q20_rate'],
                         load_dict['summary']['before_filtering']['q30_rate'],
                         load_dict['summary']['before_filtering']['gc_content']))
        outfile.write("%s\t%s\t%s\t%s\t%s\n"
                      % (load_dict['summary']['after_filtering']['total_reads'],
                         load_dict['summary']['after_filtering']['total_bases'],
                         load_dict['summary']['after_filtering']['q20_rate'],
                         load_dict['summary']['after_filtering']['q30_rate'],
                         load_dict['summary']['after_filtering']['gc_content']))

    outfile.close()

if __name__=="__main__":
    parser=argparse.ArgumentParser("Run fastp quality control.")
    parser.add_argument("-p1","--pe1",help="R1 fastq.gz",required=True)
    parser.add_argument("-p2","--pe2",help="R2 fastq.gz",default=None)
    parser.add_argument("-p","--prefix",help="prefix of output",required=True)
    parser.add_argument("-o","--outdir",help="output directory",required=True)
    args=parser.parse_args()
    run(args.pe1,args.outdir,args.prefix,args.pe2)