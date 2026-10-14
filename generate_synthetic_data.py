"""Generate clearly synthetic educational data; never overwrite existing files."""
import argparse
import csv
from pathlib import Path
import random

def generate(output,rows=128,seed=42):
    if type(rows) is not int or not 1<=rows<=1000:
        raise ValueError('Use 1..1000 rows')
    output=Path(output)
    generator=random.Random(seed)
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x',newline='',encoding='utf-8') as stream:
        writer=csv.writer(stream);writer.writerow(['x1','x2','x3','y'])
        for _ in range(rows):
            x1,x2,x3=[generator.uniform(-1,1) for _ in range(3)]
            writer.writerow([x1,x2,x3,int(x1*x2+x3>0)])
    return rows

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--rows',type=int,default=128)
    args=parser.parse_args();print('Synthetic rows written:',generate(args.output,args.rows))
