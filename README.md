# RPP - Random Positions Project

## Documentation
(*full documentation to be done*)

### List of tools and their arguments:
#### Bedfile preprocessing
##### bedfile_processing_filtering_and_midpoints.py (filtering intervals by chromosomes and score; midpoints extraction)
- *chromosomes* (chr1,chr2,chr3 etc.) - optional, for filtering (def. ‘’)
- *inverse* (def. False) – if True, chosen chrs are included in the final output
- *midpoints* (def. False) – if True, midpoints are extracted from intervals
- *score_treshold* (def. 0.) - optional, for filtering positions by score
- *infile* – required – rel/abs path to folder with inputs
- *outfile* (def. . ) - rel/abs path to output directory
- *intermediate_out* (def. None) – rel/abs path to directory to save intermediate file filtered by chrs

##### real_positions.py (keeping only intervals that are part of transcriptome bedfile)
- *same_strands_only* (def. False) – intersect only the same strands
- *transcriptome* – required – rel/abs path to folder with preprocessed transcriptome bedfile
	- preprocessing = textfile_to_bed.py
- *infile* – required – rel/abs path to folder with inputs
- *outfile* (def. . ) - rel/abs path to output directory

##### score_filter.py (filtering by score)
- *score_treshold* (def. 6.) - optional, for filtering positions by score
- *infile* – required – rel/abs path to folder with inputs
- *outfile* (def. . ) - rel/abs path to output directory

##### sequence_extractor.py (generating outputs with interval information and extracted sequence)
- *format* (def. False) – if True, format is tab delimited (header /tab sequence) (False = separate lines)
- *reference* – required – rel/abs path to the preprocessed fasta file with all references
  - preprocessing = all_ref_1_file_simple_headers.py
- *strandness* (def. False) – apply strandness if True
- *infile* – required – rel/abs path to folder with inputs
- *outfile* (def. . ) - rel/abs path to output directory

##### textfile_to_bed.py (processing text file with intervals into formated bedfile)
- *infile* – required – rel/abs path to input file (e.g. downloaded transcriptome.bed/txt which needs to be preprocessed into right format)
- *outfile* – required – rel/abs path to output file (specified name with .bed extension)
  
##### windows.py (extending intervals to defined length)
- *window_size* (def. 50) – intervals extended/shrinked to different length
- *infile* – required – rel/abs path to folder with inputs
- *outfile* (def. . ) - rel/abs path to output directory

#### Fasta preprocessing
##### all_ref_1_file_simple_headers.py (processing provided fasta files into one output)
- *reference* – required – rel/abs path to folder with reference fasta files (must have changed file names into simple chromosome headers – e.g. chr1.fa, chrY.fa etc.)
- *outfile* (def. . ) - rel/abs path to output directory

##### fasta_multiline_to_singleline.py (processing provided multiline sequence fasta files into oneline format)
- *reference* – required – rel/abs path to folder with reference fasta files (must have changed file names into simple chromosome headers – e.g. chr1.fa, chrY.fa etc.)
- *outfile* (def. . ) - rel/abs path to output directory

##### reference_fasta_proportionality.py (creating file with counted proportions and lengths of provided references)
- *prepr_ref* – required - rel/abs path to folder with preprocessed reference fasta files (must have changed 	file names into simple chromosome headers – e.g. chr1.fa) 
	- preprocessing = fasta_multiline_to_singleline.py
- *outfile* (def. . ) - rel/abs path to output directory

#### Random positions generator
##### positions_generator.py (producing bedfile with random intervals according to preprocessed PPMs)
- *alphabet* (def. [‘A’, ‘C’, ‘G’, ‘T’]) - list of nucleotides in order corresponding to PWM
- *datasize* (def. 10000) – number of intervals to create
- *position_probability_matrix* – required – rel/abs path to folder with preprocessed PPMs
	- preprocessing = CISBP_RNA_Db_PWMs_preprocessing.py; create_PPM_from_PWM.py; create_random_PPM.py
- *proportions* – required – rel/abs path to the file with reference names, lengths and proportions
	- preprocessing = reference_fasta_proportionality.py
- *reference* – required - rel/abs path to folder with preprocessed reference fasta files (must have changed 	file names into simple chromosome headers – e.g. chr1.fa) 
  - preprocessing = fasta_multiline_to_singleline.py  
- *outfile* (def. . ) - rel/abs path to output directory

#### PWM preprocessing
##### CISBP-RNA_Db_PWMs_preprocessing.py (preprocessing of PWM text files downloaded from CISBP-RNA Database) 
- *pwm_directory* – required - rel/abs path to folder with pwms downloaded from CISBP Db
- *outfile* (def. . ) - rel/abs path to output directory

##### create_PPM_from_PWM.py (preprocessing of PWM text files downloaded from HOmo sapiens COmprehensive MOdel COllection)
- *prob_weight_matrix* – required – rel/abs path to folder with PWMs downloaded from e.g. https://hocomoco11.autosome.ru/
- *outfile* (def. . ) - rel/abs path to output directory

##### create_random_PPM.py (generating files with random PPM)
- *number* (def. 1) – number of random Probability Position Matrix to create
- *seq_length* (def. 8) – specify length of the created PPM/PPMs
- *outfile* (def. . ) - rel/abs path to output directory

#### Transcriptome preprocessing
##### transcriptome_processing_and_filtering.py (filtering out intervals that are not involved in provided references)
- *reference* – required – rel/abs path to the preprocessed fasta file with all references
	- preprocessing = all_ref_1_file_simple_headers.py
- *transcriptome* – required – rel/abs path to folder with preprocessed transcriptome bedfile
	- preprocessing = textfile_to_bed.py
- *outfile* (def. . ) - rel/abs path to output directory

### Pipeline:
#### External File Sources:
- *all references separately downloaded from:*
  https://www.ncbi.nlm.nih.gov/assembly/GCF_000001405.13/
  and their names were changed according to the regular bedfiles (chr1, chr2, chrY etc.)
- *PWMs from CISBP-RNA database were downloaded from:*
  http://bioinfo.vanderbilt.edu/beRBP/download.html
  (part of Training and testing datasets in Table S1)
- *Other PWM files were downloaded from HOmo sapiens COmprehensive MOdel COllection:*
  https://hocomoco11.autosome.ru/downloads_v11
- *Transcriptome was downloaded from:*
  https://genome.ucsc.edu/cgi-bin/hgTables
  options = region: genome (otherwise default)

#### File Examples:
- *CISBP-RNA Db PWMs:* PUM2, QKI
- *HOMOCOMO type PWMs:* homocomo_train_pwm
- *Reference FASTA files:* chr21, chr22, chrY
- *UCSC transcriptome:* transcriptome

##### Reference fasta files preprocessing
    1. fasta_multiline_to_singleline.py
       $ python tools/fasta_prepr/fasta_multiline_to_singleline.py\
       --reference data_examples/raw_references/ 
    2. reference_fasta_proportionality.py
       $ python tools/fasta_prepr/reference_fasta_proportionality.py\
       --prepr_ref path/to/preprocessed_references/ 
##### PWM preprocessing
    1. CISBP-RNA_Db_PWMs_preprocessing.py 
       $ python tools/pwm_prepr/CISBP-RNA_Db_PWMs_preprocessing.py\
       --pwm_directory data_examples/raw_CISBP_Db_PWMs/
    2. create_PPM_from_PWM.py 
       $ python tools/pwm_prepr/create_PPM_from_PWM.py\
       --prob_weight_matrix individual_parts/data_examples/raw_homocomo_PWMs/
    3. create_random_PPM.py 
       $ python tools/pwm_prepr/create_random_PPM.py 
##### Positions generator
    1. positions_generator.py
       $ python tools/positions_generator/positions_generator.py\
       --reference path/to/preprocessed_references/\
       --position_probability_matrix path/to/preprocessed_pwms/\
       --proportions path/to/preprocessed_references/proportions/
##### Transcriptome preprocessing
    1. transcriptome_processing_and_filtering.py 
       $ python tools/transcriptome_prepr/transcriptome_processing_and_filtering.py\
       --reference path/to/preprocessed_references/
##### Bedfile preprocessing
    1. bed_processing_filtering_and_midpoints.py
       $ python tools/bedfile_prepr/bed_processing_filtering_and_midpoints.py\
       --midpoints True\
       --score_treshold 7.\
       --infile path/to/final_random_positions/ 
    2. real_positions.py
       $ python tools/bedfile_prepr/real_positions.py\
       --same_strands_only True\
       --transcriptome path/to/preprocessed_transcriptome/\
       --infile path/to/preprocessed_bedfiles/filtered_by_score_midpoints/
    3. windows.py
       $ python tools/bedfile_prepr/windows.py\
       --infile path/to/preprocessed_bedfiles/real_positions/
    4. sequence_extractor.py
       $ python tools/bedfile_prepr/sequence_extractor.py\
       --reference path/to/preprocessed_references/all_in_one/\
       --strandness True\
       --format True\
       --infile path/to/preprocessed_bedfiles/windows/

#### Packages version:
- bedtools 2.29.2
- numpy 1.18.1
- numpy-base 1.18.1
- pybedtools 0.8.1
- python 3.7.6
