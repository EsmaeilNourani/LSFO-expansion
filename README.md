# LSFC-expansion

## Lifestyle factor detection in the biomedical literature: comprehensive resources for enhanced named entity recognition

### Overview
In this work, we present a novel Lifestyle Factor Classification (LSFC), featuring a diverse hierarchical classification of LSFs, serving the development of a dictionary-based NER system that facilitates the recognition and normalization of matched LSF concepts. Additionally, an annotated corpus for LSFs is introduced, enabling the deep learning-based training and evaluation of a transformer-based NER system for LSF detection. Both NER systems were used to detect LSFs in PubMed and PMC Open Access articles, resulting in the identification of over 300 million LSF instances in the biomedical literature.

Associated Zenodo page for files: [Zenodo - LSFC-expansion](https://zenodo.org/records/10450308)

### Submodules

#### LSFC
[LSFC](https://github.com/EsmaeilNourani/Lifestyle-factors-classification) - This repository contains the actual LSFC. Lifestyle-factors classification (LSFC) is a multilevel hierarchical structure that begins with main lifestyle categories at the top level and extends to specific subcategories and low-level concepts.

#### S1000_Transformer_NER
[S1000_Transformer_NER](https://github.com/EsmaeilNourani/S1000-transformer-ner) - This repository is a fork of the S1000-transformer-ner project. It has been minorly adapted for specific use in training as a Named Entity Recognition (NER) system focused on the detection of Lifestyle factors.

### Installation and Setup
To clone this repository along with its submodules, use the following command:
```bash
git clone --recurse-submodules [Your_Main_Repository_URL]
cd LSFC-expansion
# Additional setup instructions if needed
