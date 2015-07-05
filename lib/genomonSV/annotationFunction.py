#!/usr/bin/env python

import pysam

def addAnnotation(inputFilePath, outputFilePath, Params):

    hIN = open(inputFilePath, 'r')
    hOUT = open(outputFilePath, 'w')

    gene_bed = Params["gene_bed"]
    exon_bed = Params["exon_bed"]

    gene_tb = pysam.TabixFile(gene_bed)
    exon_tb = pysam.TabixFile(exon_bed)

    for line in hIN:

        F = line.rstrip('\n').split('\t')

        tumorAF = 0
        if float(F[7]) + float(F[8]) > 0: tumorAF = float(F[8]) / (float(F[7]) + float(F[8]))
        normalAF = 0
        if float(F[9]) + float(F[10]) > 0: normalAF = float(F[10]) / (float(F[9]) + float(F[10]))

        ##########
        # check gene annotation for the side 1  
        tabixErrorFlag = 0
        try:
            records = gene_tb.fetch(F[0], int(F[1]) - 1, int(F[1]))
        except Exception as inst:
            print >> sys.stderr, "%s: %s" % (type(inst), inst.args)
            tabixErrorFlag = 1

        gene1 = [];
        if tabixErrorFlag == 0:
            for record_line in records:
                record = record_line.split('\t')
                gene1.append(record[3])

        if len(gene1) == 0: gene1.append("---")
        gene1 = list(set(gene1))
        ##########

        ##########
        # check gene annotation for the side 2
        tabixErrorFlag = 0
        try:
            records = gene_tb.fetch(F[3], int(F[4]) - 1, int(F[4]))
        except Exception as inst:
            print >> sys.stderr, "%s: %s" % (type(inst), inst.args)
            tabixErrorFlag = 1

        gene2 = [];
        if tabixErrorFlag == 0:
            for record_line in records:
                record = record_line.split('\t')
                gene2.append(record[3])

        if len(gene2) == 0: gene2.append("---")
        gene2 = list(set(gene2))
        ##########

        ##########
        # check exon annotation for the side 1
        tabixErrorFlag = 0
        try:
            records = exon_tb.fetch(F[0], int(F[1]) - 1, int(F[1]))
        except Exception as inst:
            print >> sys.stderr, "%s: %s" % (type(inst), inst.args)
            tabixErrorFlag = 1

        exon1 = [];
        if tabixErrorFlag == 0:
            for record_line in records:
                record = record_line.split('\t')
                exon1.append(record[3])

        if len(exon1) == 0: exon1.append("---")
        exon1 = list(set(exon1))
        ##########

        ##########
        # check exon annotation for the side 2
        tabixErrorFlag = 0
        try:
            records = exon_tb.fetch(F[3], int(F[4]) - 1, int(F[4]))
        except Exception as inst:
            print >> sys.stderr, "%s: %s" % (type(inst), inst.args)
            tabixErrorFlag = 1
       
        exon2 = [];
        if tabixErrorFlag == 0:
            for record_line in records:
                record = record_line.split('\t')
                exon2.append(record[3])

        if len(exon2) == 0: exon2.append("---")
        exon2 = list(set(exon2))
        ##########

        if F[0] != F[3]:
            SVtype = "translocation"
        elif F[2] == "+" and F[5] == "-":
            SVtype = "deletion"
        elif F[2] == "-" and F[5] == "+":
            SVtype = "tandem_duplication"
        else:
            SVtype = "inversion"

        print >> hOUT, '\t'.join(F[0:7]) + '\t' + SVtype + '\t' + ';'.join(gene1) + '\t' + ';'.join(gene2) + '\t' + ';'.join(exon1) + '\t' + ';'.join(exon2) + '\t' + \
              '\t'.join(F[7:11]) + '\t' + str(round(tumorAF, 4)) + '\t' + str(round(normalAF, 4)) + '\t' + str(round(float(F[11]), 4))


    hIN.close()
    hOUT.close()
    gene_tb.close()
    exon_tb.close()

